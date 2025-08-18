# 8.2. U-net

### Fully Convolutional Networks

![image.png](/assets/의료인공지능/8_2_U-net/image.png)

유의미한 특징들을 잡아주기 위해서 Convolutional layer와 fulling layer를 사용합니다.

fulling을 할수록 특징 맵의 사이즈는 줄어들고 리셉티드 필드에 의해 한 점이 나타내는 범위가 넓어지면서 넓은 영역의 주요 특징들을 바탕으로 classification을 잘해주게 되지만. 

반대로 해상도가 낮아짐에 따라 정확한 segmetation에는 안좋은 영향을 미치게 됩니다. 따라서 Upsampling을 진행해야 합니다.

upsampling

![image.png](/assets/의료인공지능/8_2_U-net/image_1.png)

영상을 크게 해주는 작업을 말합니다.

### 가장 가까운 값을 가져오는 Nearest Neighborhood.

![image.png](/assets/의료인공지능/8_2_U-net/image_2.png)

역방향 매핑은 output의 픽셀 위치는 1/scale로 나눠 input 포인트를 구한 뒤, 그 실수 좌표와 가장 가까운 input 픽셀(정수 좌표)의 값을 가져오는 방식을 말합니다.

예를 들어, output의 (1,1)은 input의(0.5, 0.5)에 대응되며, 가장 가까운 input의 (1,1)이 선택이 됩니다.

예시의 과정 : input 2x2 → 2배 upsampling → output 4x4 → (역방향 전환)output 4x4의 1,1 → 1/2 sampling → input 2x2의 0.5, 0.5에 대응되며, 가장 가까운 input(1,1) 선택

Nearest Neighbor Upsampling에서는 순방향 매핑도 가능하나 보통은 역방향 매핑이 일반적이고 안전한 방식임. 순방향 매핑은 정확히 일치 하지 않으면 일부 위치를 채우지 못하는 경우가 발생함.

### Linear interpolation

![image.png](/assets/의료인공지능/8_2_U-net/image_3.png)

좌표와 좌표의 값을 보고 값을 정의해주는 것인데, 예를 들어, (1,1), (1,2)의 좌표 값인 1,2를 사용하고,그 중간 값으로 처리 →  0.5(1+2)

### Unpooling

![image.png](/assets/의료인공지능/8_2_U-net/image_4.png)

점진적으로 downsampling 후 upsampling.

Deconvoluation 개념 : pooling 위치를 저장하고 upsampling할때 사용하며, 해당 위치 제외하고 모두 0값으로 처리함.

input에 영상을 넣고, deconvoluation을 통한 Unpooling 후 output에 label prediction하고 실제 label과 비교하고 cost를 정의하여 파라미터들을 학습하는 end-to-end방식.

### Transposed Convoluation

![image.png](/assets/의료인공지능/8_2_U-net/image_5.png)

(윗 부분) 3x3 커널과 4x4 input을 이용해 2x2 output을 만들어냄.

(아랫 부분) matrix 포맷으로 변경할수 잇는데

1. input을 flatten하게 늘려서 16x1로 만들고, 
2. output을 4x1에 대응 할 수 있게 끔 kernel로 부터 4x16으로 풀어 써줍니다.
3. kernel로 부터 풀어쓴 4x16부분을 자세히 보자면,, 
    1. 첫 번째 줄(Y0)
        1. 4x4input에 3x3 kernel을 적용 할때의 첫 번째를 보면 X0, X1, X2는 kernel적용이 되지만 X3는 적용이 안되는 모습이라서, 4x16부분을 보면, W0,3부분은 0으로 표기가 된 모습을 볼 수 있음.
        2. 4x4 input에 3x3 kernel을 적용 된 첫 번째에 의해 X12, X13, X14, X15역시 적용이 안되어서 0값으로 표기.
    2. 두 번째줄 (Y1)
        1. 3x3 kernel이 4x4input에서 한 칸 우측으로 이동한 결과를 보여줌.

Kernel의 Transpose. T 

Kernel matrix의 transpose와 output(y)에 의해

![image.png](/assets/의료인공지능/8_2_U-net/image_6.png)

kernel matrix(T) * output = Input으로 순서를 바꾼 식을 표현 할 수 있음.

- kernel matirx의 transpose * output vector(y) = input(16x1)

결과는 4x4 형태로 reshape로 가정한다면, 위 과정을 통해 2x2 크기의 output으로 부터 4x4 크기의 입력을 재구성하게 된 것이며 이는 결과적으로 upsampling 효과를 가진다.

![image.png](/assets/의료인공지능/8_2_U-net/image_7.png)

위 과정을 그림으로 표현하자면,

2x2의 영상(feature map)을 4x4영상(feature map)으로 만들고자 한다

padding을 추가하여 6x6으로 만들고  3x3 convoluation을 통해 4x4의 결과가 된다.

### U-Net

![image.png](/assets/의료인공지능/8_2_U-net/image_8.png)

FCN과 거의 비슷한 구조를 가지고

작아진 어떠한 feature map으로 부터 transposed convolution 기법을 사용해 사이즈를 다시 늘려주게 됩니다. deconvolution이라고도 합니다.

![image.png](/assets/의료인공지능/8_2_U-net/image_9.png)

늘려준 사이즈는 우측 파란색으로 표시를 하고, 추가로 기존에서 작아지면 내려온 피쳐를 좌측에 붙혀 그대로 사용합니다.

> FCN과 왜 비슷하다고 하나요?
→ FCN에서도 업샘플링을하고, 이전 풀링에서 사용했던 피쳐맵을 그대로 같이 사용합니다.
> 

사이즈를 늘려준 피처와 기존에 작아지면서 내려온 피쳐를 같이 붙히고 → convoluation → convoluation → transposed convolution에서 살펴보았던 filter를 학습해 크기를 키우게 됨.

이번에도 마찬가지로 추가로 feature map을 가져와 컴펙트네이션을 해주고, 다시 convolution → convolution

위와 같은 방식으로 최종적으로 prediction을 하고, prediction과 실제 y값을 차이를 바탕으로 다시 gradient descent합니다.

upsampling을 한번에 크게 하는 것보다 점진적으로 특징맵 사이즈를 크게 해주는 필터들을 학습했을때, Segmentation이 종종 좋아지는것을 확인할 수 있었습니다.