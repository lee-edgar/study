# 4.1. Overall procedure

4.1. Overall procedure

4.2. Validation

4.3. Overfitting / Regularization

4.4. Transfer Learning

4.5. Data Augmentation

4.6. Evaluation of classification model

4.7. Evaluation of classification model(Multi-label)

# 4.1. Overall procedure

![스크린샷 2025-05-21 19.36.35.png](/assets/의료인공지능/4_1_Overall_procedure/image_1.png)

### Feature Extractor를 활용한 Classififer

![스크린샷 2025-05-21 19.51.22.png](/assets/의료인공지능/4_1_Overall_procedure/image_3.png)

classifier를 위해 feature extractor로 특징을 뽑아냄.

1. feature extractor단계에서 Image Intensity값을 바로 Feature로 이용 할 수 있고, 
2. texture 정보를 이용 할 수 있음.
3. 또 segmentation을 할 수 있음. → segmentation의 shape정보, 특정 영역에서의 intensity 정보 등을 추가로 추출 할 수 있음.

### 딥러닝 모델을 활용한 prediction

![스크린샷 2025-05-21 20.02.56.png](/assets/의료인공지능/4_1_Overall_procedure/image_4.png)

굳이 feature extractor를 하지 않고 End to End 구조로 영상을 넣어서 CNN을 활용해 바로 prediction 할 수 있는 방법도 존재함.

![스크린샷 2025-05-21 19.36.35.png](/assets/의료인공지능/4_1_Overall_procedure/image_2.png)

위 방식들이(feature extractor → prediction, cnn→ prediction) 기본적인 structure이며, 영상 혹은 의료영상 등은 모두 이러한 기본적인 구조를 따르는 경우가 많음.

의료영상에서는 위 단계에 아래의preprocessing step가 추가되는 경우가 많음.  물론 영상이 preprocessing을 안거치고 feature extractor 혹은 CNN으로 바로 들어가도 됨.

Image Preprocessing 단계

- Voxel의 Spacing 일치화 : 영상 간의 타입이 다름
- Registration : 영상이 잘 맞춰지지 않을 경우.
- Intensity Normalization : intensity의 distribution이 다를 경우 normalization처리.
- Denoising : Noise줄이기 위해.

image preprocessing 처리 후 feature extractor로 전달 후 demographic score를 기준으로 feature normailzation하고 무수히 많은 feature에 대해서 feature selection을 통해 classififer를 할 수 있음.

학습데이터가 적은 경우 preprocessing ~ feature extractor ~ classifier ~ prediction를 통해 테스트를 해보고, 학습 데이터가 많은 경우에는 두번째 end-to-end CNN ~ prediction으로 하게 됨.

# 4.2. Validation

Validation : Training data에서 Training set과 Validation set으로 나눠 검증을 하기 위한 과정을 말함.

Overfitting : Training set에서의 loss는 감소하지만, Validation Set에서의 loss가 감소하다 증가 하는 구간.

주관적인 비율로 나누지만 일반적으로 Training set이 더 많은 portion을 가지게 됨(5:5, 7:3, 9:1)

만약 data set의 양이 많다면 작은 비율이라도 많은 validation set의 양을 가지게 됩니다.

### Cross Validation

![스크린샷 2025-05-21 20.55.13.png](/assets/의료인공지능/4_1_Overall_procedure/image_5.png)

- K-Fold : K개로 구획을 나눠 K번의 학습을 진행하는데 K번째 학습에서 K번째의data set을 validation으로 사용하며, 제일 좋은 결과를 채택하여 사용함.
- Linear Regression, Neural Network, CNN 등 여러 모델들에 대해서 각각 K-Fold를 적용하여 결과를 각각 내어 가장 좋은 모델을 선택하여 사용하기도 함.
- Leave one out vaildation : 예를 들어, 데이터의 수가 10개 미만일 경우 k-fold적용 시 k를 데이터의 수 만큼 사용하는 기법.

# 4.4. Transfer Learning

![스크린샷 2025-05-21 22.54.14.png](/assets/의료인공지능/4_1_Overall_procedure/image_6.png)

Transfer Learning은 Data가 부족한 Deep Learning에서 사용하는 방법임.

- Medical Image가 적은 상태에서 학습을 하기에는 성능이 매우 제한적임. 이때,Medical Image에 Medical Image가 아닌 일반 이미지를 추가하여 사용하기도 함(medical image 100,  Natural Image 100000 .. ) 두 가지 종류의 이미지를 통해 low level ~ middle level feature ~ high level feature까지 우선 학습이 진행 되게 됨.
- low level feature는 edge, texture등의 기본적인 것들로 학습을 하는데. 이를 medical image에서도 바로 적용은 할 수 있음.
- low level feature부분을 고정하고 middle level feature ~ high level feature부분만 업데이트를 진행 할 수 도 있음. 필요시, high level feature부분만 업데이트를 하게 할 수도 있음.

# 4.5. Data Augmentation

학습용 의료 데이터의 수는 꽤나 제한적이기에 학습 데이터 양을 증가하여 보강 하기 위한 방법으로 data augmentation을 사용하게 됨.

![스크린샷 2025-05-22 19.25.46.png](/assets/의료인공지능/4_1_Overall_procedure/image_7.png)

- Mirroring : 좌우 반전
- Rotation : 회전
- Shearing : 기울이기
- Local Warping : 지역적으로 늘리거나 줄이기
- Intensity Change : 밝기를 키우거나 줄이기

데이터를 스플릿 했을때 보통 training step을 위해서 augmentation을 사용하게 됨.

> generation 되는, augmented 되는 영상들이 실제 test data의 distribution을 많이 커버해주면 커버해줄 수록 모델의 성능은 높아지게 되지만, generation 되는 것이 실제 테스트와 다른 경우 효과가 없을 수도 있음.
> 

# 4.6. Evaluation of classification model

분류 모델 평가에 대한 방법.

![스크린샷 2025-05-22 19.43.04.png](/assets/의료인공지능/4_1_Overall_procedure/image_8.png)

좌측 그림 : real negative와 real postive를 가지고 classifier를 학습 할 수 있습니다.

biarny classification에서의 결과 값이 0과 1이 나오고, Decision Boundary 0.5 부근 형성

Prediction > 0.5의 경우 Postive Prediction

Prediction < 0.5의 경우 Negative Prediction

끝 단 부분(0, 1)값에서 확실하게 prediction(Postive, Negative)이 됨.

위와같이 Real Postive와 Real Negative가 정확히 분류되기를 희망하나, 현실에서는 정확하게 분류 되지 않습니다.

우측그림 : 보통의 classifier가 완벽하지 않은 경우가 많음. 실제 우측 부분(주황색)이 postive이지만, classifier에서는 우측의 아랫 부분만 postive라고 할 수 있음.

생성한 나의 classifier가 말하고 있는 결과가 뒤에 정의됩니다.(~~ positive/negative)

prediction 결과가 맞았는지 틀렸는지는 앞 부분에 정의 됨(True/False ~~ )

- ex) 파란색 부분은 real negative →true negative 라고 표기.
- ex) False Negative : Postive 영역인데, Negative로 인식했으니 → False Negative 표기

![스크린샷 2025-05-22 21.02.54.png](/assets/의료인공지능/4_1_Overall_procedure/image_12.png)

위 Confusion Matrix를 통해 Real과 Prediction간의 관계를 확인할 수 있습니다.

![스크린샷 2025-05-22 19.43.31.png](/assets/의료인공지능/4_1_Overall_procedure/image_9.png)

1. Sensitivity(True Postive rate. recall)
    - False Negative가 낮아야 Sensitivity가 높아지게됨.
2. Specificity(True negative rate)
3. Precision(Postive Predictive value. PPV)
    - FP가 낮아야 Precision이 높아지게 됨.
4. Accuarcy
    - FP, FN이 낮아야만 Accuracy가 높아짐.
    - 전체 중에 True인것을 보는것.

상황ex) 의료분야의 경우 Normal를 cancer로 진단 하는 것보다 cancer가 Normal로 진단하는 것이 훨씬 위험하기에 Cancer 환자를 잡기 위한 방향으로 진행하기에 accuracy를 사용하게 되면 문제가 되기에 Sensitivity(recall)이 100%가 되도록 해야함.

![스크린샷 2025-05-22 19.43.40.png](/assets/의료인공지능/4_1_Overall_procedure/image_10.png)

![스크린샷 2025-05-22 19.43.31.png](/assets/의료인공지능/4_1_Overall_procedure/image_9.png)

1. ROC Curve(Reciver Operating Characteristics Curve)
- x축 : 1-TNRate(Specificity), y축: TPRate(recall). 즉, x축은 이진 분류기에 의해 결정된 score가 표시된 것으로 생각 할 수 있습니다.
- x축이 작은 경우를 생각해 보았을 때, TNR값이 1에 가까워야  1-TRN(1) = 0이 되어 작아져야 합니다. 다시, TNR값이 1에 가까워지게 하기 위해서는 FP가 거의 0에 가까워져야 한다는 말이기도 합니다.
- 우측그림에서 classifier가 0.5에서 0.7로 변경했다고 가정해보면, (classifier 라인이 아래로 가게 될 것임)
    - classifier > 0.7 : postive
    - classifier < 0.7 : negative
    
    classifier 라인이 아래로 내려가기에 자연스레 false postive 부분이 줄어들게 됩니다.
    
    만약 classifier를 0.7이 아닌 0.9로 변경한다면 classifier라인이 더 아래로 내려가고 false postive는 점점 더 없어지게 됩니다.  → TNR값을 1에 가까워지게 하기 위해서는 FP가 0에 가까워져야한다고 했는데, classifier를 0.9로 변경했기에 이제 FP가 0에 가까워졌습니다만, 대신에 false negative가 그만큼 늘어났습니다.(classifier를 0.9로 변경하면 자연스레 FP는 작아지고,FN은 커지게 됨.)
    
    FN값이 증가함에 따라 Sensitivity(recall)값이 작아지게 됩니다.
    

위 설명을 다른 형태로 추가설명을 해보자면,

![스크린샷 2025-05-22 21.41.21.png](/assets/의료인공지능/4_1_Overall_procedure/image_13.png)

       classifier = 0.5

![스크린샷 2025-05-22 21.41.43.png](/assets/의료인공지능/4_1_Overall_procedure/image_14.png)

     classifier = 0.7

![스크린샷 2025-05-22 21.41.54.png](/assets/의료인공지능/4_1_Overall_procedure/image_15.png)

     classifier = 0.9

classifier 값을 클래스 분류를 위한 threshold라고 할 수 있으며 True Postive Rate, False Positive Rate 두 가지를 이용해서 표현하였습니다.

1. classifier가 0.5 :  ***데이터들이 중간에 모여있기에 분류가 잘 되지 않는 모습***을 보입니다.
2. classifier가 0.7 : 완벽하진 않지만, 클래스 간 구분이 점차 선명해지며 분류 성능이 향상되는 모습입니다. ROC 커브도 위쪽으로 휘면서 모델이 무작위 분류보다 우수함을 보여주고, threshold가 올라감에 따라 recall은 점차 감소하는 경향을 보입니다.
3. classifier 0.9 : threshold가 높아져 더 보수적인 예측을 하게 되며, 대부분 negative 판단하게 됩니다. 이로 인해 False Positive는 거의 없지만, False Negative는 증가하여 Recall은 크게 감소합니다. 따라서 ROC 커브 상에서는 점이 좌측 하단으로 이동하게 되고, 전체 ROC 커브는 이미 잘 분리된 데이터 분포를 보여주며 높은 AUC 값을 나타냅니다. 즉, threshold 0.9에서 개별 예측은 보수적이지만, 전체 모델의 성능은 분포가 잘 나뉜 상태를 의미합니다.

### classifier 0.9일때 일어나는 일

| 항목 | 변화 | 이유 |
| --- | --- | --- |
| **TP (True Positive)** | 감소 | 실제 양성인데, classifier 점수가 0.9보다 낮아서 양성이라고 판단 못함 |
| **FN (False Negative)** | 증가 | 암인데 놓침 |
| **FP (False Positive)** | 감소 | 엄격한 기준 때문에, 암이 아닌 걸 암이라고 잘못 판단하는 일이 줄어듦 |
| **Recall (= TP / (TP + FN))** | **감소** ❗️ | TP는 줄고, FN은 늘어나기 때문 |
| **Precision (= TP / (TP + FP))** | **상승** ⬆️ | FP가 줄어들기 때문 |

### classifier의 threshold 0.1과 0.9의 비교

| Threshold | 보수적 vs 민감 | Recall (TPR) | Precision | FP (오진) | FN (진짜 암 놓침) | 언제 적합? |
| --- | --- | --- | --- | --- | --- | --- |
| **0.1** | 매우 민감함 | **↑ 높음** | ↓ 낮음 | ↑ 많음 | ↓ 적음 | ***선별(Screening) 목적*** |
| **0.9** | 매우 보수적 | ↓ 낮음 | **↑ 높음** | ↓ 적음 | ↑ 많음 | ***최종 진단 or 수술 결정*** |

빠른 질병 선별(Screening) 단계에서는 threshold를 0.1처럼 낮춰 민감하게 탐지하는 것이 중요하며, 이는 높은 Recall을 확보하여 환자를 놓치지 않기 위함입니다. 반면, 최종 진단이나 수술 여부 판단 단계에서는 threshold를 0.9처럼 높게 설정하여 Precision을 최대화하고, 오진을 최소화하는 전략이 적절합니다.

![스크린샷 2025-05-22 19.43.50.png](/assets/의료인공지능/4_1_Overall_procedure/image_11.png)

F1 Score는 Harmonic mean of recall and precision이라고, recall과 precision의 조화 평균을 나타냅니다.

- precision과 recall이 높으면 h(F1 score)값이 높게 나오는 모습을 보입니다.
- precision과 recall값이 낮으면 h(f1 score)가 상대적으로 낮게 나오는 모습을 볼 수 있습니다.

# 4.7. Evaluation of classification model(Multi-label)

![스크린샷 2025-05-23 19.11.33.png](/assets/의료인공지능/4_1_Overall_procedure/image_16.png)

1. TP : 실제 클래스가 A인데, A로 예측한 것. 실제 값을 실제 값이라고 예측 한 것
2. FP : 실제 클래스가 B, C, D인데 A로 예측한 것. 실제 값이 아닌데 실제 값으로 예측 한 것.
3. FN : 실제 클래스가 A인데, B, C, D로 예측 한것. 실제 값이 아닌데 실제 값이 아니라고 예측 한 것
4. TN : 실제 클래스가 B,C,D인데 B,C,D로 예측한 것. 실제 값을 실제값이 아니라고 예측 한 것.

![스크린샷 2025-05-23 19.52.26.png](/assets/의료인공지능/4_1_Overall_procedure/image_17.png)

전체에 대해에 대해서 우측 보다 전체에 대해서 A 예측을 많이 맞추진 못했기 때문에 accuracy가 0.64로 보이는 모습.

하지만, 적은 데이터인 B, C, D에 대해서 모두 맞춘 모습을 볼 수 있습니다.

좌측보다 170개의 A를 맞췄기에 높은 accuracy를 보임.

하지만, 적은 데이터인 B, C, D에 대해서는 하나도 맞추지 못하고 놓치는 모습은 매우 크리티컬한 결과를 초래합니다.

어느 모델이 더 우세한가에 대해서  자세히 살펴보기 위해 F1 Score를 적용해 볼 수 있습니다.

                                           A, B, C, D

F1 Score :             TP : 100, 10, 10, 10

                              FP :    0, 50, 10, 10

                              FN :   70,  0,  0,  0

[(tp+fp)/tp]precision :   1, 5/6, 1/2, 1/2. → 2.x / 4

[(tp+fn)/tp]       recall : 100/170, 1, 1, 1. → 3.x / 4

| 지표 | A | B | C | D |
| --- | --- | --- | --- | --- |
| **TP** | 100 | 10 | 10 | 10 |
| **FP** | 0 | 50 | 10 | 10 |
| **FN** | 70 | 0 | 0 | 0 |
| **Precision** | **1.000 (100/100)** | **0.167 (10/60)** | **0.500 (10/20)** | **0.500 (10/20)** |
| **Recall** | **0.588 (100/170)** | **1.000 (10/10)** | **1.000 (10/10)** | **1.000 (10/10)** |
| **F1 Score** | **0.740** | **0.286** | **0.667** | **0.667** |

f1 score :  0.590 

                                          A, B, C, D

F1 Score :             TP : 170, 0, 0, 0

                              FP :    30, 0, 0, 0

                              FN :  0, 10, 10, 10

[(tp+fp)/tp]precision :   170/200, 0, 0, 0 → (170/200)/4

[(tp+fn)/tp]       recall : 1, 0, 0, 0 → 1/4

| 지표 | A | B | C | D |
| --- | --- | --- | --- | --- |
| **TP** | 170 | 0 | 0 | 0 |
| **FP** | 30 | 0 | 0 | 0 |
| **FN** | 0 | 10 | 10 | 10 |
| **Precision** | **0.850 (170/200)** | **0.000 (0/0)** | **0.000 (0/0)** | **0.000 (0/0)** |
| **Recall** | **1.000 (170/170)** | **0.000 (0/10)** | **0.000 (0/10)** | **0.000 (0/10)** |
| **F1 Score** | **0.919** | **0.000** | **0.000** | **0.000** |

f1 score :  0.230 

accuracy 기준으로 우측의 값이 우수합니다. 우측의 상황에서 A클래스의 예측 성능이 높기에 우측 accuracy값이 우수한 결과를 보입니다. 그러나 우측의 경우 b,c,d,처럼 소수클래스에 대해서는 전혀 예측을 하지 못했기에 크리티컬한 결과를 초래 하게 됩니다.

f1 score기준으로는 좌측의 값이 우수합니다. 우측기준으로 A클래스에 대해서 예측을 많이 하지는 못했지만, 소수의 B, C, D의 모든 예측을 했기 때문입니다. 

이럴 경우 accuracy보다는 f1 score 기준으로 모델을 평가를 해야 합니다.