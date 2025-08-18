# 10.7. Super-resolution via dictionary learning

Super-resolution 문제에 대해서도 비슷하게 Dictionary learning기법을 사용 할 수 있음.

![스크린샷 2025-06-18 22.38.28.png](/assets/의료인공지능/10_7_Super-resolution_via_dictionary_learning/image.png)

                                        영상의 사이즈를 줄이고, 다시 interpolation으로 확장한 영상.

해당 이미지는 Super-Resolution(초해상도 복원) 문제를 설명하는 예시로서, dictionary learning 기법이 적용될 수 있는 맥락을 보여줍니다.

1. 영상의 해상도를 인위적으로 낮춘 뒤, 보간(interpolation) 기법으로 다시 확장한 영상은 좌측 이미지처럼  전체적으로 스무스해지고 디테일이 손실된 모습을 보입니다. 
특히, 확대된 빨간 박스 영역에서 경계선이 흐릿하고 구조적 정보가 뭉개져 있는 모습을 확인 할 수 있습니다.
2. 우측은 고해상도 원본 또는 dictionary learning 등의 복원 기반 알고리즘을 적용한 것으로, 경계선이 더 명확하고 세부 구조가 잘 살아있는 모습을 보입니다.

이처럼 단순한 보간 기법만으로 디테일 복원이 어려워지므로, 고해상도 패치를 학습한 딕셔너리를 활용해 저해상도 패치를 복원하는 dictionary learning 기반 super-resolution 방법이 효과적임을 나타냅니다.

실제로 보는 옵져베이션 된 영상Y을 보고 high resoltuion X영상을 만들어야함.

→ super resolution을 위해서 dictionary learning필요한데,  dictionary learning이 되어있다고 가정.

- 학습을 할때 Dh. high resoultion의 dictionary도 만들어놨다고 가정

Y input → Y와 비슷한 어떠한 값을 만들어 낼 수 있는 alpha 값을 찾아줘야함.

1. 해당 값을 미니마이제이션 해야하면서
    
    ![스크린샷 2025-06-18 22.50.24.png](/assets/의료인공지능/10_7_Super-resolution_via_dictionary_learning/image_1.png)
    
2. 동시에 어떤 가중치를 주고, alpha의 L1 norm값을 미니마이제이션 하는 alpha를 찾아야함
    
    ![스크린샷 2025-06-18 22.53.21.png](/assets/의료인공지능/10_7_Super-resolution_via_dictionary_learning/image_2.png)
    

1. Dh alpha

![스크린샷 2025-06-18 22.56.36.png](/assets/의료인공지능/10_7_Super-resolution_via_dictionary_learning/image_3.png)

위 식에서 alpha값을 먼저 찾고, 그 alpha값을 그대로 가지고 Dh로 옵니다. 어떻게 보면, Dh alpha가 X가 되는 것입니다.

1. Y에 대해서 feature를 뽑기, F(d alpha)에 대해서 feature 뽑아냄.
    
    ![스크린샷 2025-06-18 22.59.59.png](/assets/의료인공지능/10_7_Super-resolution_via_dictionary_learning/image_4.png)
    
2. 패치단위로 precessiong이 진행되면서 특정 영역을 high resolution(고해상도)로 바꾸고, sliding하면서 다음 번째에서 또 high resolution을 하게 됩니다. 
그러다 보면 high resolution끼리 곂치는 구간이 발생함.
    
    ![스크린샷 2025-06-18 23.04.49.png](/assets/의료인공지능/10_7_Super-resolution_via_dictionary_learning/image_5.png)
    
    - 이전 precessing에서 high resolution으로 만들어논 패치와 새롭게 만들어지는 패치가 비슷해지는 alpha 값을 정의함.
    - alpha 값을 구해 super resolution을 순회하면, 픽셀 단위 기준으로, 에스티메이션 된게 여러개가 생기게 됩니다. 예시에서의 중간 픽셀을 보면 4번의 prediction이 되고 → prediction 된 값의 average 적용.
        
        ![스크린샷 2025-06-18 23.07.26.png](/assets/의료인공지능/10_7_Super-resolution_via_dictionary_learning/image_6.png)
        

### 가장 먼저 low resolution에 대한 알파값을 찾고, 그 알파값을 high resolution의 dictionary(Dh alpha)들과 곱을해서 X를 복원하는 방식으로 high resolution영상을 만들어 내게 됨.