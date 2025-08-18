# 11.1. SRCNN. Super Resolution CNN

딥러닝을 이용한 Image Enhancement 기법.

1. 이미지 해상도를 높여주는 Super resolution 문제에 처음 end-to-end CNN 구조를 이용한 RCNN기법 확인.
2. 이후에 위 구조를 발전시킨 여러 기법들에 대해서 살펴볼 예정.
3. 영상 퀄리티를 향상 시킨 후 성능평가 방법.

# 기존 딕셔너리학습 ↔ SRCNN

딕셔너리 학습 기법

1. 입력 패치 하나를 저해상도 사전(LR dictionary)의 원소들로 표현(representatiion)
2. 그 계수를 바탕으로 고해상도 사전(High resolution dictionary)의 원소를 섞어 복원(Reconstruction)
3. L1 정규화(희호성) + 관측값과의 차이 최소화라는 최적화 문제를 푸는 흐름

SRCNN

1. interpolation(보통 바이 큐빅)으로 low resolution → high resolution 크기 맞추기
2. Conv1(represetntation) : 패치를 여러 개의 필터로 쏴서 특징 맵(feature map) 생성
3. Conv2(non-linear mapping) : 특징 맵 간의 비선형 조합으로 High resolution 패치 표현 학습
4. conv3(reconstruction) : 다시 채널을 합쳐 최종 픽셀값 예측

전체를 end-to-end로 학습 한다는 점이, 이전 딕셔너리 방법과 다른 가장 큰 변화임

# Super-Resolution using CNN

![스크린샷 2025-06-19 14.46.29.png](/assets/의료인공지능/11_1_SRCNN_Super_Resolution_CNN/image.png)

low resolution의 dictonary에 알파값을 찾아주었고, 옵져베이션 Y를 빼서 데이터 fitting trerm이 되게 하고, 람다 값에 l1 norm값을 더해주고, 이 값들을 미니마이제이션 하는 알파 값을 찾는 것.

알파 값을 찾게 되면 알파값들은 쉐어 할 수 있고, high resolution에 의해 값을 복원 할 수 있음

이때, (low resolution dictonary + alpha), (옵저베이션 Y)의 각각의 feature를 뽑아서 data fitting term을 비교함.

영상에서 옵져베이션 Y에 대한 feature를 먼저 뽑고, dictionary learning(low resolution dictionary + alpha)으로 복원된 피쳐를 뽑아서 둘 간의 관계를 학습을 했었습니다.

뽑힌 피쳐들을 바탕으로 어떠한 매핑을 하게 되고(얻어낸 알파값으로 이런 피쳐들에 대한 매핑)

1. 리프레진테이션 단계
    - LR 패치를 어떤 특징맵(feature map)들의 조합으로 나타내기 위해,
    - 전통적으로 D low resolution과 알파를 사용하지만, CNN의 첫 번째 컨볼루션 레이어가 이 역할을 대신 수행
2. 비선형 Non-Linear mapping 단계
    - 얻어낸 알파를 바탕으로 low resolution 특징을 high resolution 특징으로 바꾸는 과정.
    - 전통적으로 딕셔너리 두 개를 연게하지만, CNN에서는 두 번째 컨볼루션 레이어가 비선형 매핑을 담당합니다.
3. Reconstruction단계
    - 여러 패치로 부터 복원된 값들로 부터 최종 영상을 만들어냄.
    - 어떤 패치로 부터 추정된 엑스트메이션 값들로 부터 리컨스터럭션  하기에 CNN 대체 가능
    - High resoltuion 특징 벡터들을 모아 최종 픽셀 값을 예측하는 과정임.
    - 전톡적으로는 D high reslolution에 알파를 더하는 방식이고, CNN에서는 세 번째 컨볼루션 레이어가 이 역할을 수행해 최종 고해상도 영상을 만들어냄

간단 요약

1. Low resolution 패치 → 컨볼루션 → 특징벡터(representation)
2. 특징 벡터 → 컨볼루션 → high resolution 특징 벡터(non-linear mapping)
3. High resolution → 컨볼루션 → HR 패치(reconstruction)

### 구조를 자세히 들여다보자

![스크린샷 2025-06-19 14.54.35.png](/assets/의료인공지능/11_1_SRCNN_Super_Resolution_CNN/image_2.png)

구조를 보면 상당히 간단한 CNN.

1. (input에서 다음 단계 까지의 그림) : input이 있고, input에 대해서 filter를 쓰게 되면 feature에 의해 feature map들이 생성됨 → 전통적인 과정에서 봤을때, 피처를 추출하고, 패치를 리프레젠테이션 하는 부분이라고 할 수 있습니다.

1. (input 이후 단계 부터 그 다음 단계) :  CNN을 사용해서 원바이원 컨볼루션을 쓰기도 하고, 5바이5를 써서 실험들을 진행하기도 했습니다. 이 과정에서 어떤 conv net에 의해 feature map들이 나오게 됨.

1. (최종 단계) : CNN의 어떠한 계산들로 인해 최종적으로 output을 만들어주는 and to and로 계산되는 resolution 기법을 제안함

![스크린샷 2025-06-19 15.07.14.png](/assets/의료인공지능/11_1_SRCNN_Super_Resolution_CNN/image_3.png)

low resolution 영상은 high resolution 영상의 해상도를 1/2, 1/4로 줄이게 되어 작아진 영상을 바이 큐빅 인터폴레이션, 바이 리니어 인터폴레이션으로 크게 인터폴레이션 하게 되면 사이즈가 기존의 하이 레졸루션 영상과 같아지게 됩니다. 같아진 사이즈로 부터 high resoltuion 영상을 만들어 내는 기법을 제안하였습니다.

이 논문에서는 cnn을 사용함으로서 기존의 딕셔너리 러닝 기반 방법을 좀 더 제네럴라이제이션 할 수 있는(일반화 할 수 있는) 방법을 제시했다고 주장하고, 그러한 분석들을 본문에 포함하고 있음. 구조는 간단하지만 최초로 슈퍼 레졸루션 문제의 딥러닝을 적용했다는 부분에 의의를 두고 있음

# 중간에 왜 인터폴레이션을 사용하나?

- SRCNN 당시는 CNN만으로 크기 자체르 바꾸는(upsampling) 모듈이 일반화 되기 전이라서, 바이큐빅을 이용해 크기를 올리고, 해상도를 개선했음

간단 요약

1. Low resolution 패치 → 컨볼루션 → 특징벡터(representation)
2. 특징 벡터 → 컨볼루션 → high resolution 특징 벡터(non-linear mapping)
3. High resolution → 컨볼루션 → HR 패치(reconstruction)
4. 

> SRCNN은 딕셔너리 학습의 3단계(표현→매핑→복원)를 3개의 합성곱 층으로 바꿔, 크기 맞추기(interpolation) 이후에 한번에 학습하도록 한 최초의 end-to-end CNN 기법.
>