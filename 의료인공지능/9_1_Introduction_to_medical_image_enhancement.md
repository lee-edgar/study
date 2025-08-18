# 9.1. Introduction to medical image enhancement

> Image Enhancement(이미지 향상)은 이미지를 더 잘 보이게 만들기 위한 전처리 기법. 원본 이미지의 품질을 높여 시각적 정보나 분석에 유리하게 만드는 기술임. 의료 영상(MRI, CT, X-Ray)에서는 질병 부위를 더 명확히 보이게 하기 위해 사용함.
> 

![image.png](/assets/의료인공지능/9_1_Introduction_to_medical_image_enhancement/image.png)

Conventional methods

1. Normalization : 픽셀 단위, 복셀 단위 인텐시티(표준) 값으로 바꿔주는 기법
    1. Z-score 정규화(평균0, 표준편차1)
2. Histogram equalization : Histogram 변형을 통해 픽셀과 복셀의 인텐시티 값을 바꿔주는 기법
    1. 확장:CLAHE(지역 기반으로 contrast 제한하며 향상)
3. Filter : 어떤 filter를 정의하고, conv 하여 영상 특성 변형, 혹은 영상 도메인을 frequency 도메인으로 변경 후 필터링 수행하는 기법 등.
    1. Gaussian Filter → 노이즈 제거
    2. Median Filter → salt-and-pepper 잡음 제거
    3. sharpen filter → 경계 강조
    4. Frequency Domain Filtering → Fourier Transform 후 고/저주파 조절
4. Dictionary learning : 학습 된 딕셔너리 데이터를 바탕으로 영상의 퀄리티를 향상 시키는 기법.
    1. 고해상도 이미지의 작은 패치들을 작은 딕셔너리 형태로 학습하여, 저해상도 이미지를 조합으로 재구성. K-SVD. 데이터가 적은 상황에서 유용

Deep Learning methods

1. SRCNN : Dictionary learning 성질을 잘 반영해서 제안한 방법.
    1. 저해상도 이미지 입력 → 고해상도 이미지 출력
    2. patch extraction → non-linear mapping → reconstruction
2. GAN : 수퍼 레졸루션 이용한 메서드
    1. 생성자(generator)가 고해상도 이미지를 생성하고, 판별자(discriminator)는 진짜/가짜를 구분.
    2. 매우 고품질의 디테일 보존 가능(인공적인 아티팩트 줄이기)
    3. CT 영상의 저선량 → 고품질 변환
    4. MRI의 낮은 해상도 → 고해상도 복원