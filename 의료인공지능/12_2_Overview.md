# 12.2. Overview

레스트레이션이 수행되는 전체적인 과정 설펴보기.

![스크린샷 2025-06-25 14.04.17.png](/assets/의료인공지능/12_2_Overview/image.png)

- 왼쪽의 이미지를 moving image, source image라고 하며,
- 오른쪽의 이미지를 fixed image, target image라고 합니다.

두 영상을 보면 아마도, “이 왼쪽 영상을 시계방향으로 로테이션 시키면 오른쪽과 잘 맞을 거야”라고 생각을 할 수 있습니다. 직관적으로 그런 판단을 어떻게 내릴 수 있는지 좀 더 세분화 해서 생각을 해볼수 있습니다. 
세분화 한 것들을 컴퓨터로 구현 한 것을 레지스트레이션 이라고 할 수 있겠습니다.

![스크린샷 2025-06-25 14.12.42.png](/assets/의료인공지능/12_2_Overview/image_1.png)

왼쪽 영상에 x1, y1 오른쪽 영상에 ,x1’, y1’ 있다고 가정합니다.

x1,y1에서 x1’, y1’으로 변형을 할 수 있습니다. 식으로 작성하면 아래와 같습니다.

![스크린샷 2025-06-25 14.14.19.png](/assets/의료인공지능/12_2_Overview/image_2.png)

- 어떤 matrix (a, c, d b)를 곱할 수 있고, 어떤 특정 값(e, f)들을 더 해줄 수 있습니다.
- x1, y1자리에 x2,y2, x3, y3값들이 들어올 수 있고, x1’, y1’에 x2’, y2’ 등이 들어올 수 있겠습니다.

각각의 파라미터(a,c,d,b)를 찾아 주게 되면 정합을 수행할 수 있습니다.

풀어 써보 자면,

![스크린샷 2025-06-25 14.38.52.png](/assets/의료인공지능/12_2_Overview/image_4.png)

                                       x1’ = ax1 + by1 + e ,  y1’ = cx1 + dy1 + f

다시 매트릭스로 표현해보자면, 

![스크린샷 2025-06-25 14.38.22.png](/assets/의료인공지능/12_2_Overview/image_3.png)

- x1’, y1’과 같은 여러 점들의 매칭을 해주는 이러한 트랜스포메이션 매트릭스를 구하게 됩니다.
- 트랜스포메이션 매트릭스를 바탕으로 이제는 이 무빙 이미지의 모든 점들을 변형 시킬 수 있습니다.

즉, 모든 점들의 변형을 시켜 주게 되면, 좌측의 영상에서 우측의 영성과 같이 변형을 할 수 있습니다.

### 정리

![스크린샷 2025-06-25 14.50.09.png](/assets/의료인공지능/12_2_Overview/image_5.png)

1. fine correspondences :
    - 먼저 correspondence 대응점를 찾아줘야합니다.
        - 우선 왼쪽의 (x1,y1)이 오른쪽의 (x1’, y1’)과 짝이 된다는 것을 식별해야합니다.
        - 위 과정을 통해 매칭(SIFT, SUFR 혹은 의학 영상 특화 마커)이나, 수작업으로 레이블링 하여 구현합니다.
2. Estimate transformation matrix :
    - 찾아진 점들을 바탕으로 위 식에서의 a,b,c,d,e,f 와 같은 값들을 찾아줘서 transformation matrix를 찾게 됩니다.
    - 확보된 대응점 쌍을 바탕으로, 아핀변환 파라미터(a,d,c,d,e,f)를 구합니다.
    - 이때, 최소제곱 방법을 쓰거나, 이상치에 강한 RANSAC를 기법을 적용 할 수도 있습니다.
3. Transform the moving image : 
    - 찾아진 transformation matrix를 바탕으로 무빙 이미지를 transform을 시키게 됩니다.
    - 새로 생긴 비정형 그리드에 픽셀 값을 입힐 때는 Nearest, Linear, Cubic 등 보간(interploation) 기법을 써야 해상도 저하 현상을 막을 수 있습니다.

변환 모델의 종류

- Rigid(강체) : 회전+이동(의료 영상 뼈 구조)
- Similarity : 강체 + 스케일
- Affine : 전단(shear)  까지 허용
- Projective(투영) : 원근 왜곡 보정
- Non-rigid/Deformable : 스플라인,

매칭 전략

- featrue-base : 코너, 엣지, 해부학적 랜드마크
- Intensity-base : 상호정보, SSD, NCC
- Hybrid : 둘을 결합하여 견고성 및 정확성 향상

최적화 & 안정화

- Multi-resolution pyramid : 전체 영상→세부 영역 순으로 정합해 국소 최적화 회피
- Regularization : 지나친 번형 억제( 특히 비강체 정합에서 중요함)
- Convergence criteria : 변환 파라미터 변화량, 반복 수, 잔차 에러 임계치

결과 평가

- 정량적 지표  : MSE, Dice coefficient(분할 라벨 정합 시), Target Registration Error(TRE)