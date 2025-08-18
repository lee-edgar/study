# 12.3. Transformation Matrix in 2D

트랜스포메이션은 정도에 따라서 몇 가지로 나뉘게 됩니다.

변환 모델의 종류

- Rigid(강체) : 회전+이동(의료 영상 뼈 구조)
- Similarity : 강체 + 스케일
- Affine : 전단(shear)  까지 허용
- Projective(투영) : 원근 왜곡 보정
- Non-rigid/Deformable : 스플라인,

매칭 전략

- feature-base : 코너, 엣지, 해부학적 랜드마크
- Intensity-base : 상호정보, SSD, NCC
- Hybrid : 둘을 결합하여 견고성 및 정확성 향상

최적화 & 안정화

- Multi-resolution pyramid : 전체 영상→세부 영역 순으로 정합해 국소 최적화 회피
- Regularization : 지나친 번형 억제( 특히 비강체 정합에서 중요함)
- Convergence criteria : 변환 파라미터 변화량, 반복 수, 잔차 에러 임계치

결과 평가

- 정량적 지표  : MSE, Dice coefficient(분할 라벨 정합 시), Target Registration Error(TRE)

변환이 어디까지, 어느 정도 까지 진행되었는지에 따라서, 트랜스포메이션들을 아래와 같이 나눌 수 있겠습니다.

![스크린샷 2025-06-25 15.56.59.png](/assets/의료인공지능/12_3_Transformation_Matrix_in_2D/스크린샷_2025-06-25_15.56.59.png)

1. Rigid transformation : rotation과 translation만 고려.
2. Similarity transformation : rotation + translation + scaling
    - 여기서의 scaling 이란 전체적으로 영상이 같은 비율로 작아지거나, 확장 되는 것
3. Affine transformation :
    - scaling 비율이 맞춰져서 축소되거나 확장되지 않고, 예를 들어 가로만 축소되고 세로는 그대로 유지되는 경우(스케일 x방향과 y방향이 다른)
4. projective transformation(Homography)
    - 보통의 affine transformation에서는 변의 평행성이 유지가 되는데, projective transformation에서는 변의 평행성도 없어 질 수 있습니다.

보통의 의료 영상 분석에서는 Rigid transformation, Similarity transformation, affine transformation이 주로 사용 됩니다.

### Transformation

![스크린샷 2025-06-25 17.52.36.png](/assets/의료인공지능/12_3_Transformation_Matrix_in_2D/스크린샷_2025-06-25_17.52.36.png)

1. translation
    - x방향으로 t만큼, tx만큼 이동을 했고, y방향으로 ty만큼 이동했음을 위 수식으로 표현
2. rotation

예시로 (1,0)을 90도 로테이션 시켰다고 가정. cos세타, sin세타에 각각 90값을 넣어 주게 되면

- -sin90 → -1
- cos 90 → 0.
- sin 90 → 1
- cos 90 → 0

(1,0)에서 90도 변환 값을 주어 (0,1)의 결과를 만들어 내는 것을 볼 수 있음.

1. scaling
    - x방향, y방향이 같은 비율로 스케일 되는걸 가정.
    - x방향으로 스케일링 되는 비율과 y방향으로 스케일링 되는 비율을 바꾸고 싶다면, s→sx, sy로 정도를 조정 할 수 있습니다.
2. shear
    - 식에서의 0과 감마 부분을 변화시켜주면, 영상이 그 만큼 기울어진 영상을 얻을 수 있습니다.

### rotation과 translation을 고려하는 rigid변환.

![스크린샷 2025-06-25 18.03.17.png](/assets/의료인공지능/12_3_Transformation_Matrix_in_2D/스크린샷_2025-06-25_18.03.17.png)

- (x’, y’) = (cos$\theta$, -sin$\theta$, sin$\theta$,cos$\theta$)(x,y) + (tx, ty)의 값들을 찾아주게 되면 rigid 변환 식을 구할 수 있습니다.

### 추가로, 여기에 Similarity transformation을 적용해본다면,

![스크린샷 2025-06-25 18.12.12.png](/assets/의료인공지능/12_3_Transformation_Matrix_in_2D/스크린샷_2025-06-25_18.12.12.png)

Similarity transformation는 rotation + translation + scaling의 조합이므로, scaling = (s,0,0,s)식이 고려가 되기 때문에, (s,0,0,s) matrix를 곱해주게 됩니다. 

좀 더 정리된 식으로 보자면 아래와 같습니다.

![스크린샷 2025-06-25 18.13.08.png](/assets/의료인공지능/12_3_Transformation_Matrix_in_2D/스크린샷_2025-06-25_18.13.08.png)

각각의 $\theta$값들과 tx, ty값들을 찾게 되면, similarity transformation의 파라미터 값들을 찾을 수 있습니다.

## Pseudo Inverse[sú:dou]

각각의 $\theta$값들과 tx, ty값들을 찾기 위한 파라미터를 얻을 수 있습니다.

matrix를 다시 표현 해보자면 (x’, y’)은 아래와 같습니다. 

![스크린샷 2025-06-25 20.05.57.png](/assets/의료인공지능/12_3_Transformation_Matrix_in_2D/스크린샷_2025-06-25_20.05.57.png)

위 슬라이드 내용에 의해서

                                                            a = Scos $\theta$, b = Ssin $\theta$

풀어 써 본다면,

                                                           x’ = ax - by + c 

                                                           y’ = bx + ay + d

우리가 구해야하는 값 martix(a, b, c, d)이고,

### 아핀 변환

x’ = ax - by + c,     y’ = bx + ay + d 식을 아래와 같이 아핀 변환을 통해 표현 할 수 있습니다.

![스크린샷 2025-06-25 20.21.52.png](/assets/의료인공지능/12_3_Transformation_Matrix_in_2D/스크린샷_2025-06-25_20.21.52.png)

- x’ 해석 : ax, by순서이기에, a, b값을 제외하고,  x, -y가 들어오고, c값이 있으니 1, d 값이 없으니 0
- y’해석 : bx + ay의 순서로 따지면, ay + by가 될 것이기때문에, y +x가 들어오고, c값0,  d값 1

아래 식은 하나의 점(x1, y1)만을 고려를 한 상태입니다.  

                                                           x’ = ax - by + c 

                                                           y’ = bx + ay + d

사실은 (x1, y1)이 변환되는 (x1’, y1’)을 찾아야 되며, 하나의점이 아니라 여러개의 점을 찾는 경우, 아래의 값들을 찾아야 하며,

                                                       (x1,y1) → (x1’, y1’)

                                                       (x2,y2) → (x2’, y2’)

                                                                     .

                                                                     .

                                                                     .

찾아야 하는 값들이 여러개로 증가 했기에 아래 식처럼 추가 되겠습니다.  (*두 점에 대한 네개의 식)

![스크린샷 2025-06-25 20.35.31.png](/assets/의료인공지능/12_3_Transformation_Matrix_in_2D/스크린샷_2025-06-25_20.35.31.png)

4개의 식 결과로 4x4 matrix가 되고, vector도 (x1’, y1’, x2’, y2’)과 같은 형태가 도리 것이고, 이 식을 만족하는 a, b, c, d값을 구할 수 있습니다.

식의 형태를 생각해본다면

                                                          Ax = B

A가 matrix, x는 우리가 구해야하는 파라미터, B가 우측의 벡터이며, 이것이 ***전형적인 선형 연립 방정식*** 풀이 문제라고 할 수 있습니다.

A의 역함수가 존재하면, A역함수 양 옆에 곱을해서, 아래와 같이 풀어 낼 수 있습니다. (A의 역함수를 통해 x = A-1 * B)

![스크린샷 2025-06-25 20.50.42.png](/assets/의료인공지능/12_3_Transformation_Matrix_in_2D/스크린샷_2025-06-25_20.50.42.png)

그런데, 매칭 점들이 많아지게 되면 A값이 정방행렬이 아니게 되고 역행렬을 구할 수 없게 되는데, 이러한 문제를 풀기 위한 방식이 Pseudo Inverse입니다. Pseudo Inverse로 풀게 되면, 이 x 값을 구한다고 한들, 모든 A,B에 이 식이 만족하게 할 수는 없지만, 근사적으로 이 두 값을 비슷하게끔 만들어주는 X를 찾아주게 되는 것입니다.

- ***Pesudo-Inverse 설명 과정에서 아핀변환을 사용한 이유?***
    
    ![스크린샷 2025-06-26 21.37.30.png](/assets/의료인공지능/12_3_Transformation_Matrix_in_2D/스크린샷_2025-06-26_21.37.30.png)
    
    ![스크린샷 2025-06-26 21.37.41.png](/assets/의료인공지능/12_3_Transformation_Matrix_in_2D/스크린샷_2025-06-26_21.37.41.png)