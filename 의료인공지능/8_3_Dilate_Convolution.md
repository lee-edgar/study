# 8.3. Dilate Convolution

> Dilate Convolution은 다운 샘플링 없이 Receptive Field를 넓히는 기술.
> 
1. Downsampling 
    - Receptive Filed(수용 영역)를 넓히기 위해 사용하지만,
    - 위치 정보 손실이 발생함(픽셀 해상도가 줄어들기 때문)
2. Upsampling
    - Downsampling에서 잃은 공간 정보를 복원하려고 사용하지만,
    - 완벽한 복원이 어렵고 노이즈나 왜곡이 생기기 마련

Dilate Convolution을 사용하면 ?

- Receptive Filed를 넓히면서도 Downsampling을 하지 않기 때문에, 연산량 증가 없이 더 넓은 문맥 정보를 얻는 동시에 공간 해상도(위치 정보)도 그대로 유지 할 수 있음.

![스크린샷 2025-06-04 15.36.24.png](/assets/의료인공지능/8_3_Dilate_Convolution/스크린샷_2025-06-04_15.36.24.png)

Dilated Convolution : 

기존의 방법에서는 3x3의 filter가 커버하는 영역은 원본 input의 3x3인데, 공백 사이사이를 띄어두고 convooution을 수행하게 되면 5x5영역을 확인하게 됩니다.

w1*x1 + w2*x3 + x3*x5 … 의 수식을 가지게 됨.

늘어난 빈 공간 사이를 인터폴레이션 해줄 수 있고, 

가장 가까운 값을 가져올 수 있는데 가장 가까운 값을 가져오면 rough한 결과가 얻어지게 됩니다.

반면에, 

1. Dilated Convolution을 하게 되면 빈 공간을 만든 필터를 계산하면서 이미지를 위에서 아래로 훝으면서 prediction을 수행 할 수 있습니다. 
2. 그 결과로 clear한 prediction map을 얻을 수 있습니다. 
3. 이후 prediction결과와 y값과의 비교를 통해 의network의 parameter들을 update하게 됩니다.

![스크린샷 2025-06-04 15.54.58.png](/assets/의료인공지능/8_3_Dilate_Convolution/스크린샷_2025-06-04_15.54.58.png)

1. FCN, U-Net에서 확인 했듯이 pooling을 여러번 사용한 다음에 다시 upsampling을 해주는 방식 대신에 
2. Dilated Convolution을 이용하게 되면 upsampling, downsampling을 할 필요 없이 해상도를 유지 할 수 있습니다.
    - 해상도를 유지하는데 실제 학습해주는 filter의 내부의 parameter의 수는 변함이 없이 receptive field가 넓어질 뿐입니다. 이러한 구조를 DeepLab이라고 합니다.
    - Atrous convolution의 rate값들을 변경하여 receptive field를 변경 할 수 있습니다.
        
        ![스크린샷 2025-06-04 16.33.30.png](/assets/의료인공지능/8_3_Dilate_Convolution/스크린샷_2025-06-04_16.33.30.png)
        
        예를 들어, rate를 3으로 하여, 빈공간 빈공간 필터값 빈공간 빈공간 필터값 .. 
        

### DeepLab V3.

![image.png](/assets/의료인공지능/8_3_Dilate_Convolution/image.png)

1. Convolution과 Pool를 사용하는 ResNet구조를 사용 →
2. Block3이후에 여러개의 Dilate Convolution과 Image Pooling Concat →
3. 1x1 convolution하여 최종 prediction.
4. 최종prediction(16)에서 upsampling을 하고, y값과 비교하여 loss를 구해 파라미터를 업데이트함.

*output stride는 input 영상에 비해서 feature map이 얼마나 줄었는지를 나타내는것을 의미함(4,8,16배 줄어들었음 의미)

좀 더 상세히 구조 요약

1. Backbone : Resnet with atrous convolution
    - resnet을 backbone로 사용하며, resnet의 block3 이후부터는 stride를 제거하고 dilation rate를 적용해 해상도 유지 + recaptive filed 확대를 동시에 이룸
2. ASPP(atrous spatial pyramid pooling)
    - block4의 출력에 대해 여러 dilation rate를 사용한 Dilate Convolution 병렬 연산.
    - image-level pooling 할 때, concat하여 다양한 스케일의 문맥 정보를 수집함.
3. 1x1 Convoluation → 예측 결과 생성
    - concat된 feature들을 1x1 conv를 통해 차원 축소 및 클래스 수만큼 출력(feature map) 생성
4. Upsampling 후 Loss 계산
    - 예측결과 bilinear upsampling 등으로 원본 크기로 복원
    - 원본 GT와 비교하여 loss 계산 및 Backprogation 수행함