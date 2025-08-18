# 12.8. Similarity measure ? Mutual information

mri, pet 혹은 mri, ct 등 서로다른 모달리티를 가지는 영상들 사이에서 유사도를 비교할 때 사용할 수 있는 measure에 대해

![스크린샷 2025-06-29 15.12.39.png](/assets/의료인공지능/12_8_Similarity_measure_Mutual_information/스크린샷_2025-06-29_15.12.39.png)

- 위 영상 : moving image
- 아래 영상 : fixed image

두 영상 간 ssd, sad, ncc를 구하게 되면 similiarity는 낮게 나오게 될 것 이고, 이것을 어떻게 극복 하지?

moving 이미지에 대한 값, fixed이미지에 대한 값의 join histogram을 구해 볼 수 있습니다.

### 불확실성이 낮은 유사도 측정

![스크린샷 2025-06-29 17.27.57.png](/assets/의료인공지능/12_8_Similarity_measure_Mutual_information/스크린샷_2025-06-29_17.27.57.png)

1. 배경부분은 둘다 어두운 색으로 표현하여 유사도가 비슷하다고 볼 수 있습니다. 가장 하단에 히스토그램으로 표현합니다.
2. moving의 상단 흰색 영역과 fixed에서의 연분홍색과 비교해 보았을때, 조금의 유사도가 있으니, 가장 우측에 히스토그램을 포현할 수 있습니다.
3. moving의 하단 회색부분과 fixed의 연붕홍을 비교할때, 비교적 어두운 배경 부분과, 흰색 영역의 사이의 색깔이니, 중간에 히스토그램을 표현합니다.

***배경과 타겟의 위치, 비율이 비슷하게 되어있으므로 꽤나 적은 히스토그램이 나오게 되었습니다. → 불확실성이 좀 낮아지는 결과***

### 불확실성이 높은 유사도 측정

![스크린샷 2025-06-29 17.27.40.png](/assets/의료인공지능/12_8_Similarity_measure_Mutual_information/스크린샷_2025-06-29_17.27.40.png)

***배경과 타겟의 위치가 서로 일치하지 않고, 비율 또한 미스매칭되는 모습을 보여줍니다.***

서로 배경이 되는 위치가 다르고, 타겟의 위치가 다르기에 비율 같은 부분이 미스매칭되는 모습을 보여줍니다.

moving에서는 타겟이 되는 영역이 fixed에서는 배경이 되는 모습같은것이죠.

그렇다 보니, 히스토그램에서 수없이 작고 많은 히스토그램이 생성됩니다 → ***불확실성이 좀 높아지는 것이죠***

### Mutual Information

![스크린샷 2025-06-29 18.47.26.png](/assets/의료인공지능/12_8_Similarity_measure_Mutual_information/스크린샷_2025-06-29_18.47.26.png)

entropy를 바탕으로 mutual information을 구하는데 식은 아래와 같습니다.

MI → I(Moving, Fixed) = H(Moving) + H(Fixed) - H(Moving, Fixed) 
                                                                                       ←여기서 H(Moving, Fixed)는 join entropy를 말함.

H(Moving, Fixed)값이 작으면 작을 수록 잘맞는 좋은 결과임.

***결국, I(M,F)값의 maximaize 하는 방향으로 유사도가 높은 패치들을 찾아준다고 생각하면 됩니다.***

Mutual Information의 변형으로 normalization Mutual Information이 사용 되기도 합니다.

***아래 부분의 H(M,F)의 부분이 작아지게 되면 normalization mutual information의 값이 전체적으로 커지게 됩니다.***