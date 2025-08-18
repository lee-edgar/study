# 9.4. Histogram Matching

![image.png](/assets/의료인공지능/9_4_Histogram_Matching/image.png)

좌측의 어두운 값이 많은 히스토그램을 우측의 밝은 값이 많은 히스토그램으로 변형 해주는 것이 목적임.

![image.png](/assets/의료인공지능/9_4_Histogram_Matching/image_1.png)

Histogram Equalization과 비슷하나, source distribution을 target distribution으로 누적분포(CDF)로 변형하는 것이 목적. 

![image.png](/assets/의료인공지능/9_4_Histogram_Matching/image_2.png)

source

![image.png](/assets/의료인공지능/9_4_Histogram_Matching/image_3.png)

target

- source, target에 대해서 각각 좌측은 일반 분포, 우측은 누적분포(CDF)
- 예를 들어, soruce의 CDF(0) 0.19값과 가장 비슷한 target CDF(3) 0.15에 대응시키는 것.
- soruce CDF(4) 0.89는 traget CDF(6) 0.85와 대응

![image.png](/assets/의료인공지능/9_4_Histogram_Matching/image_4.png)

좌측표는 위에서 대응되는 값들을 나타낸 것임.

좌측 표) 왼쪽 끝은 soruce CDF, 우측 끝은 target CDF임.

target에 맞게 분포를 matching시키면 target 분푸와 비슷하게 되는 모습을 그래프를 통해 확인 할 수 있음.