# 12.5. Backward warping

![스크린샷 2025-06-28 10.58.03.png](/assets/의료인공지능/12_5_Backward_warping/image.png)

![스크린샷 2025-06-28 10.58.40.png](/assets/의료인공지능/12_5_Backward_warping/image_2.png)

![스크린샷 2025-06-28 11.23.08.png](/assets/의료인공지능/12_5_Backward_warping/image_3.png)

- 2x2 는 선형 변환(회전, 스케일, 전단) 만 다루기에, 이동에 대한 부분은 덧셈이 추가적으로 필요합니다.
    - 호모지니어스 좌표(homogeneous coordinates) : 2D 점(x,y)를 (x, y, 1)로 확장하여, 3x3 행렬로 만들어 “선형 + 이동”을 모두 처리.
- 호모지니어스(3차원) 좌표 + 3x3 matrix 한 번의 곱으로 “선형+이동” 을 깔끔하게 처리하려면 마지막 행을 [0 0 1]로 고정해야합니다. 즉 h1 = 0, h2 = 0, h3 = 1을 두어,
    
    w’ = h1x, h2y, h3w를 구해주게 됩니다.
    

## Backward Warping

Backward warping(역방향 워핑)은 이미지 변환 기술 중 하나로, 출력 이미지의 각 픽셀에 대해 원본 이미지의 어느 위치에서 값을 가져와야 하는지 계산하는 방식입니다.

### Forward vs Backward Warping

- **Forward warping(순방향 워핑)**: 원본 이미지의 각 픽셀을 변환하여 출력 이미지의 어느 위치에 놓을지 결정합니다.
    - 원본 이미지의 픽셀이 출력 이미지에서 정확히 픽셀 위치에 매핑되지 않을 수 있어 홀(holes)이나 중복(overlaps)이 발생할 수 있습니다.
    - 구현이 복잡하고 결과 이미지에 artifacts가 생길 수 있습니다.
- **Backward warping(역방향 워핑)**: 출력 이미지의 각 픽셀에 대해 원본 이미지의 어느 위치에서 샘플링할지 결정합니다.
    - 출력 이미지의 모든 픽셀이 채워지므로 홀이 발생하지 않습니다.
    - 원본 이미지의 위치가 정확한 픽셀 위치가 아닐 수 있으므로 보간(interpolation)이 필요합니다.
    - 구현이 더 간단하고 효율적이며, 일반적으로 더 나은 결과를 제공합니다.

### Backward Warping 과정

- 출력 이미지의 각 픽셀 위치 (x', y')에 대해:
- 역변환 행렬(inverse transformation matrix)을 사용하여 원본 이미지의 대응 위치 (x, y)를 계산합니다.
- 계산된 위치 (x, y)가 원본 이미지 경계 내에 있는지 확인합니다.
- 원본 이미지에서 해당 위치의 픽셀 값을 보간하여 출력 이미지의 (x', y') 위치에 할당합니다.

### 보간 방법(Interpolation Methods)

- **최근접 이웃 보간(Nearest neighbor interpolation)**: 가장 가까운 픽셀 값을 사용합니다. 계산이 빠르지만 결과 이미지가 울퉁불퉁할 수 있습니다.
- **이중 선형 보간(Bilinear interpolation)**: 주변 4개 픽셀의 가중 평균을 사용합니다. 더 부드러운 결과를 제공합니다.
- **이중 3차 보간(Bicubic interpolation)**: 주변 16개 픽셀을 사용하여 더 정확한 보간을 수행합니다. 가장 부드러운 결과를 제공하지만 계산 비용이 더 높습니다.

### 장점

- 홀(holes)이나 중복(overlaps) 문제가 없습니다.
- 구현이 더 간단하고 효율적입니다.
- 보간 방법을 통해 결과 품질을 조절할 수 있습니다.

### 응용 분야

- 이미지 리사이징(resizing)
- 이미지 회전(rotation)
- 이미지 왜곡(distortion)
- 파노라마 스티칭(panorama stitching)
- 이미지 렌더링(rendering)

![스크린샷 2025-06-28 20.23.46.png](/assets/의료인공지능/12_5_Backward_warping/image_4.png)

forward warping : 특정 영역 (3,1)좌표에 hole 문제가 발생함

- vector에 1,1입력 → transform matrix * vector=(1.1, 1.3, 1) → 가장 가까운 좌표 1, 1 → forward warping하여 1,1 좌표에 위치
- vector에 2,1입력 → transform matrix * vector=(2.3, 1.4, 1) → 가장 가까운 좌표 2, 1 → forward warping하여 2,1 좌표에 위치
- ***vector에 3,1입력 → transform matrix * vector=(3.6, 1.4, 1) → 가장 가까운 좌표 4, 1 → forward warping하여 4,1 좌표에 위치하게 됩니다. 이때, (3, 1)의 좌표의 영역이 hole으로 비어지게 되는 현상이 생기고 문제가 발생합니다.***

forward warping을 하게 되면, 특정 영역 (3,1)좌표에 hole 문제가 발생하기 때문에 backward warping으로 처리를 해야합니다.

backward warping은 transform matrix의 역함수를 구하게 됩니다.

역함수*프라임의 좌표(=타겟에서의 좌표)를 이용해 어떤 좌표의 값이 될 것 인지 알아 낼 수 있습니다.

어떤 좌표의 intensitic 값을 다시, 프라임의 값으로 가져오게 됩니다

다시말해 froward warping은 vector에 값을 순차적으로 넣어주게 되고, vetctor*matrix의 값과 가장 가까운 값의 좌표를 생성합니다.

하지만 backward warping은 matrix의 역함수 * 타겟좌표의 값을 넣어 주기 때문에 (3,1)과 (4,1)의 중복된 값이 있긴하지만, forward warping처럼 3,1의 자리를 hole로 두진 않습니다.

---

forward warping(순방향 변형)

$$
(x′,y′)=H(x,y,1)T
$$

                             원본 화소 좌표 (x, y)에 대해 계산하고, 가장 가까운 정수 좌표를 사용합니다.

- (1, 1) → (1.1, 1.3) → 가장 가까운 (1,1)
- (2, 1) → (2.3, 1.4) → 가장 가까운(2,1)
- (3, 1) → (3.6, 1.4) → 가장 가까운(4,1) ← 이렇게 되면
(3,1) 자리에는 아무 화소도 할당되지 않아 빈 칸(hole) 발생

backward warping(역방향 변형)

$$
(x,y,1)T=H^{-1}(x′,y′,1)T
$$

1. 목표 영상의 픽셀 (x’, y’)에 대해 계산하고, 원본 영상의 (비정수) 좌표(x,y)를 찾아냅니다.
2. 그 좌표에서 보간(interpolation)을 통해 픽셀 값을 샘플링
3. 결과
- (3,1)에도 역방향으로 계싼하면 원본의 어딘가 (3.1, 0.8)의 같은 위치기 나오므로
- 보간으로 값을 채우기 때문에 구멍 없이 모든 픽셀에 값이 할당됩니다.

정리

forward warping : “원본→ 목표”로 쏴 주다 보니 일부 좌표에 hole이 생기게 됨

backward warping : “목표→원본”으로 역계산 해서 값을 가져오니 누락 없이 모두 채워진다.

---