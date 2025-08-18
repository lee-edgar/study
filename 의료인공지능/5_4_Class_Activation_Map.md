# 5.4. Class Activation Map

Bolck Box 구조로 인해 왜 결과가 이렇게 나오는지, 동작원리가 어떻게 되는지 알아보기 위한 연구가 이뤄지고 있는데 그중 하나가 Class Activation Map임.

![image.png](/assets/의료인공지능/5_4_Class_Activation_Map/image.png)

기본적인 CNN 모델이며, 컨볼루션 필터를 통과하고 풀링을 통과하여 피쳐맵들이 생성되고 이후 fully connect layer를 거쳐 최종 prediction을 하게 됨.

class activation mpa은 feature map ~ prediction 부분을 말하며, feature map 이전 단계는 CNN, VGG, ResNet, GoogleNet을 사용해도 무방함.

feature map과 fc layer node들과 모두 연결하는데, 공간 정보들이 사라지는 문제가 있어 Prediction시 영상에서 어느 부분을 보고 판단했는지를 알 수 가 없어서 Global Average [Pooling.GAP](http://Pooling.GAP) 된 score들과 output layer를 이어줘 파라미터를 학습하게 됨.

![image.png](/assets/의료인공지능/5_4_Class_Activation_Map/image_1.png)

Class ACtivation Map의 주요 idea : GAP를 통해 생성핸 channel 별 feature map과 weight간의 관련성을 기반으로 유의미한 패턴들을 추출 할 수 있음

![image.png](/assets/의료인공지능/5_4_Class_Activation_Map/image_2.png)

- 각 feature map의 시각화 결과에 weight들을 곱해주고, feature map*w1부터 feature map*wn까지 더해주면 새로운 activation map을 얻게 됨.
- activation 된 곳을 보고 어떻게 Class를 판별했는지 알 수 있게 됨.

![image.png](/assets/의료인공지능/5_4_Class_Activation_Map/image_3.png)

X-RAY 상에서 질병(Nodule, Mass)가 어딨는지 확인 할 수 있음.