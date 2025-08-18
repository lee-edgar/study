# 12.6. Interploation

대표적인 interploation 기법

1. Nearest-neighbborhood
2. Linear
3. Cubic

![스크린샷 2025-06-28 21.41.00.png](/assets/의료인공지능/12_6_Interploation/image_1.png)

(타겟값 1.3)

1. Nearest-neighborhood의 경우 1과 2 사이의 좀 더 가까운 1에 해당하는 intenstity값을 가져오는 걸 말합니다.
2. Linear : 1과 2의 값들을  모두 고려하고, linear하게 중간의 값을 채택하기때문에, 좀 더 영상이 스무스하게 변화됩니다. 1의 intensity 10과 2의 intensity 50사이의 30정도의 값을 가지게 됩니다.
3. Cubic : ***0~3값을 포함하여 고려하여 3차 다항식의 곡선으로 만들어 타겟 값 추정방식.*** 
Linear보다 더 스무스한 영상 변화. 1과 2의 값 이전, 이후 값들인 0과 3을 포함하여 함께 고려하여 값을 결정해줍니다. 곡선을 에스터메이션하고 곡선을 만들수 있는 3차 다항식을 만들고 타겟값인 1.3을 넣어서 타겟값에 대한 intensity값을 최종 정의합니다

linear interpolation은 1차원에 대한 표현, bilinear는 2차원, trilinear는 3차원.

### Bilinear interpolation

![스크린샷 2025-06-28 22.13.50.png](/assets/의료인공지능/12_6_Interploation/image_3.png)

2차원이라서 2개의 축이고, 4개의 점(q11, q12, q21, q22)을 고려합니다. P값은 변환된 곳을 말합니다.

x축으로 봤을때, x1과 x2 사이의 x이며, 비율을 바탕 비중치를 각각 주어 값을 줄 수 있습니다.

![스크린샷 2025-06-28 22.10.06.png](/assets/의료인공지능/12_6_Interploation/image_2.png)

- X축 기준 x는 x1에 가깝기 때문에 y2에서의 Q22보다 Q12에 더 많은 비중치,
- X축 기준 x는 x1에 가깝기 때문에 y1에서의 Q21보다 Q11에 더 많은 비중치.

### Bicubic Interpolation

![스크린샷 2025-06-28 22.14.53.png](/assets/의료인공지능/12_6_Interploation/image_4.png)

Bilinear에서는 Q11, Q12, Q21, Q22 총 4개의 점을 고려했습니다. Bicubic에서는 좀 더 확장된 값으로, 16개의 점을 고려하여 최종적으로 가운데의 값을 정의하게 됩니다.  

![스크린샷 2025-06-28 23.01.34.png](/assets/의료인공지능/12_6_Interploation/image_5.png)

cubic은 곡선에 대한 식을 정의해야하는데, a값을 정의해주게 되면 곡선을 정의 할 수 있겠습니다.

x1, y1을 0, x2, y2를 1이라고 하고, 해당 식을 푼다고 가정하면 밝기값을 얻을 수 있습니다.

P(0,0), P(0,1), P(1,0), P(1,1). 점에 대한 4개의 식을 구할 수 있습니다.

![스크린샷 2025-06-28 23.05.35.png](/assets/의료인공지능/12_6_Interploation/image_6.png)

이러한 방식으로 모든 값들을 구하면, 밝기 값을 구할 수 있습니다.