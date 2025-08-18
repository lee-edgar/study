# 10.1. Filtering in frequency domain

Fourier transform 등을 통해 영상을 다른 도메인으로 변환 후 변화된 도메인에서 Filtering을 수행하는 방법이며, 학습을 통한 Noise 제거  및 해상도 증가하는 방법론임.

![image.png](/assets/의료인공지능/10_1_Filtering_in_frequency_domain/image.png)

frequency를 기반으로 cosine 함수를 통해 표현이 가능한데, 여러 개의 cos함수를 scalar값으로 곱함으로서 다양한 주파수의 표현이 가능함.

fourier transform을 사용하면 혼합된 주파수를 cos으로 분리가 가능하며, 역으로도 가능함.

2D Frequency Domain

![image.png](/assets/의료인공지능/10_1_Filtering_in_frequency_domain/image_1.png)

일정한 패턴을 가지고 있는 3개의 그림을 더해 줄 수 있습니다. 

![image.png](/assets/의료인공지능/10_1_Filtering_in_frequency_domain/image_2.png)

각각을 2D Fourier transform을 통해 주파수 영역으로 신호들을 바꿔줄 수 있습니다.

- 2번째 그림 High Frequency를 가지는 그림 패턴
- 3번째 그림 Low Frequency를 가지는 그림 패턴

각각을 더해준 영상으로 부터 특정 frequency가 큰 신호의 패턴을 없애기 위해 Convolution을 할 수 있는데, Convolution을 하기에는 상당히 어려움이 있습니다. 즉, 필터를 잘 만들어서 두 번째 영상의 패턴만을 날리기가 상당이 난이도가 높습니다.

그래서, 하단의 붉은색의 frequency domain으로 바꿔서 보게 되면, low frequency 신호와 high frequency 신호들을 구분할 수 있으며, 해당 부분을 없애주고, 남은 신호들만으로 복원을 하게 되면 원하는 패턴을 없애 줄 수 있습니다.

> 즉, frequency domain으로 변환 → 원하는 값 filterling → 다시 inverse Fourier transfrom으로 변환을 통해 효과적으로 noise 및 특정 패턴 제거.
> 

신호를 Visualize 할 때 Spectrum을 사용함.

High Frequency에서는 아주 작은 값, Low Frequency(주저줖)에서는 큰 값을 가짐. 영상으로 좋게 만들어 주기 위해 Log를 취해줍니다.

![image.png](/assets/의료인공지능/10_1_Filtering_in_frequency_domain/image_3.png)

- 2번째 식은 스펙트럼을 구하는 식이고, 스펙트럼에 Log를 씌우게 되면 Spectrum에 대한 그림을 만들어 낼 수 있고, F(u,v)에 대해서 시프트를 시켜주게 되면 다음과 같은 그림을 얻을 수 있습니다.(오른쪽 그림)
    - 스펙트럼 그림에서 중앙에 있는 작은 원 부분이 low frequency를 가지는 신호의 값.
    - 스펙트럼 그림에서 외각에 있는 큰 원 부분이 high frequency를 가지는 신호의 값.
    

---

![image.png](/assets/의료인공지능/10_1_Filtering_in_frequency_domain/image_4.png)

                                                           (좌측 Frequency domain, 우측 원본)

Frequency domain에서 가운데 어떠한 점 하나를 남기고 inverse DFT하게 되면 파장이 상당이 긴 영상을 만들 수 있습니다. 여러 신호가 추가 될 수록 아래와 같이 영상이 점차 뚜렷하게 

![image.png](/assets/의료인공지능/10_1_Filtering_in_frequency_domain/image_5.png)

![image.png](/assets/의료인공지능/10_1_Filtering_in_frequency_domain/image_6.png)

![image.png](/assets/의료인공지능/10_1_Filtering_in_frequency_domain/image_7.png)

![image.png](/assets/의료인공지능/10_1_Filtering_in_frequency_domain/image_8.png)

![image.png](/assets/의료인공지능/10_1_Filtering_in_frequency_domain/image_9.png)

![image.png](/assets/의료인공지능/10_1_Filtering_in_frequency_domain/image_10.png)

중앙 부분의 신호만 남겨두고 다른 부분을 지우고 복원을 한다면 스무딩 된 영상이 나오게 됨.

![image.png](/assets/의료인공지능/10_1_Filtering_in_frequency_domain/image_11.png)

- 너무 스무딩 처리가 된 영상이라서 조금의 조절을 더하고, 노이즈를 제거해주면 클리어한 영상으로 변환시킬 수 있음

가운데 부분을 가리게 되면 low-frequencey가 사라지게 되어 high frequencey만 남기게 되고, inverse DFT하게 되면 아래와 같이 엣지와 텍스쳐만 살아있는 영상을 얻을 수 있음.

![image.png](/assets/의료인공지능/10_1_Filtering_in_frequency_domain/image_12.png)

### frequency domain에서 filtering을 하는게 유리하다고 했음.

![image.png](/assets/의료인공지능/10_1_Filtering_in_frequency_domain/image_13.png)

- 일정한 패턴을 지니는 오류가 있을 때, DFT로 신호를 바꾸면 왼쪽과 같은 밝은 high frequency 신호를 얻을 수 있음

![image.png](/assets/의료인공지능/10_1_Filtering_in_frequency_domain/image_14.png)

- high frequency신호를 가리고, inverse DFT로 변환하게 되면 우측과 같이 클리어한 영상을 얻을 수 있음.

### 대표적인 필터

                                                                 low frequency

![image.png](/assets/의료인공지능/10_1_Filtering_in_frequency_domain/image_15.png)

가운데만 1 나머진 0

![image.png](/assets/의료인공지능/10_1_Filtering_in_frequency_domain/image_16.png)

점점 Smooth하게

![image.png](/assets/의료인공지능/10_1_Filtering_in_frequency_domain/image_17.png)

가우시안으로 전체적으로 퍼지는

                                                             high frequency에서는 반대.

![image.png](/assets/의료인공지능/10_1_Filtering_in_frequency_domain/image_18.png)

# 10.3. Spatial domain vs Frequency domain

![image.png](/assets/의료인공지능/10_1_Filtering_in_frequency_domain/image_19.png)

1. Spatial Domain
    - 신호(g)가 들어왔을 때 filter(h)를 정의해주고 convolution(*)을 통해 원하는 신호(f)얻어냄.
2. Frequency domain
    1. 신호(g)를 DFT해서 Frequency Domain에서의 신호를 얻음
    2. filter도 transfomr하여 Frequency Domain에서의 신호 filter로 바꿀 수 있음(H)
        
        혹은 DFT 이후 신호(G)만 보고 Frequency Domain에서의 filter를 설정 할 수 있음(H)
        
    3. convolution이 아닌 일반 곱셈.
    4. convolution의 결과에서 IDFT(inverse discrete Fourier transform)를 하게 되면
    5. 최종 원하는 아웃풋인 신호(f)를 얻어냄.

1. Spatial Domain에서는 convolution을 하고, Frequenecy domain에서는 일반적인 곱셈을 하기에 Spatial Domain에서의 연산량이 더 많음.
    
    Frequency domain에서는 연산량이 적기에 장점이 되면서도, DFT하고, IDFT하는 과정에서의 시간 소모 발생함.
    
2. Frequency domain에서의 장점으로는, 특정 패턴에 에러가 포함되어 있을 때, filter를 어떻게 정의할지가 불분명할때 Frequency Domain에서 filterling을 하는게 유리 할 수 있음.(의료 데이터의 경우 독특한 패턴이 있는 경우 transform을 통해 filterling처리 복원 등.)