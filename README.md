# knowledge-branch

이 레포는 본인이 **노션(Notion)에 정리한 공부 자료를 GitHub에 손쉽게 업로드**하기 위해 만든 공간입니다.  

노션에서 export한 **마크다운(.md)과 이미지**를 자동으로 정리해주는 스크립트(`tools/branch.py`, `study_notions_manager.py`)를 직접 작성하여, 자료를 **카테고리별로 깔끔하게 관리**할 수 있도록 했습니다.  

공부 기록을 모아둔 **개인 아카이브**이자, 필요할 때 검색해 참고할 수 있는 공간입니다.  

# 의료인공지능 : 컴퓨터비전_머신러닝_딥러닝을 이용한 의료영상분석(DGIST 로봇및기계전자공학과 박상현 교수)
* 3.1. Property of Deep Nerual Network
* 3.2. Convolution
* 3.2. Convolution
* 4.1. Overall procedure
* 5.1. Feature Selection Using L1 regularizationß
* 5.2. Feature selection using Entropy / Mutual information
* 5.3. Feature extracting using Deep Learning
* 5.4. Class Activation Map
* 5.5. Weekly Supervised Learning
* 5.6. Multiple Instance Learning
* 6.1. Introduction to medical image segmentation
* 6.2. Otsu thresholding
* 6.3. Morphological processing(dilation, ersion)
* 6.4. Region growing / Watershed algorithm
* 7.1. Active Contour Model
* 7.2. Atlas based method
* 7.3. Segmentation via learning based method
* 7.4. Principle Component Analysis(PCA) NP
* 7.5. Active shape model.ASM
* 7.6. Segmentation using classififer
* 8.2. U-net
* 8.3. Dilate Convolution
* 8.4. DeepLab V3
* 8.5. Segmentation using 3D CNN
* 8.6. Loss Function
* 8.7. Segmentation Metric
## Enhancement
* 9.1. Introduction to medical image enhancement
* 9.2. Intensity normalization
* 9.3. Histogram Equalization
* 9.4. Histogram Matching
* 9.5~7 Spatial Filtering, Anistropic diffusion filtering, Vessel enhancement filtering
* 10.1. Filtering in frequency domain
* 10.4. Non-Local Mean de noising
* 10.5. Denoising with Dictionary
* 10.6. Dictonary Learning
* 10.7. Super-resolution via dictionary learning
* 11.1. SRCNN. Super Resolution CNN
* 11.2. Upsampling strategy
* 11.3. Deep network for super resolution
* 11.4. Generative Adversarial Network 
* 11.6. CNN for medical image enhancement컴퓨터비전_머신러닝_딥러닝을 이용한 의료영상분석2
* 11.7. Enhancement metric
## Registartion(정합)
* 12.1. Introuduction to medical image registration
* 12.2. Overview
* 12.3. Transformation Matrix in 2D
* 12.5. Backward warping
* 12.6. Interploation
* 12.7. Similarity measure ? SSD SAD NCC
* 12.8. Similarity measure ? Mutual information
* 13.1. Registration types
* 13.2. Registration using main axis
* 13.4. Nonrigid registration via ICP
* 13.5. Nonrigid Registration via B-spline
* 13.6. Nonrigid registration via deformable model
* 14.1. Optical flow / FlowNet
* 14.4. Spatial Transformer Network


## Notion <-> GitHub 스크립트 설명
### branch.py : 
역할: 분기(branch) 처리 핵심 로직 모듈  

기능:  
- 노션에서 export한 `.md` 파일과 이미지 폴더 인식  
- 파일명 끝의 **식별 코드 제거** 및 **공백 → `_` 변환**  
- `.md` 내부 이미지 링크를 `study/assets/<카테고리>/...` 형태로 자동 수정  
- 이미지 파일을 **평탄화(flat)** 하여 카테고리별 자산 폴더로 이동  

### study_notions_manager.py : 
역할: Streamlit 기반의 UI 관리 도구  

기능:
- 노션 루트(`notion/`)에서 `.md` 파일 불러오기 및 카테고리별 분류  
- 원하는 카테고리를 선택하여 파일 **이동** 또는 **분기 실행**  
- 카테고리 내부의 `.md` / 이미지 파일 현황을 **웹 UI에서 확인**  
- `branch.py`의 함수를 호출해 실제 처리를 실행  
