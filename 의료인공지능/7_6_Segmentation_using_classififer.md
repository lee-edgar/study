# 7.6. Segmentation using classififer

![image.png](/assets/의료인공지능/7_6_Segmentation_using_classififer/image.png)

정경에 대한 스크리블, 배경에 대한 스크리블을 주었을때 intenstiy distribution을 위와 같이 만들 수 있고, 모델을 가지고 각 점의 확률을 정의 할 수 있습니다.

![image.png](/assets/의료인공지능/7_6_Segmentation_using_classififer/image_1.png)

확률 값에 -log를 취해 에너지 식으로 정리하고, 에너지식의 Likeilhood term은  정경 스크리블, 배경 스크리블에 의해 정해지는게 아니고 학습 데이터를 바탕으로 만든 모델을 만들어냅니다.

![image.png](/assets/의료인공지능/7_6_Segmentation_using_classififer/image_2.png)

위 Test의 스크리블만을 가지고 만든 모델은 밝기 값으로만 만들었기 때문에 성능이 좋을 수 가 없습니다.

![image.png](/assets/의료인공지능/7_6_Segmentation_using_classififer/image_3.png)

- 반면에, Training data는 정확한 전경의 위치를 알고 있으며, 모든 전경의 밝기, 모든 배경의 밝기 값들을 전부 이용해 모델을 만들 수 있습니다. 다수의 데이터가 있으니 정보를 이용해 Foregound, background 모델을 만들 수 있습니다.
- 정교한 트레이닝 모델을 가지고 테스트 이미지의 각 pixel, voxel의 확률을 구하고 -log를 취해 Likelihood term을 정의하고 최적화를 통해 좋은 결과를 얻을 수 있습니다.

### Haar-like feature

위에서 Intensity model 기반으로 하여 feature extraction. 정교하게 확률 값을 구했는데, 위 방법 외에도 다양한 방법이 존재함.

haar-like feature : 다양한 filter를 사용해 filter에 맞는 해당 위치별 밝기 값들의 차이 값을 구함.

![image.png](/assets/의료인공지능/7_6_Segmentation_using_classififer/image_4.png)

- 밝은 영역의 intensity의 합 a
- 어두운 영역의 intensity의 합b

![image.png](/assets/의료인공지능/7_6_Segmentation_using_classififer/image_5.png)

![image.png](/assets/의료인공지능/7_6_Segmentation_using_classififer/image_6.png)

Harr-like filter를 이미지에 적용해보면, 위 영역에 대한 밝기 값의 합, 아래 영역에 대한 밝기 값의 합의 차이를 구할 수 있습니다. 위 사진에서의 절대값을 적용하면 많은 차이가 나는 것을 볼 수 있습니다.

![image.png](/assets/의료인공지능/7_6_Segmentation_using_classififer/image_7.png)

만약 아래 부분에 harr-like filter를 적용하면 차이가 0에 가깝게 나오게 될 것입니다.

하나의 필터만으로 구분하는게 어려우니, 다양한 필터들을 만들어 값을 구할 수 있습니다.