# 3.2. Convolution

# 3.2. Convoluation

### Convoluation

![image.png](/assets/의료인공지능/3_2_Convolution/image.png)

- Image에 Filter를 입혀 Pixelwies multiplication and sum을 하여 값을 채워 넣음으로서 features map을 생성하는 것을 의미합니다.
- 원래는 filter flip을 하여 사용하지만 해당 설명에서는 correlation으로 처리함.
- filter의 특징에 따라서, 한쪽면을 어둡게 처리하기도 하고,   9에서 0으로 우측으로 넘어가는 과정에서 점점 어두워지는 효과를 만들어 낼 수도 있음.

![image.png](/assets/의료인공지능/3_2_Convolution/image_1.png)

CNN에서는 filter의 성질 학습을 통해 아래와 같이 여러 특징을 가진 feature map 구성을 이루게 된다. 

- 4번째 그림처럼 선명하게 처리
- 3번째 그림처럼 테두리를 강조
- 2번째 그림처럼 끝 부분을 흐리게 처리

# 3.3. Convoluation Neural Network(CNN)

### Convoluational Layer

![image.png](/assets/의료인공지능/3_2_Convolution/image_2.png)

RGB에 대한 입력 6x6x3과 3x3x3filter를 컨볼루션하게 되면 4x4x3의 feature map을 얻을 수 있게 학습을 진행함.

![image.png](/assets/의료인공지능/3_2_Convolution/image_3.png)

- 4x4x3의 feature map에서 다시 3x3x3 filter를 컨볼루션하게 되면 2x2x3 feature map을 학습을 통해 얻을 수 있음.

### Stride

![image.png](/assets/의료인공지능/3_2_Convolution/image_4.png)

- 몇 칸씩 건너뛸지를 결정하는 것이 stride hyperparameter임.
- 위는 stride가 1인 경우 / 아래는 stride가 2인 경우

### Padding

![image.png](/assets/의료인공지능/3_2_Convolution/image_5.png)

- 컨볼루션 연산을 하게 되면 아웃풋 사이즈가 인풋 사이즈 보다 작아지게되는데, padding을 설정하면, 사이즈가 줄어들지 않는 아웃풋을 만들어 낼 수 있음.

### Pooling Layer

![image.png](/assets/의료인공지능/3_2_Convolution/image_6.png)

- 이미지 사이즈를 줄일 수 있는 방법을 말함.
- 그림에서의 4x4 이미지를 2x2로 줄일 수 있는데, 최댓값을 뽑은 Max Pooling, 평균 값을 뽑는 Average Pooling 등이 있으나, 일반적으로 Max Pooling을 많이 사용함. → local 부분에서의 중요한 특징을 잘 표현해서 Classification 성능을 높인 다는 연구 결과가 있음.

### Fully Connected Layer

![image.png](/assets/의료인공지능/3_2_Convolution/image_7.png)

충분히 작아진 feature map값들에 대해 모든 layer의 weight들이 존재하도록 연결한 layer.

- feature map의 각각의 값들을 layer에 연결을 하게 되는데, 이때 bias도 추가를 해야함.
- 4x4x3 = 48 + biase = 49 parameters

위 사진에서는 6개의 layer에 각각 fully connected layer를 적용하니, 49 * 6(layer)가 됨.

최종적으로, fully connected layer 이후 predict를 하게 됨.

### CNN

![image.png](/assets/의료인공지능/3_2_Convolution/image_8.png)

입력 이미지를 3x3x3으로 가정 → 9개의 filter를 생성하여 9번의 conv연산 → 2x2 pooling(max pool, avg pool) → filter conv → pooling → fully connect layer → fully connect layer → predict → predict값과 y값의 error 비교 → back propagation

# 3.4. Advanced CNNs(LeNet_AlexNet_VGG)

### LeNet-5

![image.png](/assets/의료인공지능/3_2_Convolution/image_9.png)

conv → pool → conv → pool → fc → fc → softmax

- input : 흑백이미지. 32x32x1
- conv1 : 5x5x6 filter conv → 28x28x6
- pool1 : 28x28x6 → avg pooling2x2 → 14x14x6
- conv2 : 14x14x6 → 5x5x16filter conv → 10x10x16
- pool2 : 10x10x16 → avg pooling 2x2 → 5x5x16
- flatten : 5x5x16=400
- fc layer : fully connected layer (120 unit) → fully connected layer(84 unit)  → softmax(10classes)
    - fc1 : fully connected layer (120 unit)
    - fc2 : fully connected layer(84 unit)
    - fc3 : softmax(10classes)

> Conv 연산은 padding 없이 수행되어 feature map의 크기는 줄어들지만, 이후 layer에서 더 많은 필터를 사용하여 채널 수를 증가시켜 feature 표현력을 높임.
> 

### AelxNet

LeNet-5에 비해 이미지 사이즈가 커진것을 볼 수 있으며, 이미지 사이즈가 커졋기에 Stride를 4를 주게 됨.

처음으로 activation function에 ReLU 적용

![image.png](/assets/의료인공지능/3_2_Convolution/image_10.png)

Input(227×227×3) → Conv(11x11x96, s=4) → ReLU → Pool → Conv(5x5x256) → ReLU → Pool → Conv(3x3x384) → Conv(3x3x384) → Conv(3x3x256) → Pool → FC(4096) → FC(4096) → FC(1000) → Softmax

- input : 컬러 이미지. 227x227x3
- conv1 : 11x11x3 filter → 55x55x96
- pool1 : max pool 3x3, stride 2 → 27x27x96
- conv2 : 5x5xs256 filter → 27x27x256
- pool2 : max pool 3x3, stride 2 → 13x13x256
- conv3 : 3x3x384 filter → 13x13x384
- conv4 : 3x3x384 filter → 13x13x384
- conv5 : 3x3x256 filter → 13x13x256
- pool3 : max pool 3x3x256 → 6x6x256
- flatten :6x6x256 → 9216
- fc layer
    - fc1 : 9216→ 4096
    - fc2 : 4096 → 4096
    - fc3 : 4096 → 1000(ImageNet 수)
    - activation : ReLU + DropOut
- Softmax : 1000probabality

### VGG16

![image.png](/assets/의료인공지능/3_2_Convolution/image_11.png)