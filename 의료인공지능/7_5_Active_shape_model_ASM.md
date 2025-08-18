# 7.5. Active shape model.ASM

Active shape Model은 learning 기반입니다.

![image.png](/assets/의료인공지능/7_5_Active_shape_model_ASM/image.png)

Test는 위와 같으며,

![image.png](/assets/의료인공지능/7_5_Active_shape_model_ASM/image_1.png)

Training에서 각 Shape들이 존재하고, Landmark들이 각각  존재하게 됩니다.

v1, v2 ,,, vn개의 landmark들이 존재하게 되고, 두번째 shape에서도 첫 번째 shape과 매치되는 landmark들이 존재하게 됩니다.

![image.png](/assets/의료인공지능/7_5_Active_shape_model_ASM/image_2.png)

Training 단계에서는 여러 개의 shape에 대해 landmark들을 수집합니다.

각 shape마다 동일한 위치의 landmark들이 존재하며, 예를 들어 첫 번째 landmark에 대해서는 $v_1^1 \sim v_1^m$ 처럼 m개의 subject에서 수집됩니다.

이처럼 각각의  landmark 위치들($v_1^1 \sim v_1^m$, $v_2^1 \sim v_2^m$, $v_3^1 \sim v_3^m$)에 대해 분포를 관찰 할 수 있으며, 이를 통해 각 점이 이동할 수 있는 범위(분포)를 학습하는 것이 Active Shape Model의 핵심 아이디어입니다.

![image.png](/assets/의료인공지능/7_5_Active_shape_model_ASM/image_3.png)

실제 테스트 할때 Shape는 어떻게 사용하느냐?

Active Contour처럼 boundary만 보고 점(포인트)의 이동 방향을 정할수 있지만, 이 경우 로컬 최소점(local minima)에 빠져 비정상적인 shape이 생성 될 수 있습니다. 

이를 보완하기 위해, Training 시 학습한 landmark 분포를 기반으로 shape 변화가 분포 내에 있으면 허용하고, 분포 밖에 벗어나는 변화는 제한하는 것이 Active Shape Model(ASM)의 핵심이 됩니다.

1. Training 해놓은 분포를 바탕으로 boundary shape가 비슷하다면 변화를 허용합니다.
2. training 해놓은 분포와 다르게 이동방향을 잡고 이동한다면 제한합니다.

따라서, 중요한 건 landmark 분포의 변화를 어떻게 학습하느냐이며, 이를 위해 PCA를 사용하게 됩니다.

![image.png](/assets/의료인공지능/7_5_Active_shape_model_ASM/image_4.png)

![image.png](/assets/의료인공지능/7_5_Active_shape_model_ASM/image_5.png)

PCA 과정을 그림으로 표현.

1. 각 landmark들의 일치하는 n번째 포인트매칭해줍니다.
2. 이후 각 shape들을 중심점에 모이게 alignement(정렬)해줍니다.

포인트 매칭 된 landmark들의 포인트 간 거리가 먼 경우 변화가 큰 구간이 있고, 상대적으로 포인트 간 거리가 짧가 변화가 낮은 구간을 찾는 등의 변화량을 확인합니다.

학습 수행 단계(수학적으로)

![image.png](/assets/의료인공지능/7_5_Active_shape_model_ASM/image_6.png)

위 이미지에 대한 단계별 설명

1. 평균 벡터 계산
- 각 subject(환자)의 벡터 xix^ixi의 평균을 구함
- 예: 영상마다 landmark가 10개 있고 2D 위치(x, y)를 가진다면 → 20차원 벡터

---

1. 평균 제거(중심화)
- 각 벡터에서 평균을 빼줌 → 데이터의 중심을 원점으로 이동시킴

---

1. 공분산 행렬 계산
- 차원 간 상관관계를 담은 20×20 행렬 생성

---

1. 고유벡터, 고유값 계산
- SVD 또는 고유값 분해를 통해 eigenvector(축), eigenvalue(분산량) 획득

---

1. 주요 축 선택
- 모든 축(20개) 중 상위 몇 개(예: 3~5개)를 선택 → 주성분 축
- 정보 손실을 최소화하면서 차원을 줄임

---

1. 주성분 계수 계산
- 선택한 주성분 축으로 데이터를 투영하여 좌표값 획득

---

1. 중심화된 데이터 복원
- 주성분 좌표를 다시 원래 공간으로 변환 (중심화 상태)

---

1. 원래 데이터 복원
- 평균을 다시 더해 원래 위치로 복원 (근사 복원)

Active Shape Model

![image.png](/assets/의료인공지능/7_5_Active_shape_model_ASM/image_7.png)

20차원 평균을 시각화 한 것임(정확하진 않아 보임)

![image.png](/assets/의료인공지능/7_5_Active_shape_model_ASM/image_8.png)

- 학습 과정의 절차

![image.png](/assets/의료인공지능/7_5_Active_shape_model_ASM/image_9.png)

min shape(X 바)으로 부터 이동하고자 하는 boundary 확률이 높은 곳으로 포인트들을 이동시켜줌.

하단 포인트와 같이 포인트의 이동이 잘못 되는 경우도 있음

![image.png](/assets/의료인공지능/7_5_Active_shape_model_ASM/image_10.png)

위 포인트들의 모임 값 Y와 min shape(X bar)을 이용해 b값을 구하고, b값을 통해 복원을 수행하면 최종 변화된 x값을 구할 수 있음.

![image.png](/assets/의료인공지능/7_5_Active_shape_model_ASM/image_11.png)

![image.png](/assets/의료인공지능/7_5_Active_shape_model_ASM/image_12.png)

b값을 바탕으로 복원된 값을 더하기 때문에 우측 사진과 같은 심한 변화들은 불가능해지게 됨.

![image.png](/assets/의료인공지능/7_5_Active_shape_model_ASM/image_13.png)

이 사진과 같이 가능한 변화

쉐입의 분포로 보았을때 가능한 변화이기에 위(안쪽)쪽으로 이동될 확률이 높다는 것임.