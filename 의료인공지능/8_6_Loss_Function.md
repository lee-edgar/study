# 8.6. Loss Function

![image.png](/assets/의료인공지능/8_6_Loss_Function/image.png)

Segmetnation Loss에 대해서.

1번째는 CrossEntropy Loss를 나타냅니다. CE에 Label과 Prediction을 비교하여 loss를 확인 할 수 있습니다.

![image.png](/assets/의료인공지능/8_6_Loss_Function/image_1.png)

- Segmentation을 하면 어떤 영상에 대해 위와같은 Prediction값과 GroundTruth가 있습니다.

![image.png](/assets/의료인공지능/8_6_Loss_Function/image_2.png)

- pixel단위로 label이 매칭이 되는지 되지 않는지 확인을 해볼 수 있습니다. 모든 값들을 합하게 되면 loss로 사용 할 수 있습니다.
- segmentation에서의 CE는 이렇게 사용되지 않는 경우가 많습니다.

![image.png](/assets/의료인공지능/8_6_Loss_Function/image_3.png)

1. ground truth의 object가 상당히 작다고 가정해보면, 
의료영상에서 특정 부분의 부위가 상당이 작은 경우가 있을 수 있습니다. prediction 값도 해당 부분을 잘 찾으면 좋지만, prediction값이 foreground가 하나도 안나왔다고 0으로 가정해보면,
2. prediction과 ground truth 서로의 similarity가 상당이 좋은것으로 나오는데. ground truth의 소수 부분을 제외하면 다 맞는 결과이기 때문입니다. 
3. 즉, classifiaction에서 사용하는 loss를 가지고 segmentation에 적용한다면 물체가 아주 작은 경우에 이러한 에러가 발생 할 수 있습니다.

### WCE(weighted cross entropy)

이러한 문제를 해결하기 위해 WCE(Weighted Cross Entropy)기법이 사용됩니다.

![image.png](/assets/의료인공지능/8_6_Loss_Function/image_4.png)

기존의 CE에 베타값을 추가해주었는데, 베타 값을 통해서 foreground와 background 값을 강조할 수 있습니다.

1. 베타 값이 1보다 크게 되면 false negative를 줄임(foreground에 대한 값이 커짐)
2. 베타 값이 1보다 작은 경우 false postive를 줄임(background가 되게끔 만들수 있음)

BCE(Balanced Cross Entrpoy)를 사용 할 수도 있음.

### Dice Loss

![image.png](/assets/의료인공지능/8_6_Loss_Function/image_5.png)

Dice coefficient는 Segmentation의 ground truth와 Prediction이 있다고 가정하면,
                          둘 간의 식 : 교집합x2/ |Sg|+|Sp|
 얼마나 ground truth와 prediction 값이 유사하느냐를 나타내는 식 

1. Sg, Sp가 완전히 같으면 Dice coefficient는 1
2. Sg, Sp가 완전히 다르면 Dice coefficient는 0

> Sg, Sp에 대해 Coefficient가 1인 경우 Background는 고려하지 않고 Foreground만을 고려하기에 Cross Entropy에 비해 Foreground에 집중함.
> 
1. Dice Loss에서 =$\frac{2p\hat{p}}{p + \hat{p}}$가 완전히 같으면 1이 되어  loss는 0.
2. Dice Loss에서 = $\frac{2p\hat{p}}{p + \hat{p}}$가 완전히 다르면 0이되어 loss는 1.

Dice Loss는 아래와 같이 구할 수 있으나, 

                      Dice Loss = 1-Dice coefficient

분모(p)가 0이 되는 것을 방지하기 위해 분모, 분자에 1을 더한 식임

![image.png](/assets/의료인공지능/8_6_Loss_Function/image_6.png)

픽셀 단위가 아니라 영상 단위 Loss 계산을 통해 parameter update으로 사용이 가능하며 CrossEntropy와 Dice Loss 모두를 같이 사용하고, 최적화를 시킬 수 도 있습니다.