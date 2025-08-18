#!/usr/bin/env python3
# study_notions_manager.py
import re
import shutil
from pathlib import Path
from typing import Optional, Dict
import streamlit as st
from urllib.parse import quote, unquote
import re, shutil
from pathlib import Path
from typing import Optional, Dict
from urllib.parse import unquote, quote

st.set_page_config(page_title="Study Notion Organizer", layout="wide")


from branch import (  # type: ignore
    list_categories,
    list_category_mds,
    process_one_md_in_category,
)


# ------------------ 기본 설정 ------------------
DEFAULT_STUDY_ROOT = Path(".").resolve()
NOTION_DIRNAME = "notion"
EXCLUDE_MD = {"README.md"}

# 긴 식별번호: 공백 + 16자 이상 영숫자
ID_TAIL_RE = re.compile(r"^(?P<title>.+?)\s(?P<id>[0-9A-Za-z]{16,})$")


# ------------------------------------------------
# 유틸
# ------------------------------------------------
def split_title_and_id(stem: str):
    """
    '제목 <긴식별번호>' -> ('제목', '<id>')
    식별번호 없으면 ('제목', None)
    """
    m = ID_TAIL_RE.match(stem)
    if m:
        return m.group("title"), m.group("id")
    return stem, None

def normalize_empty(s: str) -> str:
    return re.sub(r"\s+", "_", s.strip())

def _rename_files_spaces_to_underscores(root_dir: Path) -> Dict[str, str]:
    """
    root_dir 하위 모든 파일의 파일명 내 공백을 '_'로 치환.
    반환: {원래파일명: 새파일명} (파일명만, 경로 제외)
    - 동일 디렉토리 내에서만 의미 있음 (중복 파일명 충돌 방지)
    """
    mapping: Dict[str, str] = {}
    # 파일 경로 길이가 긴 것부터(하위 경로 먼저) 안전하게 처리
    for p in sorted(root_dir.rglob("*"), key=lambda x: len(str(x)), reverse=True):
        if p.is_file():
            new_name = normalize_empty(p.name)
            if new_name != p.name:
                new_path = p.with_name(new_name)
                if new_path.exists():
                    new_path.unlink()
                p.rename(new_path)
                mapping[p.name] = new_name
    return mapping

#1
# def _rewrite_links_folder_and_filenames(md_text: str, old_dir: str, new_dir: str, fname_map: Dict[str, str]) -> str:
# def _rewrite_links_folder_and_filenames(md_text: str, old_dir: str, category: str, new_dir: str, fname_map: Dict[str, str]) -> str:
#
#     """
#     MD 내부 이미지 링크에서:
#       - 상위 폴더명 old_dir → new_dir
#       - 파일명 공백 치환 등으로 바뀐 경우 fname_map을 반영
#     URL 인코딩/비인코딩 경로 모두 처리.
#     """
#     img_link_re = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
#
#     # old_dir 매칭 후보(인코딩/비인코딩)
#     old_variants = {
#         old_dir.strip("/").replace("\\", "/"),
#         quote(old_dir.strip("/").replace("\\", "/")),
#     }
#
#     def repl(m):
#         alt, path = m.group(1), m.group(2)
#         decoded = unquote(path).lstrip("./").replace("\\", "/")
#
#         for old in old_variants:
#             if decoded == old:
#                 # 폴더만 가리키는 경우
#                 new_rel = new_dir
#                 return f"![{alt}]({new_rel})"
#             if decoded.startswith(old + "/"):
#                 tail = decoded[len(old):].lstrip("/")        # 폴더 이후 경로
#                 # 파일명만 치환 적용
#                 tail_path = Path(tail)
#                 fname = tail_path.name
#                 parent_rel = str(tail_path.parent).replace("\\", "/")
#                 new_fname = fname_map.get(fname, normalize_empty(fname))  # 맵 없으면 공백치환만
#                 new_rel = new_dir + ("/" + parent_rel if parent_rel not in ("", ".") else "")
#                 # 안전하게 <>로 감싸기 (공백 등 특수문자 대비) + URL 인코딩
#                 # final_path = "/".join(quote(seg) for seg in new_rel.split("/")) + "/" + quote(new_fname)
#                 final_path = f"/assets/{category}/{new_dir}/{new_fname}"
#
#                 return f"![{alt}](<{final_path}>)"
#         return m.group(0)
#
#     return img_link_re.sub(repl, md_text)
def _rewrite_links_folder_and_filenames(md_text: str, old_dir: str, new_dir: str, fname_map: Dict[str, str], category: str) -> str:
    """
    MD 내 이미지 링크를 assets/<category>/<new_dir>/<파일명> 으로 변경
    """
    pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

    def repl(m):
        alt, path = m.group(1), unquote(m.group(2)).lstrip("./").replace("\\", "/")
        if path.startswith(old_dir) or path.startswith(old_dir + "/"):
            fname = Path(path).name
            new_fname = fname_map.get(fname, normalize_empty(fname))
            return f"![{alt}](/study/assets/{category}/{new_dir}/{new_fname})"
        return m.group(0)

    return pattern.sub(repl, md_text)


# def split_title_and_id(stem: str):
#     """
#     '제목 <긴식별번호>' -> ('제목_가공됨', '<id>')
#     - 식별번호 없으면 ('제목_가공됨', None)
#     - 공백은 '_'로 치환
#     """
#     m = ID_TAIL_RE.match(stem)
#     if m:
#         raw_title = m.group("title")
#         file_id = m.group("id")
#     else:
#         raw_title = stem
#         file_id = None
#
#     # 공백을 "_"로 통일
#     safe_title = raw_title.strip().replace(" ", "_")
#
#     return safe_title, file_id



def find_pair_image_dir(md_path: Path) -> Optional[Path]:
    """
    MD와 짝인 이미지 폴더 탐색:
      1) '<제목> <id>' 폴더
      2) '<제목>' 폴더(드물지만)
    """
    stem = md_path.stem
    title, file_id = split_title_and_id(stem)
    parent = md_path.parent
    # 1순위: 제목 + 식별번호
    if file_id:
        p = parent / f"{title} {file_id}"
        if p.is_dir():
            return p
    # 2순위: 제목만
    p2 = parent / title
    if p2.is_dir():
        return p2
    return None


def list_notion_mds(notion_root: Path):
    return sorted([p for p in notion_root.glob("*.md") if p.name not in EXCLUDE_MD])


def list_categories(notion_root: Path):
    return sorted([d for d in notion_root.iterdir() if d.is_dir()])


# 식별코드 제거 리네임
def _rewrite_links_folder_rename(md_text: str, old_dir_name: str, new_dir_name: str) -> str:
    """
    MD 내부 이미지 링크에서 폴더명만 교체.
    예) ![...](old_dir/aaa.png) -> ![...](new_dir/aaa.png)
    - URL 인코딩(%20 등)된 old_dir도 매칭
    """
    pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    old_variants = {
        old_dir_name.strip("/").replace("\\", "/"),
        quote(old_dir_name.strip("/").replace("\\", "/")),  # 공백 → %20 등
    }

    def repl(m):
        alt, path = m.group(1), m.group(2)
        decoded = unquote(path).lstrip("./").replace("\\", "/")
        for old in old_variants:
            if decoded == old:
                # 폴더만 참조하는 경우는 유지
                return f"![{alt}]({new_dir_name})"
            if decoded.startswith(old + "/"):
                tail = decoded[len(old):].lstrip("/")
                return f"![{alt}]({new_dir_name}/{tail})"
        return m.group(0)

    return pattern.sub(repl, md_text)


# def move_pair(md: Path, img_dir: Optional[Path], dest_cat_dir: Path) -> Path:
#     """
#     선택한 카테고리 폴더로 MD와 이미지 폴더를 함께 이동.
#     파일/폴더명은 변경하지 않음.
#     """
#     dest_cat_dir.mkdir(parents=True, exist_ok=True)
#     # 1) MD 이동
#     md_dest = dest_cat_dir / md.name
#     if md_dest.exists():
#         md_dest.unlink()
#     shutil.move(str(md), str(md_dest))
#     # 2) 이미지 폴더 이동
#     if img_dir and img_dir.exists():
#         img_dest = dest_cat_dir / img_dir.name
#         if img_dest.exists():
#             shutil.rmtree(img_dest)
#         shutil.move(str(img_dir), str(img_dest))
#     return md_dest

#2
# def move_pair(md: Path, img_dir: Optional[Path], dest_cat_dir: Path) -> Path:
#     """
#     선택한 카테고리 폴더로 MD와 이미지 폴더를 함께 이동.
#     - MD/폴더의 식별코드(ID) 제거하여 <제목>만 남김
#     - MD 본문 내 이미지 링크의 폴더명도 함께 업데이트
#     """
#     dest_cat_dir.mkdir(parents=True, exist_ok=True)
#
#     # 0) 제목/ID 분리
#     title, _ = split_title_and_id(md.stem)
#
#     new_md_name = f"{title}.md"
#     md_dest = dest_cat_dir / new_md_name
#
#     # 1) MD 본문 로드
#     text = md.read_text(encoding="utf-8")
#
#     # 2) 이미지 폴더 이동 + 링크 교체
#     if img_dir and img_dir.exists():
#         old_dir_name = img_dir.name
#         # 이미지 새 폴더명(식별코드 제거): 제목만
#         new_img_dir = dest_cat_dir / title
#         if new_img_dir.exists():
#             shutil.rmtree(new_img_dir)
#         # 먼저 폴더를 목적지의 새 이름으로 "이동"
#         shutil.move(str(img_dir), str(new_img_dir))
#
#         # MD 내부 링크에서 old_dir_name → title 로 치환
#         text = _rewrite_links_folder_rename(
#             md_text=text,
#             old_dir_name=old_dir_name,
#             new_dir_name=title
#         )
#
#     # 3) MD 쓰고 이동(동명 파일 있으면 덮어쓰기)
#     if md_dest.exists():
#         md_dest.unlink()
#     md.write_text(text, encoding="utf-8")
#     shutil.move(str(md), str(md_dest))
#
#     return md_dest

# 3
# def move_pair(md: Path, img_dir: Optional[Path], dest_cat_dir: Path) -> Path:
#     """
#     선택한 카테고리 폴더로 MD와 이미지 폴더를 함께 이동.
#     - 식별코드 제거 → 제목만 사용
#     - 제목/폴더/파일의 공백은 '_'로 치환 (정규화)
#     - MD 본문 내 이미지 링크도 폴더명/파일명 변경에 맞춰 업데이트
#     """
#     dest_cat_dir.mkdir(parents=True, exist_ok=True)
#
#     # 0) 제목/ID 분리 → 제목 정규화
#     raw_title, _ = split_title_and_id(md.stem)
#     safe_title = normalize_empty(raw_title)
#
#     # MD 대상 경로 (정규화된 제목)
#     new_md_name = f"{safe_title}.md"
#     md_dest = dest_cat_dir / new_md_name
#
#     # 1) MD 본문 로드
#     text = md.read_text(encoding="utf-8")
#
#     # 2) 이미지 폴더 이동 + 파일명 공백 치환 + 링크 교체
#     if img_dir and img_dir.exists():
#         old_dir_name = img_dir.name  # MD 내부엔 이 이름(또는 인코딩)이 들어있을 수 있음
#         new_img_dir = dest_cat_dir / safe_title
#
#         if new_img_dir.exists():
#             shutil.rmtree(new_img_dir)
#         # 먼저 카테고리 폴더 안으로 폴더 자체 이동
#         shutil.move(str(img_dir), str(new_img_dir))
#
#         # 폴더 내부 파일들의 공백 → '_' 일괄 변경 (맵 확보)
#         fname_map = _rename_files_spaces_to_underscores(new_img_dir)
#
#         # MD 내부 링크에서 old_dir_name → safe_title, 파일명 변경 반영
#         text = _rewrite_links_folder_and_filenames(
#             md_text=text,
#             old_dir=old_dir_name,
#             new_dir=safe_title,
#             fname_map=fname_map
#         )
#
#     # 3) MD 쓰고 이동(동명 파일 있으면 덮어쓰기)
#     if md_dest.exists():
#         md_dest.unlink()
#     md.write_text(text, encoding="utf-8")
#     shutil.move(str(md), str(md_dest))
#
#     return md_dest
def move_pair(md: Path, img_dir: Optional[Path], dest_cat_dir: Path, category: str) -> Path:
    """
    선택한 카테고리 폴더로 MD와 이미지 폴더를 함께 이동.
    - 식별코드 제거 → 제목만 사용
    - 제목/폴더/파일의 공백은 '_'로 치환 (정규화)
    - MD 본문 내 이미지 링크도 폴더명/파일명 변경에 맞춰 업데이트
      → 최종 경로는 assets/<category>/<title>/<파일명>
    """
    dest_cat_dir.mkdir(parents=True, exist_ok=True)

    # 0) 제목/ID 분리 → 제목 정규화
    raw_title, _ = split_title_and_id(md.stem)
    safe_title = normalize_empty(raw_title)

    # MD 대상 경로
    new_md_name = f"{safe_title}.md"
    md_dest = dest_cat_dir / new_md_name

    # 1) MD 본문 로드
    text = md.read_text(encoding="utf-8")

    # 2) 이미지 폴더 이동 + 파일명 공백 치환 + 링크 교체
    if img_dir and img_dir.exists():
        old_dir_name = img_dir.name
        new_img_dir = dest_cat_dir / safe_title

        if new_img_dir.exists():
            shutil.rmtree(new_img_dir)
        shutil.move(str(img_dir), str(new_img_dir))

        # 내부 파일 공백 → `_`로 치환 (매핑 딕셔너리 생성)
        fname_map = _rename_files_spaces_to_underscores(new_img_dir)

        # 링크 치환 (assets/<category>/<safe_title>/<파일명>)
        text = _rewrite_links_folder_and_filenames(
            md_text=text,
            old_dir=old_dir_name,
            new_dir=safe_title,
            fname_map=fname_map,
            category=category   # 🔑 추가됨
        )

    # 3) MD 쓰고 이동
    if md_dest.exists():
        md_dest.unlink()
    md.write_text(text, encoding="utf-8")
    shutil.move(str(md), str(md_dest))

    return md_dest

# ------------------------------------------------
# Streamlit 레이아웃 (함수 분리)
# ------------------------------------------------
def setup_page():
    st.title("📚 Study Notion Organizer")


# def sidebar_settings() -> Optional[Path]:
# def sidebar_settings() -> Optional[tuple[Path, Path]]:
#
#     """
#     사이드바: 루트 경로 입력/검증 후 notion_root 반환.
#     """
#     with st.sidebar:
#         st.header("Settings")
#         root_str = st.text_input("Study root path", str(DEFAULT_STUDY_ROOT))
#         # 윈도우 경로 호환: \ 대신 / 로 입력해도 OK
#         root = Path(root_str.replace("\\", "/")).expanduser().resolve()
#         if not root.exists():
#             st.error(f"경로가 존재하지 않습니다: {root}")
#             return None
#
#         notion_root = root / NOTION_DIRNAME
#         if not notion_root.exists():
#             st.error(f"노션 폴더가 없습니다: {notion_root}")
#             return None
#
#         st.caption(f"Notion dir: `{notion_root}`")
#         st.divider()
#         return notion_root
# --- 사이드바 설정: study_root, notion_root 튜플 반환 ---
def sidebar_settings() -> tuple[Path, Path] | tuple[None, None]:
    with st.sidebar:
        st.header("Settings")
        root_str = st.text_input("Study root path", str(DEFAULT_STUDY_ROOT))
        root = Path(root_str.replace("\\", "/")).expanduser().resolve()

        if not root.exists():
            st.error(f"경로가 존재하지 않습니다: {root}")
            return (None, None)

        notion_root = root / NOTION_DIRNAME
        if not notion_root.exists():
            st.error(f"노션 폴더가 없습니다: {notion_root}")
            return (None, None)

        st.caption(f"Notion dir: `{notion_root}`")
        st.divider()
        return (root, notion_root)




def sidebar_category_create(notion_root: Path):
    """
    사이드바: 새 카테고리 생성 UI
    """
    with st.sidebar:
        st.subheader("➕ 새 카테고리 만들기")
        new_cat = st.text_input("카테고리 이름", placeholder="예) 의료인공지능, transformer, cv ...")
        if st.button("카테고리 생성", type="primary", use_container_width=True):
            if not new_cat.strip():
                st.warning("카테고리 이름을 입력하세요.")
            else:
                new_dir = notion_root / new_cat.strip()
                if new_dir.exists():
                    st.info("이미 존재하는 카테고리입니다.")
                else:
                    new_dir.mkdir(parents=True, exist_ok=True)
                    st.success(f"생성됨: {new_dir}")
                    # st.experimental_rerun()





def sidebar_show_categories(notion_root: Path):
    """
    사이드바: 현재 카테고리 목록만 표시 (중복 생성 방지 체크용)
    """
    with st.sidebar:
        cats = [d.name for d in list_categories(notion_root)]
        st.subheader("🏷️ 현재 카테고리")
        if not cats:
            st.info("아직 카테고리가 없습니다. 위에서 새로 만드세요.")
        else:
            st.markdown(" ".join(f"`{c}`" for c in cats))
            st.caption(f"총 {len(cats)}개")


def main_md_mover(notion_root: Path):
    """
    메인 영역: MD 목록 표시 → 체크 → 선택 카테고리로 이동
    """
    mds = list_notion_mds(notion_root)
    st.subheader("📝 Categorization")
    if not mds:
        st.info("노션 루트에 MD 파일이 없습니다. (MD + 이미지 폴더를 notion/ 아래에 두세요)")
        return

    cats = [d.name for d in list_categories(notion_root)]
    selected_cat = st.selectbox("보낼 카테고리 선택", options=["(선택)"] + cats, index=0)

    cols = st.columns(2)
    picks: Dict[Path, bool] = {}
    for i, md in enumerate(mds):
        with cols[i % 2]:
            chk = st.checkbox(f"{md.name}", key=f"pick_{md.name}")
            picks[md] = chk
            # 짝인 이미지 폴더 존재 여부 표시
            pair_dir = find_pair_image_dir(md)
            st.caption("🖼️ 이미지 폴더 연결됨" if pair_dir else "⚠️ 이미지 폴더 없음")

    if st.button("📦 카테고리로 보내기", type="primary", use_container_width=True):
        if selected_cat == "(선택)":
            st.warning("먼저 카테고리를 선택하세요.")
            return
        dest_dir = notion_root / selected_cat
        moved = []
        for md, ok in picks.items():
            if not ok:
                continue
            img_dir = find_pair_image_dir(md)
            # new_md = move_pair(md, img_dir, dest_dir)
            new_md = move_pair(md, img_dir, dest_dir, selected_cat)

            moved.append(new_md.name)
        if moved:
            st.success(f"{len(moved)}개 항목 이동 완료 → `{dest_dir}`")
            for name in moved:
                st.write(f"- {name}")
            # st.experimental_rerun()
        else:
            st.info("선택된 항목이 없습니다.")

# === 카테고리 브라우저 ===
def ui_browse_category_files(notion_root: Path):
    st.subheader("📂 Branching")

    cats = [d.name for d in list_categories(notion_root)]
    if not cats:
        st.info("카테고리가 없습니다.")
        return

    cat_name = st.selectbox("카테고리 선택", options=cats, index=0)
    cat_dir = notion_root / cat_name

    # MD와 폴더 리스트
    mds = sorted(cat_dir.glob("*.md"))
    dirs = [d for d in cat_dir.iterdir() if d.is_dir()]

    matched, missing = [], []
    for md in mds:
        pair_dir = find_pair_image_dir(md)
        if pair_dir:
            matched.append(md)
        else:
            missing.append(md)

    # 요약 정보
    st.markdown(
        f" MD 파일: {len(mds)}개 **폴더(이미지 등)**: {len(dirs)}개"
    )
    # 파일명 리스트
    if not mds:
        st.caption("MD 파일이 없습니다.")
    else:
        for md in mds:
            st.write(f"- {md.name}")



# def ui_browse_category_files_with_branch(notion_root: Path):
#     st.subheader("📂 카테고리 안의 파일 확인 & 분기")
#
#     cats = [d.name for d in list_categories(notion_root)]
#     if not cats:
#         st.info("카테고리가 없습니다.")
#         return
#
#     cat_name = st.selectbox("카테고리 선택", options=cats, index=0)
#     cat_dir = notion_root / cat_name
#
#     # MD와 폴더 리스트
#     mds = sorted(cat_dir.glob("*.md"))
#     dirs = [d for d in cat_dir.iterdir() if d.is_dir()]
#
#     # 요약 정보
#     st.markdown(f"- **카테고리**: `{cat_name}`  \n- **MD 파일**: {len(mds)}개  \n- **폴더(이미지 등)**: {len(dirs)}개")
#
#     st.divider()
#     st.write("### 📑 MD 파일 목록 (분기할 파일 선택)")
#     if not mds:
#         st.caption("MD 파일이 없습니다.")
#         return
#
#     # 체크박스 나열
#     cols = st.columns(2)
#     picks = {}
#     for i, md in enumerate(mds):
#         with cols[i % 2]:
#             picks[md] = st.checkbox(md.name, key=f"pick_{cat_name}_{md.name}")
#
#     st.divider()
#     if st.button("🚚 선택한 파일 분기하기", type="primary", use_container_width=True):
#         chosen = [md for md, ok in picks.items() if ok]
#         if not chosen:
#             st.warning("분기할 파일을 선택하세요.")
#             return
#         moved = []
#         errors = []
#         for md in chosen:
#             try:
#                 out = process_one_md_in_category(md, category=cat_name)
#                 moved.append(out.name)
#             except Exception as e:
#                 errors.append((md.name, str(e)))
#         if moved:
#             st.success(f"{len(moved)}개 문서 분기 완료 → `study/{cat_name}` 및 `study/assets/{cat_name}`")
#             for name in moved:
#                 st.write(f"- {name}")
#             # st.experimental_rerun()
#         if errors:
#             st.error("오류 발생:")
#             for n, msg in errors:
#                 st.write(f"- {n}: {msg}")
# --- 카테고리 브라우저 + 분기 ---
def ui_browse_category_files_with_branch(study_root: Path, notion_root: Path):
    st.subheader("📂 Branching")

    cats = [d.name for d in list_categories(notion_root)]
    if not cats:
        st.info("no category")
        return

    cat_name = st.selectbox("category selection", options=cats, index=0)
    cat_dir = notion_root / cat_name

    mds = sorted(cat_dir.glob("*.md"))
    dirs = [d for d in cat_dir.iterdir() if d.is_dir()]

    st.markdown(
        f"- **카테고리**: `{cat_name}`  \n"
        f"- **MD 파일**: {len(mds)}개  \n"
        f"- **폴더(이미지 등)**: {len(dirs)}개"
    )

    st.write("### 📑 Branching file selection)")
    if not mds:
        st.caption("MD 파일이 없습니다.")
        return

    cols = st.columns(2)
    picks: dict[Path, bool] = {}
    for i, md in enumerate(mds):
        with cols[i % 2]:
            picks[md] = st.checkbox(md.name, key=f"pick_{cat_name}_{md.name}")

    st.divider()
    if st.button("🚚 선택한 파일 분기하기", type="primary", use_container_width=True):
        chosen = [md for md, ok in picks.items() if ok]
        if not chosen:
            st.warning("분기할 파일을 선택하세요.")
            return

        moved, errors = [], []
        for md in chosen:
            try:
                out = process_one_md_in_category(
                    md_path=md,
                    category=cat_name,
                    study_root=study_root,            # ✅ 필수 인자
                    notion_root=notion_root,
                    assets_root=study_root / "assets",
                )
                moved.append(out.name)
            except Exception as e:
                errors.append((md.name, str(e)))

        if moved:
            st.success(f"{len(moved)}개 문서 분기 완료 → `study/{cat_name}` 및 `study/assets/{cat_name}`")
            for name in moved:
                st.write(f"- {name}")
            st.rerun()  # ✅ 최신 API

        if errors:
            st.error("오류 발생 목록")
            for n, msg in errors:
                st.write(f"- {n}: {msg}")


from pathlib import Path
import streamlit as st

DEFAULT_EXCLUDE = [".idea", "assets", "notion", "tools"]

def ui_dir_checker_recursive(default_root: str = r"G:\study"):
    st.divider()

    st.subheader("📂 derectory search")

    st.caption(
        "루트 경로부터 시작해서 하위 폴더를 단계별로 선택하며 탐색할 수 있습니다. "
        "제외할 폴더는 멀티셀렉트로 관리할 수 있으며, 최종 선택한 폴더의 **파일 목록**을 보여줍니다."
    )


    root = Path(default_root)
    if not root.exists():
        st.error(f"경로가 존재하지 않습니다: {root}")
        return

    # 제외 폴더 옵션
    all_dirs = [d.name for d in root.iterdir() if d.is_dir()]

    col1, col2 = st.columns([0.7, 0.3])
    with col2:

        exclude = st.multiselect(
            "제외할 폴더 선택",
            options=all_dirs,
            default=DEFAULT_EXCLUDE,
            help="체크된 폴더는 목록에서 제외됩니다."
        )

        # 탐색 시작
        current_dir = root
        depth = 0
    with col1:
        while True:
            # 현재 폴더 안의 하위 폴더만 나열 (제외 반영)
            subdirs = [d for d in current_dir.iterdir() if d.is_dir() and d.name not in exclude]

            if not subdirs:
                break  # 더 이상 하위 폴더 없음

            # 하위 폴더 선택 박스
            selected = st.selectbox(
                f"{current_dir} 하위 폴더 선택 (depth {depth})",
                options=["(선택 안함)"] + [d.name for d in subdirs],
                key=f"dir_select_{depth}"
            )

            if selected == "(선택 안함)":
                break

            # 선택된 폴더로 이동 후 다음 루프에서 계속 탐색
            current_dir = current_dir / selected
            depth += 1

    # 최종적으로 도달한 폴더 표시 + 파일 리스트
    st.markdown(f"**선택된 최종 경로:** `{current_dir}`")

    files = [p.name for p in current_dir.iterdir() if p.is_file()]
    if not files:
        st.info("파일이 없습니다.")
    else:
        st.write("### 📄 파일 목록")
        for f in sorted(files):
            st.write(f"- {f}")

def footer_note():
    st.caption(
        "설명: notion/ 루트의 MD와 동일 접두(제목 + 공백 + 긴식별번호)를 갖는 이미지 폴더를 찾아 "
        "선택한 카테고리 폴더(notion/<카테고리>/)로 함께 이동합니다. "
        "파일명/폴더명은 변경하지 않습니다."
    )
    st.divider()


# ------------------------------------------------
# 엔트리 포인트
# ------------------------------------------------
def main():
    setup_page()
    study_root, notion_root = sidebar_settings()
    if not study_root or not notion_root:
        return
    sidebar_show_categories(notion_root)
    sidebar_category_create(notion_root)
    main_md_mover(notion_root)
    footer_note()
    ui_browse_category_files_with_branch(study_root, notion_root)
    ui_dir_checker_recursive()

if __name__ == "__main__":
    main()
