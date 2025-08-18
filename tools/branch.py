#!/usr/bin/env python3
# study/tools/study_notions_manager.py
import re
import shutil
from pathlib import Path
from typing import Optional
from urllib.parse import unquote, quote

# 이미지 링크 패턴: ![alt](path)
IMG_LINK_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

def list_categories(notion_root: Path):
    """notion/<카테고리> 디렉토리 목록"""
    return sorted([d for d in notion_root.iterdir() if d.is_dir()])

def list_category_mds(notion_root: Path, category: str):
    """특정 카테고리 안의 .md 목록"""
    cat_dir = notion_root / category
    return sorted(cat_dir.glob("*.md")) if cat_dir.exists() else []

def _rewrite_md_links_to_assets(md_text: str, old_dir_names: list[str], new_assets_rel: str) -> str:
    """
    MD 내 이미지 링크를 new_assets_rel/파일명 으로 치환.
    - old_dir_names: MD가 참조하던 (제목 폴더명 등) 기존 상위 폴더명들
    - new_assets_rel: 'assets/<category>/<title>' 같은 최종 상대 경로(앞에 'assets/' 포함)
    """
    from urllib.parse import quote, unquote
    import re
    IMG_LINK_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

    # URL 인코딩/비인코딩 모두 허용
    candidates = set()
    for d in old_dir_names:
        d_norm = d.strip("/").replace("\\", "/")
        candidates.add(d_norm)
        candidates.add(quote(d_norm))  # 공백 → %20 등

    def repl(m):
        alt, path = m.group(1), m.group(2)
        decoded = unquote(path).lstrip("./").replace("\\", "/")
        for c in candidates:
            if decoded == c:  # 폴더만 참조
                return f"![{alt}]({new_assets_rel})"
            if decoded.startswith(c + "/"):
                fname = decoded[len(c):].lstrip("/")
                return f"![{alt}]({new_assets_rel}/{fname})"
        return m.group(0)

    return IMG_LINK_RE.sub(repl, md_text)


def _move_images_flat(src_dir: Path, dst_dir: Path):
    """
    src_dir 하위 모든 파일을 dst_dir로 '파일명 그대로' 평탄화 이동.
    동일 파일명 존재 시 덮어씀. 끝나면 빈 디렉토리 정리 후 src_dir 제거 시도.
    """
    dst_dir.mkdir(parents=True, exist_ok=True)
    for p in list(src_dir.rglob("*")):
        if p.is_file():
            target = dst_dir / p.name
            if target.exists():
                target.unlink()
            shutil.move(str(p), str(target))
    # 빈 폴더 정리
    for sub in sorted(src_dir.rglob("*"), reverse=True):
        if sub.is_dir():
            try:
                sub.rmdir()
            except OSError:
                pass
    try:
        src_dir.rmdir()
    except OSError:
        pass

def process_one_md_in_category(
    md_path: Path,
    category: str,
    study_root: Path,
    notion_root: Optional[Path] = None,
    assets_root: Optional[Path] = None,
) -> Path:
    """
    - 이미지 폴더: md.stem 과 동일한 폴더명 가정(식별코드 제거 완료 상태)
    - MD 내부 이미지 링크: assets/<category>/<title>/파일명 으로 치환  ✅ (문서별 하위 폴더)
    - 이미지: study/assets/<category>/<title>/ 로 평탄화 이동  ✅
    - MD: study/<category>/ 로 이동 (파일명은 md.stem + '.md')
    """
    from urllib.parse import unquote
    import re

    study_root = study_root.resolve()
    notion_root = notion_root.resolve() if notion_root else study_root / "notion"
    assets_root = assets_root.resolve() if assets_root else study_root / "assets"

    title = md_path.stem
    cat_dir = md_path.parent  # notion/<category>

    # 이미지 폴더: 기본은 제목과 동일
    img_dir_main = cat_dir / title

    # 백업 후보: MD 안 첫 이미지 링크의 상위 폴더명(혹시 폴더명이 다른 경우)
    IMG_LINK_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    alt_img_dir = None
    text_probe = md_path.read_text(encoding="utf-8")
    m = IMG_LINK_RE.search(text_probe)
    if m:
        probed = unquote(m.group(2)).lstrip("./").replace("\\", "/")
        parent_name = probed.split("/", 1)[0] if "/" in probed else probed
        if parent_name and parent_name != title:
            alt_img_dir = cat_dir / parent_name

    # 링크 치환 준비
    old_names = []
    if img_dir_main.is_dir(): old_names.append(img_dir_main.name)
    if alt_img_dir and alt_img_dir.is_dir(): old_names.append(alt_img_dir.name)

    # ✅ 최종 링크 prefix: assets/<category>/<title>
    new_assets_rel = f"assets/{category}/{title}"

    # 링크 치환
    new_text = _rewrite_md_links_to_assets(
        md_text=text_probe,
        old_dir_names=old_names,
        new_assets_rel=new_assets_rel
    ) if old_names else text_probe

    # ✅ 이미지 이동: assets/<category>/<title>/ 로 평탄화
    dst_images = assets_root / category / title
    dst_images.mkdir(parents=True, exist_ok=True)
    if img_dir_main.is_dir():
        _move_images_flat(img_dir_main, dst_images)
    elif alt_img_dir and alt_img_dir.is_dir():
        _move_images_flat(alt_img_dir, dst_images)
    # 없으면 스킵

    # MD 이동 (study/<category>/제목.md)
    dst_dir = study_root / category
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst_md = dst_dir / f"{title}.md"

    # 내용 업데이트 후 이동
    md_path.write_text(new_text, encoding="utf-8")
    if dst_md.exists():
        dst_md.unlink()
    shutil.move(str(md_path), str(dst_md))
    return dst_md


def branch_category(category: str, study_root: Path):
    """
    분기 실행(카테고리 전체):
    - 입력: category (예: '의료인공지능'), study_root (예: Path('./study'))
    - 동작: study/notion/<category>/ 의 모든 .md에 대해 process_one_md_in_category 수행
    """
    study_root = study_root.resolve()
    notion_root = study_root / "notion"
    assets_root = study_root / "assets"

    cat_dir = notion_root / category
    if not cat_dir.exists():
        raise FileNotFoundError(f"카테고리 폴더가 없습니다: {cat_dir}")
    assets_root.mkdir(exist_ok=True)

    mds = sorted(cat_dir.glob("*.md"))
    for md in mds:
        process_one_md_in_category(
            md_path=md,
            category=category,
            study_root=study_root,
            notion_root=notion_root,
            assets_root=assets_root,
        )
