# 8.4. DeepLab V3+

### Depth-wise Separable Convolution

![image.png](/assets/의료인공지능/8_4_DeepLab_V3+/image.png)

기존 convolution은 모든 채널에 동시에 연산을 수행하기 때문에 3x3x3 = 27개의 파라미터를 사용.

반면, Depthwise Separable Convolution은 연산을 두 단계로 나눠서 진행함 → Depthwise(3x3x1=9parameters) + pointwise(1x1x3=3parameters) = 총 12개의 parameters

1. Depthwise Convolution(3x3x1)
    - 입력의 각 채널마다 독립적으로 3x3 필터를 적용
    - 즉, 채널 수 x 필터 크기 (3x3x1) 만큼만 연산 → 채널 간 정보를 섞지 않음.
    - 예로, 입력 채널이 3개면 3개의 3x3 필터 → 9 parameters
2. Pointwise Convolution(1x1x3)
    - 각 픽셀 위치에서 모든 채널을 조합하여 새로운 출력을 만듦.
    - 1x1 convolution을 통해 채널 간 정보를 학습.
    - 예로, 1x1 필터 하나당 3채널 입력 → 3 parameter

> Depthwise는 공간적 특징 추출,
Pointwise는 채널 간 정보 통합에 집중하는 구조
> 

Depth-wise Separable Convolution 장점
1. 파라미터 수 감소
2. 연산량 및 메모리 사용량 감소
3. 모델 경량화에 매우 효과적
4. 성능 저하 없이 효율 크게 향상 가능.
 → MobileNet, DeepLab v3+ 

U-Net 구조.

![image.png](/assets/의료인공지능/8_4_DeepLab_V3+/image_1.png)

U-Net : Enconder/Decoder 구조를 통해 점진적 upsampling시 결과 상향

1. Encoding : 이미지 사이즈를 줄여나가면서 유의미한 feature를 뽑아내는 작업(최하단)을 Encoding이라고 하며,
2. Decoding : 어떠한 추출된 정보(최하단으로 부터)로부터 원하는 어떤 값을 찾아내는 작업을 Decoding이라고 합니다.

![image.png](/assets/의료인공지능/8_4_DeepLab_V3+/image_2.png)

1. 1번째 Block에서 Low level의 어떠한 정보들을 가지고 옵니다.
2. 기존의 DeepLab v3구조의 prediction 결과(위쪽 이미지)를 4배 upsampling(아랫쪽 이미지)을 해줍니다.
3. 1번의 low level의 정보와 2번의 upsampling을 concat → 3x3 convolution → 4배 upsampling → prediction
4. 최종 prediction과 y 간의 loss를 구해 backpropagation

위쪽 파트를 Enconder, 아랫쪽 파트를 Decoder