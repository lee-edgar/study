# 12.7. Similarity measure ? SSD SAD NCC

영상 간의 similarity(유사성) 측정하는 방법

정합 과정을 복습해본다면, 먼저  correspondences(대응점, 매칭점)을 찾아서 transformation matrix를 추정하고 backward warping을 하게 됩니다.

- registration정합 과정의 단계별 풀이
    
    ![스크린샷 2025-06-29 09.52.29.png](/assets/의료인공지능/12_7_Similarity_measure_SSD_SAD_NCC/image_1.png)
    
    ![스크린샷 2025-06-29 09.52.42.png](/assets/의료인공지능/12_7_Similarity_measure_SSD_SAD_NCC/image_2.png)
    
    ![스크린샷 2025-06-29 09.53.00.png](/assets/의료인공지능/12_7_Similarity_measure_SSD_SAD_NCC/image_3.png)
    

![스크린샷 2025-06-29 10.09.33.png](/assets/의료인공지능/12_7_Similarity_measure_SSD_SAD_NCC/image_4.png)

좌측 moving 이미지 패치에 대응하는 우측 fix이미지에서의 여러 패치들을 볼 수 있으며, 각각의 패치들과의 유사성을 비교하면, 2번째, 4번째 패치는 꽤나 높은 유사도를 가지게 됩니다.

---

![스크린샷 2025-06-29 10.14.13.png](/assets/의료인공지능/12_7_Similarity_measure_SSD_SAD_NCC/image_5.png)

작은 패치들 간의 거리를 계산하는 여러가지 방법 존재.

1. Sum of Squared Distance. SSD
    
    I : intensity이며, ***각 intensity의 차를 제곱한 값. distance가 작을 수록 유사도가 높다고 할 수 있음(완전히 일치하면 0)***
    
    - I1(x,y) : moving image patch
    - I2(x,y) : fix image patch
2. Sum of Absolute Distance. SAD
    
    각 intensity의 차를 절대값 씌운 값. 픽셀의 모든 값에 대해서 차이를 구해 유사도를 계산하는 방법
    
3. Normalized Cross Correlation
    1. SSD, SAD를 사용하면 발생하는 문제점 : 
        
        ![스크린샷 2025-06-29 10.30.09.png](/assets/의료인공지능/12_7_Similarity_measure_SSD_SAD_NCC/image_6.png)
        
        - moving이미지에서 fixed 이미지 변환 시, 배경과 밝기가 더 어두워지거나, 더 밝아지게 됩니다. 이때, SSD, SAD를 구하면 모든 점에서의 어느 정도의 밝기가 차이 나기 때문에 유사도가 서로 낮아지게(distance가 크게) 됩니다.
    2. SSD, SAD 사용시 발생하는 문제를 보완하기 위해 사용됩니다. 
        
        ![스크린샷 2025-06-29 12.34.08.png](/assets/의료인공지능/12_7_Similarity_measure_SSD_SAD_NCC/image_7.png)
        
        - SSD에 대한 식을 풀어 쓴 식입니다. ***SSD식의 유사도를 높이기 위해 해당 식이 낮은값***이 되도록해야합니다.
        
                                      코릴레이션 : SSD를 풀어쓴 수식 $I1(x,y)*I2(x,y)$
        
        - 코릴레이션이 높아지게되면 마이너스 연산에 의해 distance가 낮아지게 되어, 유사도가 커지게 됩니다.
        
        →코릴레이션을 구할 때, 색깔의 변화가 있기에 각 패치별 평균값과 스텐다이비에이션을 통해 intensitic값을 구하고 
        → 해당 intensitic 값들을 normalization해주게됩니다. 
        → 이후 normalization 된 패치의 코릴레이션을 구하겠다는게 Normalized cross correlation이 되겠습니다.
        
        ![스크린샷 2025-06-29 14.40.28.png](/assets/의료인공지능/12_7_Similarity_measure_SSD_SAD_NCC/image_8.png)
        
                                           Normalized cross correlation. NCC 식
        
        Normalized cross correlation 값은 -1에서 1사이의 값이 나오게 되며, 1에 가까울 수록 상당이 유사한 관계를 가진다 라고 볼 수 있습니다.