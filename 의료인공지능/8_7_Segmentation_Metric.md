# 8.7. Segmentation Metric

![image.png](/assets/의료인공지능/8_7_Segmentation_Metric/image.png)

1. Pixel accuracy
    - Classification에서 많이 사용하는 정확도이며, 물체가 작은 경우 높게 나올 수 있음.
    - 예로, 1%의 물체(True Postive)가 존재하고, 99%의 배경이 존재한다면 99%의 배경(TN, True Negative)만을 보고 높은 정확를 내보낼수 있기에 Segmentation에서는 적합하지 않은 metric일 가능성이 있음.
2. Intersection over Union
    - Sg는GroundTruth label. Sp는 Prediction. 합집합/교집합을 구한 것임.
    - True Negative가 없기에 foreground의 겹침의 정도를 보고 metirc함. 많이 곂치면 1, 덜 곂치면 0.
3. Dice Coefficient
    - True Negative 미사용.
    
    ![image.png](/assets/의료인공지능/8_7_Segmentation_Metric/image_1.png)
    

외곽선들이 얼마나 잘 맞는지를 재보는 distance 기반의 metric방법들도 있음. 녹색 부분을 ground truth=G, 파란 부분을 prediction=A으로 가정.

![image.png](/assets/의료인공지능/8_7_Segmentation_Metric/image_2.png)

1. Hausdoff distance
- h(A,B)를 먼저 살펴보면, Prediction(A)의 한점에 대해서 GroundTruth(B)의 바운더리에 있는 모든 점들을 살펴보며 minimum값을 구함.
    
    ![image.png](/assets/의료인공지능/8_7_Segmentation_Metric/image_3.png)
    
    - 위와 같은 방식으로 모든 Prediction 점에 대해서 Minimum을 찾고, 그 중에서의 Maximum 값을 선택하게 됨.
    
    ![image.png](/assets/의료인공지능/8_7_Segmentation_Metric/image_4.png)
    
    - 반대로 GroundTruth의 점에대해서 Prediction 바운더리의 모든 점의 minum을 찾고, 그 중 maximum을 찾는 경우 위와 같은 방식으로 처리될 수 있음.
- Hausdorff distnace는 Noise에 약한 단점이 있음.
1. AVD는 Hasudorff distnace의 minum들의 maximum을 찾는게 아닌 minum의 평균을 냄.

## Hausdorff Distance를 두 방향으로 계산하는 이유

**예측(Prediction)과 정답(Ground Truth)의 경계선 사이의 최대 오차를 양방향으로 확인하기 위함입니다.**

- **GT → Prediction**: 정답 경계에서 예측 경계까지 얼마나 떨어져 있는지
- **Prediction → GT**: 예측 경계에서 정답 경계까지 얼마나 떨어져 있는지

이 두 가지를 모두 봐야 **한쪽 경계가 정확하고 다른 한쪽은 많이 벗어난 경우를 포착할 수 있습니다.**

예를 들어, 예측이 전체적으로 정답보다 한쪽으로 치우쳐 있으면, 한 방향에서는 작은 값이 나오고, 다른 방향에서는 큰 값이 나옵니다.

따라서, **양방향 모두 최대 오차를 보는 것(Hausdorff Distance 본연의 의미)이 중요**합니다.

---

## ✅ 그런데… Backpropagation에는 쓰지 않습니다

**Hausdorff Distance는 보통 "성능 지표(metric)"로 사용되며**,

**Loss 함수로 사용되어 Backpropagation에 쓰이는 경우는 드뭅니다.**

왜냐하면:

- 거리 기반 연산이라 **미분 가능성이 떨어짐** (즉, gradient를 구하기 어려움)
- 오차의 최대값만 반영되므로 **훈련 안정성이 낮음**

→ 그래서 보통 **Dice Loss, Cross Entropy, Focal Loss** 등을 사용해서 학습을 진행하고,

**Hausdorff Distance는 모델 평가 단계에서만** 사용합니다.

---

## 🔁 요약

| 질문 | 답변 |
| --- | --- |
| 두 방향 모두 비교하는 이유? | 예측이 한쪽으로 치우치거나 불균형한 오차를 잡기 위해 |
| 오차를 확인하면 Backpropagation 하기 위한 건가요? | ❌ 아니요. Hausdorff는 주로 성능 평가 지표(metric)로 사용합니다. |
| 그럼 Loss로는 안 쓰나요? | 거의 쓰지 않지만 일부 연구에서는 soft approximation으로 사용하기도 합니다. |