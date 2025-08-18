# 5.3. Feature extracting using Deep Learning

![image.png](/assets/의료인공지능/5_3_Feature_extracting_using_Deep_Learning/image.png)

하나하나의 Fixel 값 혹은 Voxel값이 input feature가 되고, 이것들 중에서 유용한 feature를 추출하는 것을 feature Extraction이라고 함.

x1의 컬러값, … n의 컬러값 + 3채널의 RGB까지 더한 모든 score 정보들을 모은것이 feature가 됩니다. 이후 기존의 feature 모음을 기반으로하여 유용한 feature들을 새롭게 추출하는 방법을 feature extraction이라고 합니다.

![image.png](/assets/의료인공지능/5_3_Feature_extracting_using_Deep_Learning/image_1.png)

- 100x100영상이 있고, x1부터 x10000까지의 10000개의 데이터가 100개가 있다고 가정합니다. 이러한 데이터로부터 피처의 개수를 extraction하여 줄여서 z1부터 z100까지의 100개로 줄여나갑니다. 이를 dimensionality reductor, unsupervise learning이라고함.
- 이 feature들은 어떠한 특정 레이블을 잘 찾기 위해서 만들어진 feature가 아니고 원본 데이터를 잘 표현 할 수 있는 특징을 찾는 문제가 됨.
- 영상 데이터에서 언뜻 보기에는 구분이 어려울 수 있는데, 전체 100개의 subject를 보았을때 색깔 분포, 셀들의 shape의 변화를 본다던지 등 데이터들을 리프리젠테이션 해줄 수 있는 feature들이 추출이 되는데, 대표적인 기법으로 PCA(Principle Component Analysis), Auto-Encoder 등이 있음.

![image.png](/assets/의료인공지능/5_3_Feature_extracting_using_Deep_Learning/image_2.png)

- Auto Encoder는 Dimensionality reduction(차원 축소)를 통한 stacked Neural Netowrk를 통한 Encoder feature들을 이용하여 DEcoder를 한 결과가 원본 이미지와 같도록 하는 기법
- 6개의 input, 1개의 bias → 적은 수의 hidden layer node(3개 + 1bias)→ 6개의 output을 주어 input과 동일하게 맞춰주고, loss를 계산하여 다시 back-propagaion하여 내부의 파라미터를 업데이트해주게 됨.

![image.png](/assets/의료인공지능/5_3_Feature_extracting_using_Deep_Learning/image_3.png)

6개의 input feature 100개 → encoding → 3개의 노드 100개를 생성 → decoding → 6개의 out feature 100개 생성하고, 이후 out feature를 바탕으로 다시 node를 생성해 더 적은 수, 더 많은 수의 output feature를 만들어 확장해나갈 수 있음. 

![image.png](/assets/의료인공지능/5_3_Feature_extracting_using_Deep_Learning/image_4.png)

한번에 너무 적은 수의 피처로 줄이게 되면 많은 정보 손실이 발생방지를 위해 stack auto encoder 구조를 사용하여 extracion하기도 함(*feature 변화 : 1000→500→30→500→1000)

> 의료 영상데이터들은 3차원일 경우가 많아 사이즈가 매우 커서 그대로 학습 할 수 없어 feature를 여러가지 feature extraction, Dimensionality reduction(차원 축소)를 feature를 줄여 classification을 함.
>