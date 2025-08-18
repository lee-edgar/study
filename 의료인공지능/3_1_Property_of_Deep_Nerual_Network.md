# 3.1. Property of Deep Nerual Network

![image.png](assets/의료인공지능/3_1_Property_of_Deep_Nerual_Network/image.png)

                                         (숫자7 영상에 대한 각row를 dense하게 하여 sigmiod→predict)

위 그림과 같이 영상의 파라미터를 1row만 weight를 강하게 주고, 나머지 row에 대해서는 0에 가깝게 주었다고 가정 했을때, 첫 번째 줄의 pixel값에 의해 sigmiod 내부의 값이 정의가 될 것입니다.

이 값이 0보다 크면 최종 prediction 값이 0.5보다 크게 될 것이고, 0보다 작은 값이 나온다면 sigmoid function에 의해 0.5보다 작은 값이 나오게 될 것입니다.

(빨간 원)해당 노드는 영상에서의 1row에 대해 강조하는 node가 될 것입니다. 해당 노드 대신에 다른 node들을 만들 수 도 있구요. neural network을 보면 여러 node로 구성 되는 것을 볼 수 있습니다.

![image.png](/assets/의료인공지능/3_1_Property_of_Deep_Nerual_Network/image_1.png)

만약, 위 이미지처럼 다른 부분을 높은 파라미터라고 정의하게 되면(중점으로 보게 되면) 파라미터 weight의 중요도가 다름을 알 수 있습니다. 각각의 node들 하나하나가 자기가 담당하는 어떠한 local한 부분의 특징을 확인 할 수 있다고 생각 할 수 있습니다.

![image.png](/assets/의료인공지능/3_1_Property_of_Deep_Nerual_Network/image_2.png)

각각 다른 곳을 중점으로 보는 여러 node들을 생성 할 수 있음.

- low level featreus : 1 hidden layer들에서는 작은 local 부분에서 특징은 추출하게 되며,
- higher level fetarues : 2hidden layer에서는 점점 더 큰 local 부분에서의 특징을 추출함.

hidden layer가 거의 없는 logistic regression이나 neural network는 low level features만으로 classification할 수 있고,

hidden layer가 깊은 deep neural network을 처리 할 때는 higher level feature 바탕으로 classification하게 됨.

![image.png](/assets/의료인공지능/3_1_Property_of_Deep_Nerual_Network/image_3.png)

숫자가 아닌 사람 영상으로 보았을때,

1. 1 hidden layer : 엣지나 텍스처와 같은 local한 feature을 추출함.
2. 2 hidden layer :  1hidden layer의 weight에 따라서 중간단계 feature을 뽑게 됨.
3. 3 hidden layer : 그 이후 3hidden layer에서는 더 높은 수준의 feature을 뽑게 됨. 
4. classifier layer : 높은 수준의 feature를 바탕으로 최종 판단(humen 유무 구분)을 하게 됨.

deep nerual network의 구조를 보면 앞단(1 hidden layer ~ 3 hidden layer)은 feature extraction역할을 수행하고 feature extraction에서 얻은 feature로 classifier(logistic regression,nn 등)를 하게 됨.

classifier layer 이전 hidden layer에서 사람의 입, 강아지의 입, 고양이의 입에 대한 feature를 정확히 구분하기 수월해진다.

![image.png](/assets/의료인공지능/3_1_Property_of_Deep_Nerual_Network/image_4.png)

위 단계를  end-to-end learning이라고 부른다. 영상을 넣어주고, y값이 존재하다고 가정하면 영상과 레이블y의 관계를 학습. 그리고 레이블y를 잘 구분하는데 유용한 feature를 최적화해 gradient descent로 feature를 추출할 수 있는 어떠한 파라미터들을 학습해준다는 측면이 주요한 내용임.

![image.png](/assets/의료인공지능/3_1_Property_of_Deep_Nerual_Network/image_5.png)

보통의 의료영상 데이터에서는 데이터가 적기에 DNN과 기초적인 Machine learing Model(SVM, Random Forest)과 차이가 적을 수 있으나, 많은 데이터가 있을 경우 큰 성능 차이를 보이게 된다.

![image.png](/assets/의료인공지능/3_1_Property_of_Deep_Nerual_Network/image_6.png)

위에서 Deep Neural Network가 좋은점에 대해서 확인해보았는데, 한계점도 분명히 존재함.

hidden layer들을 깊게 쌓을 수록 parameter 수가 매우 많아지게 되어서 학습 시 단점이 될 수 있으며, 일반적으로 feature extraction이 잘 구성되고, feature를 잘 뽑아줄 수 있어야 좋은 성과를 내 보일 수 있음. 이러한 단점을 극복하기 위해 CNN이 제안되었음.