# 5.2. Feature selection using Entropy / Mutual information

![image.png](/assets/의료인공지능/5_2_Feature_selection_using_Entropy_Mutual_informa/image.png)

1. 벡터 연관성

![image.png](/assets/의료인공지능/5_2_Feature_selection_using_Entropy_Mutual_informa/image_1.png)

- V1, V2, V3간의 연관성을 알아 볼 수 있음.
- V1의 N값에 대해서는 V2에서 낮은 숫자 값을 볼 수 있고, C값에 대해서는 높은 숫자 값을 볼 수 있습니다.
    
    반면에, V3는 V1, V2의 연관성과는 좀 떨어진 모습을 보일 수 있습니다. V1, V2 처럼 연관성이 높은 feature들을 추출 할 수 있으면 overfeating과 같은 문제들을 완화 시킬 수 있습니다.
    
- 이러한 feature간의 상관관계를 분석해 의미있는 feature를 추출해야 모델 성능 향상에 기여할 수 있습니다.

이러한 어떤 Distribution 간에 어떤 유사도를 계산해 주기 위한 방법들을 생각 해 볼 수 있습니다.

1. 정보량에 대한 식(Amount of information) : -log(p(x))

![image.png](/assets/의료인공지능/5_2_Feature_selection_using_Entropy_Mutual_informa/image_2.png)

Entropy 정보량의 기댓값 : 불확실성이 높을 수록 Entropy가 커진다.

- 확률 p(x)p(x)p(x)가 1에 가까우면, 해당 사건은 항상 일어나는 일이므로 정보량은 0입니다.
- 반대로, p(x)p(x)p(x)가 0에 가까울수록 드물게 발생하는 사건이므로 정보량은 매우 커집니다 (이론적으로 무한대).

결합 엔트로피. Joint Entropy : 확률 변수(X,Y) 둘 간의 불확실성 관계를 표현해주는 식

한 가지의 사건이 아닌 X와 Y를 고려한 하여 확률p(x, y)를 -log{p(x, y)}에 넣어서 기대값을 구한 것

X,Y가 독립변수 일 경우 H(X) +H(Y) = H(X,Y))가 되고,

H(X)+H(Y)와 H(X,Y)의 차이를 구하면 X와 Y가 서로 관련성이 있는지 알아 낼 수 있는데 이를 Mutual information이라고 함.

상호정보량. Mutual information :   I(X;y) = H(X) +H(Y) - H(X,Y)

상호 의존성에 의해 두 변수 간 관련성이 높으면 해당 값이 커지게 되며, 관련성이 없는 독립된 값이라면 0 값이 됩니다.

즉, Mutual Information은 두 변수를 함께 고려할 때 얼마나 불확실성이 줄어드는지를 정량적으로 측정하는 지표.

> 따라서, Mutual Information이 높은 feature들을 선택하면, target 변수와 높은 관련성을 가진 특징들을 추출할 수 있으며, 이를 통해 모델의 예측 성능을 높이고 불필요한 정보로 인한 overfitting 가능성을 줄일 수 있습니다.
> 

1. Decision Tree

상관관계가 있는 feature들 간 selection을 Entropy를 통해 구하는 ML방법.

![image.png](/assets/의료인공지능/5_2_Feature_selection_using_Entropy_Mutual_informa/image_3.png)

전체 Subject를 보면 4개의 Normal, 4개의 AD로 구성되어있습니다. 

- 전체 4개의 Normal, 4개의 AD = -(Normal log Normal + AD log AD) =  -(1/2 log 1/2 + 1/2 AD 1/2) = H(s)

feature1이 8보다 크냐, 작냐의 조건

위  8≥feature1≥8 =  0log0 - (1/5 log 1/5 + 4/5 log 4/5) = H(f1)

- feature1≤8일 경우 3가지는 대해서 모두 Normal인 상황 = 0log0
- feature1>8일 경우 5가지는 1개의 Normal, 4개의 AD인 상황 = (1/5 log 1/5 + 4/5 log 4/5)

feature2가 10보다 크냐, 작냐의 조건

0 - 0 = H(f2)

- Normal이 10보다 모두 작은 상황 = 0
- AD가 10보다 모두 큰 상황 = 0

H(f2)에 대한 Dicision Tree

![image.png](/assets/의료인공지능/5_2_Feature_selection_using_Entropy_Mutual_informa/image_4.png)

- 1번째 : 초기 f2 ≥ 10 조건을 확인하고
- 2번쨰 : 엔드로피를 가장 낮춰줄 수 있는 특정 피처와 그에 맞는 Threhold값이 계산됨.

이러한 방식으로 내려가는 과정을 반복하며 트리구조를 만들어 냅니다. 해당 트리구조에서 상단에 존재하는 트리들이 feature와 특정 class 간의 연관성이 높기 때문에 중요한 포인트가 될 수 있고. 이러한 연관성을 바탕으로 classification을 통해 feature selection을 할 수 있게 됨.

해당 decision tree에서는 feature와 class간의 관계를 학습을 하는데, feature와 feature 간의 관계를 고려해주는 mRmR Feature Selection 기법도 존재함.

1. mRMR Feature Selection

![image.png](/assets/의료인공지능/5_2_Feature_selection_using_Entropy_Mutual_informa/image_5.png)

mRMR은 클래스와의 관련성이 높은(relevant) feature를 선택하되, 다른 feature들과 중복 정보가 적은(redundant하지 않은) feature를 선별하는 방법이며 아래 두 가지 조건을 동시에 만족하는 feature를 추출.

1. 클래스와 높은 상호정보량(Mutual Information)을 가지는 feature를 우선 선택
- I(feature, class)값이 클수록 해당 feature는 클래스 예측에 유용한 정보를 많이 담게되고,  평균 정보량D(S,c)는 클래스와의 관련성(높을 수록 좋음)을 중요시 함.
1. 서로 중복되는 정보가 적은 feature들만 함께 선택
- I(feature1, feature2)값이 작을수록 feature 간 중복 정보가 적다는 뜻이고, 중복도 측정  값 R(S)는 feature간 중복성(낮을 수록 좋음) 중요시함

mRMR = max[D(S,c) - R(S)]. 

즉, mRMR은 클래스와 관련성은 높고, 다른 feature들과 중복은 적은 feature를 선택함으로써 모델의 예측 성능을 높이고, 과적합(overfitting) 문제를 줄이는데 기여할 수 있음.