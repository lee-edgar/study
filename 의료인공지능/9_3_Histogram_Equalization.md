# 9.3. Histogram Equalization

“CDF를 이용해 기존 intensity 값을 새로운 intensity 값으로 매핑 해주는 과정”

![image.png](/assets/의료인공지능/9_3_Histogram_Equalization/image.png)

Histogram은 밝기 값이 영상에서 어떻게 분포하는지를 말해주는데,

구역별로 pixel의 개수를 구해줄 수 있음.  어두운 영역의 경우 0~255값 중 0에 가깝게 분포가 되어있음.

하나하나의 구간들을 Bin이라고 부르고, 위 예시에서는 Bin의 size가 4로 설정됨(0,1,2,3 / 4,5,6,7 … )

각기 다른 intensity들의 영상.

![image.png](/assets/의료인공지능/9_3_Histogram_Equalization/image_1.png)

![image.png](/assets/의료인공지능/9_3_Histogram_Equalization/image_2.png)

                                                   (분포)

분포에 대해서 Cumulative Density Function(CDF)를 그려볼 수 있음.

![image.png](/assets/의료인공지능/9_3_Histogram_Equalization/image_3.png)

누적분포이기에 값들이 점차 커지게 됨.

1번 영상에서는 초기 부분의 값들이 크기에 초반부분이 가파르며,

2번 영상에서는 후기 부분의 값들이 크기에 후반부분에서 가파라지는 모습을 보임.

![image.png](/assets/의료인공지능/9_3_Histogram_Equalization/image_4.png)

x축 : 기존 intensity 값(예, 10, 50, 70, 90)

y축 : 해당 intensity 픽셀 누적 비율.(예, 60, 120, 140, 180) 0~255값.

CDF(10) → 매핑 값 60

CDF(50) → 매핑 값 120

CDF(70) → 매핑 값 140

> Intensity가 작을수록 좌측이 크게 생기며, CDF 변화폭이 크기에 더 큰 밝기로 매핑이 됨. 어두운 영역에 대해서 더 높은 변화폭을 주기에 크게 밝아지는 모습을 보임.
가장 어두운 영역인 가장 좌측 부는 영상에서 아무것도 없는 빈 공백인 경우가 많기에, 값이 변화하긴 하나 크게 영양가 없는 부분이라고 볼 수 있음.

“CDF를 이용해 기존 intensity 값을 새로운 intensity 값으로 매핑 해주는 과정”
> 

그렇다면, 밝은 영상에서는 상대적으로 어두워지긴하나, 어두운 영상에서 밝은 영상으로 되는것의 반대 개념은 아님. 이는 CLAHE(적응형 히스토그램 평활화) 방식이 효과적임.