# 7.3. Segmentation via learning based method

러닝 기반 기법.

![image.png](/assets/의료인공지능/7_3_Segmentation_via_learning_based_method/image.png)

pair한 이미지와, 라벨에 대한 트레이닝 데이터가 있습니다.

![image.png](/assets/의료인공지능/7_3_Segmentation_via_learning_based_method/image_1.png)

1. img → segmentation model → label :
    - img가 segmentation model을 거쳐 label 나오게 하는 것이 가장 직관적인 모델.
2. img → classification model → 각 점에 대한 prediction → 전체 prediction 집계 → label
    - 모델에 영상을 넣었을 때 classification과 같이 영상에 대한 한 점에 대한 prediction을 모든 점에 대해서 한다고 가정하면,
        
        prediction을 다 모아서 최종적인 label로 만들어 줄 수 있습니다. 이러한 기법도 러닝 기반 기법이라고 할 수 있겠습니다.
        
3. img → shape 추출 → 모델 기반 업데이트 → 최적 shape → label
    - 액티브 컨투어모델. 영상에서 쉐입에 대해서 업데이트를 하는 과정에서 어떤 모델에 의해 변형을 해줘 더 나은 쉐입으로 바꿔준 후 최종 레이블을 결정하는 이러한 방법도 러닝 베이스 기반이라고 할 수 있습니다.
    - active shape model이라고 불립니다