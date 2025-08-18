# 11.7. Enhancement metric

영상을 만들어냈을때 그 영상의 퀄리티가 좋은지 안 좋은지 평가를 어떻게 할 수 있는지 살펴보겠습니다.

# PSNR. Peak Signal to Noise Ratio

![스크린샷 2025-06-25 09.42.53.png](/assets/의료인공지능/11_7_Enhancement_metric/image.png)

prediction 영상과, ground truth 영상의 비교를 측정합니다.

이때 각 픽셀에 대해 MSE를 구하게 됩니다.

## 개요

- *PSNR(Peak Signal-to-Noise Ratio)**은 원본 이미지와 복원 또는 향상된 이미지 간의 차이를 평가하는 대표적인 **정량적 지표**로, 특히 **Super-resolution, Denoising, Compression** 등에서 널리 사용됨.

### 직관적 해석

- 높은 PSNR → MSE가 작다 → 두 영상이 거의 동일하다
- 낮은 PSNR → MSE가 크다 → 차이가 크다
- 일반적으로
    - 30 ~ 40 db 이상 : 사람 눈에는 거의 차이 못 느낌
    - 20 ~ 30 db : 약간 티남
    - 20 db 이하 : 뚜렷한 화질 열화

## 세부 설명

### 1. 정의

- PSNR은 MSE(Mean Squared Error, 평균 제곱 오차)를 기반으로 계산되는 지표이며, 단위는 decibel (dB)을 사용.
- 일반적으로 PSNR 값이 **높을수록** 향상된 이미지가 원본과 **가깝다**는 것을 의미.

### 2. 의료 인공지능에서의 활용

의료 영상 분야에서 PSNR은 다음과 같은 이미지 복원 및 향상 문제에 주로 활용됩니다

1. 저선량 CT(Low-dose CT → Normal-Dose CT)
    - 목적 : 환자의 방사선 노출을 줄이기 위해 저선량으로 촬영한 CT 영상을 고선량 품질로 복원
    - PSNR 사용 : 복원된 영상이 고선량 CT와 얼마나 유사한지를 객관적 수치로 평가
2. Super Resolution in MRI/CT
    - 문제 : 낮은 해상도의 의료 이미지를 고해상도로 향상
    - PSNR 활용 : 향상된 이미지가 원본 고해상도 이미지와 얼마나 유사한지 평가
3. Denoising (잡음 제거)
    - 문제 : MRI나 초음파 영상 등에서 발생하는 노이즈 제거
    - PSNR 활용 : 노이즈 제거 후 영상이 얼마나 원본과 가까운지 평가
4. Compression Artifact Removal
    - JPEG, JPEG2000 등으로 압축된 의료영상의 화질 저하를 복원하는 모델의 성능 측정

### 3. 코드

```python
import cv2
import numpy as np
import math

# 원본 이미지와 복원된 이미지 불러오기 (흑백 가정)
original = cv2.imread('original.png', cv2.IMREAD_GRAYSCALE)
enhanced = cv2.imread('enhanced.png', cv2.IMREAD_GRAYSCALE)

# MSE 계산
mse = np.mean((original - enhanced) ** 2)

# PSNR 계산
if mse == 0:
    psnr = float('inf')
else:
    PIXEL_MAX = 255.0
    psnr = 10 * math.log10((PIXEL_MAX ** 2) / mse)

print(f'PSNR: {psnr:.2f} dB')

```

### 4. 결론

- PSNR은 의료 영상 향상, 복원, 초해상도, 노이즈 제거 등의 성능을 객관적 수치로 측정하는데 중요한 지표임.
- 그러니, 인간의 시각적 판단을 반영하지 않기에, 실제 임상 적용을 위해 SSIM 등 다른 지표와 병행 사용이 필요함
- PSNR은 기본적인 성능 평가 지표로서 의료 인공지능의 영상 품질 향상 과제에서 기초적이면서도 필수적인 척도입니다.

# SSIM. Structural Similarity Index

사람 시각의 구조 지각을 모사해, 두 영상 간 유사도를 계산하는 화질 평가 지표. PSNR처럼 단순한 픽셀 오차가 아니라, 밝기.대비.구조(패턴)의 유사성을 종하뱋 측정하기 때문에, 주관적 품질과 더 잘 일치합니다.

### 1. SSIM의 기본 개념

목표 : 원본 영상 x와 처리된 영상 y가 얼마나 구조적으로 비슷한가를 0~1 사이 값으로 평가.

- 1에 가까울 수록 거의 동일한 구조
- 0에 가까울 수록 완전히 다름

창(윈도우) 기반 :

- 영상을 작은 블록(예, 11x11 윈도우)으로 나누고, 각 블록별 SSIM을 계산한 뒤 평균

# 2. 의료 영상 인공지능에서의 SSIM 활용

1. 의료 영상 복원/향상 평가
    - Super resolution, denoising, deblurring 모델의 결과를 평가할 때 SSIM을 사용하여 병변의 형태, 경계선 등 구조 보존 여부를 평가.
    - 특히, PSNR은 높은데 SSIM이 낮은 경우, 실제로는 시각적으로 중요한 구조가 문너진 경우가 많음
2. 저선량 CT 영상 향상
    - 저선량 CT에서 고선량 CT로 변환 시, SSIM을 통해 미세 구조(혈관, 종양)가 유지되었는지 확인
3. MRI 노이즈 제거, 압축 복원 등
    - 구조 손실 없이 복원이 되었는지를 SSIM으로 측정
    - PSNR이 보장되지 않더라도 SSIM이 높다면 시각적으로 우수한 결과일 수 있음

# 3. 코드

```python
from skimage.metrics import structural_similarity as ssim
import cv2

# 흑백 이미지 로딩
original = cv2.imread('original.png', cv2.IMREAD_GRAYSCALE)
enhanced = cv2.imread('enhanced.png', cv2.IMREAD_GRAYSCALE)

# SSIM 계산
ssim_value = ssim(original, enhanced)
print(f'SSIM: {ssim_value:.4f}')

```

### 요약

> SSIM은 밝기, 대비, 구조 세 축으로 두영상으로 비교해 인간이 느끼는 품질과 더 잘 맞는 지표.
특히 의료 영상처럼 조직 경계, 미세 구조 보존이 중요한 분야에서 PSNR만으로 놓칠 수 있는 차이를 잡아주는 핵심 평가 도구.
> 

### PSRN vs. SSIM

| 항목 | PSNR | SSIM |
| --- | --- | --- |
| 기준 | 픽셀 단위 오차 | 구조적 유사도 |
| 단위 | dB | 0 ~ 1 (무단위) |
| 시각적 민감도 | 낮음 | 높음 (시각 구조 반영) |
| 의료영상 적합성 | 낮은 구조 평가 정확도 | **높은 구조 보존 평가 가능** |

# MOS. Mean Opinion Score

ground truth가 없더라도 prediction 영상을 여러 사람들에게 보고, 여러 사람들이 1 ~ 5 점까지의 점수를 매기게 되고, 그 여러 점수에 대한 평균.

### MOS의 한계점 및 보완 필요성

| 한계점 | 설명 |
| --- | --- |
| 주관적 편향 존재 | 사람마다 기준이 다르므로 MOS의 신뢰도에 변동성 있음 |
| 반복성(reproducibility) 낮음 | 동일한 평가 환경을 구성하기 어려움 |
| 시간/비용 많이 듦 | 평가자 섭외, 실험 환경 구성, 통계 분석 필요 |
| 표본 수가 적으면 불안정함 | 최소 20명 이상 권장됨 |

보통 PSNR, SSIM과 같은 정량 지표와 병행 사용

---

영상의 퀄리티를 확인하기 위해 PSNR, SSIM을 주로 사용하며 

PSRN이 높다고 해서 꼭 퀄리티가 좋다고 말할 수 없다고 하는 논문들이 꽤나 있다고하며, 실제 퀄리티를 증명하기 위해 실제 사람이 평가하는 Mean Opinion Score을 이용해 볼 수 있습니다.

Resnet SR보다 Gan SR이 사림이 보기에 더 좋은 퀄리티를 준다고 판단 할 수 있구요