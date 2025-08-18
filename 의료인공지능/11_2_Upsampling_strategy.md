# 11.2. Upsampling strategy

![image](/assets/의료인공지능/11_2_Upsampling_strategy/image_3.png)

처음 row resolution은 작았을 것이고, 바이 리니어 혹은 바이 큐빅 인터폴레이션을 통해 영상의 사이즈를 키워, 인풋과 아웃풋의 크기를 동일하게 매치시켜줍니다. 

위 과정에서 두 가지 문제가 발생합니다.

1. row resolution에서 upsampling하는 과정에서 발생하는 문제.
2. 큰 피쳐맵에 대한 컨볼루션을 수행해야하기에, computation 코스트가 큰 문제

위 두 문제를 해결 하기 위해 논문을 제안한 저자들의 해결책

- ***작은 사이즈에서 곧 바로 컨볼루션 레이어를 통과시키는 기법을 제안***합니다. 그렇게 되면 자연스럽게 피처맵의 사이즈가 작게 될 것이고, 같은 computation이라고 하면, 더 많은 CNN을 사용할 수 있다고 주장

마지막에는 동일한 크기의 high resolution 영상을 얻어야 하기에, 마지막 부분에서 업샘플링을 할 수 있는 convolution을 사용하게 됩니다. 여기서는 transpose convolution을 사용하게 됩니다.

# Fast SRCNN(SRCNN의 속도 한계를 극복하기 위해 제안)

배경 및 동기

SRCNN은 먼저 바이큐빅으로 크기를 증가하고, 3개 conv층의 구조를 가짐.

- 속도 측면에서 interpolation 연산과 커다란 feature 맵을 처리하는데 병목이 발생

FSRCNN

1. 학습 가능한 업샘플링(deconvolution)으로 interpolation 대체
2. 채널 수 축소/확대(shrinking & expanding) 단계 도입
3. 매핑(mapping) 층 수 조절을 통해 연산량 대폭 절감.

→ SRCNN 대비 40배 이상 빠른 실시간 처리 가능

![스크린샷 2025-06-19 18.34.59.png](/assets/의료인공지능/11_2_Upsampling_strategy/image_1.png)

작은 사이즈로 부터 CNN을 수행하고 마지막 부분에서 transpose convolution을 수행하게 되면서 사이즈가 커지게 됩니다. 이러한 방식을 사용하기에 동일한 compution 타입으로 더 깊은 컨볼루션 레이어를 많이 사용 할 수 있다고 하며, 성능을 향상 시킨 논문입니다.

> FSRCNN은 low resolution에서 연산 → 학습 가능한 업샘플링 구조로 SRCNN의 연산 병목을 제거해 40배 빠른 슈퍼해상도를 달성한 모델.
* 빠른 속도와 비교 가능한 품질을 모두 잡고 싶다면 FSRCNN
* 그 위에 더 높은 화질이 필요하다면 후속모델(ESPCN, VDSR 등)을 고려
> 

# Sub-Pixel CNN

SRCNN/FSRCNN 이후 습관처럼 크기를 증가(interpolation)시키고, CNN을 사용하는 대신, CNN 이후에 한 번에 업샘플링을 처리하는 방식입니다.

기존 방식의 문제 및 한계

1. 바이큐빅 interpolation으로 먼저 해상도를 키우게 되면
    - 연산량이 급격히 증가하고
    - 학습 가능한 부분이 적어 Super resolution이 제한됨
2. Deconvolution/Transpose Conv
    - 업샘플링까지 하나의 층에서 처리 가능하지만
    - checkerboard artifact(눌린 격자 무늬)문제
    - 연산 및 메모리 효율이 좋지못함.

sub-pixel cnn은 두 방식 모두 대체하면서 속도, 품질을 증가시키고, 아티팩트를 감소합니다.

> 1. 먼저 LR 해상도에서 CNN 연산을 하고,
2. 마지막 채널 수를 늘린 뒤 pixelshuffle로 한번에 해상도를 높이는 방식.
> 

![스크린샷 2025-06-19 19.57.10.png](/assets/의료인공지능/11_2_Upsampling_strategy/image_2.png)

1. 작은 해상도에서의 먼저 연산
    - (첫번째 ~ 두번째 그림)작은 사이즈로부터 계속해서 컨볼루션을 진행하고, 마지막 upsampling 단계에서 transpose convolution 대신에 다른 upsampling 기법을 사용합니다.
2. pixel shuffle
    - 3x3에서 6x6 으로 upsampling 하고 싶다고 했을 때 4개의 필터를 사용해 각각 feature map을 만든 후 첫 번째 4개의 숫자를 각 피처맵에서 가져오는 방식입니다. 각각의 feature map에서 같은 인덱스의 픽셀 하나씩 가져와 High Resolution격자의 네 칸(2x2블록)에 분산배치 하고, 순회 하면서 한 번에 업샘플링

# 단순 비교(속도 vs 화질 vs 아티팩트)

1. SRCNN
    - 가장 먼저 나온 end to end cnn 슈퍼 해상도
    - 하지만 크기를 높이기 위해 바이큐빅에 의존 → 처리해야할 feature map가 커지고 속도가 느려짐
2. FSRCNN
    - 학습 가능한 업샘플링(deconv)을 도입해 interpolation을 네트워크 안으로 옮기고,
    - Low resolution 크기에서 대부분 연산 → 속도, 메모리 효율 40배 개선
3. Sub-pixel CNN
    - deconv의 단점을 보완해, 마지막에 채널 ↔ 공간만 재배치(pix-shuffle)
    - 깨끗하고 빠른 업샘플링 → 실시간 비디오 SR에 적용 가능