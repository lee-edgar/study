# 7.2. Atlas based method

![image.png](/assets/의료인공지능/7_2_Atlas_based_method/image.png)

                                          foreground(흰색)=1, background(검은색)=0

영상 취득 이후 앞에서 배운 방식들을 이용해 관심 부위의 segmentation을 진행 했을 때 Label Map을 얻을 수 있습니다.

위 작업을 반복해 데이터를 축적 및 저장 할 수 있으며, 이를 이용해주기 위한 기법으로 Atlas-based label fusion 기법이 있습니다.

![image.png](/assets/의료인공지능/7_2_Atlas_based_method/image_1.png)

Region Growing 기법 말고 기존의 영상과 Label을 이용해 test에서의 segmentation을 효율적으로 만드는 방법을 제시하며, segmentation 된 label map을 atlas라고 합니다.

![image.png](/assets/의료인공지능/7_2_Atlas_based_method/image_2.png)

1. segmentation하고자 하는 이미지를 X(우측) = x
2. 가지고 있던 이미지를 y1, y2(좌측 상단, 좌측 하단) = yi
3. 가지고 있던 이미지의 label을 z1, z2(중간 상단, 중간 하단) = zi

두 영상(x, (yi, zi)을 정합(registration)을 진행 할 수 있습니다.

 Registration의 다양한 기법을 이용해 영상을 Y로 옮겨줍니다.

보통의 Registration은 Transformation Matrix를 구한 후 이를 통해 Image를 변형합니다.

1. Y1 영상을 X로 옮기는 Transformation matrix를 구하고
2. Transformation matrix를 이용해 y1값을 변형해 y1’을 생성합니다.
3. 이때의 y1와 y1’은 비슷한 값을 보이게 됩니다.
4. y1과 y1’을 비슷하게 보이게 하기 위해 Transformation matrix의 값을 찾아주게 되는데,    이를 T(y1) = y1’, T(z1) = z1’ … T(yn) = yn’, T(zn) = T(zn’)으로 label에 대해서도 표현 할 수 있게 됩니다.
5. T(zn)=T(zn’)은 label 값이므로, 이미지 X에 대해 아래와 같이 label을 붙힐 수 있습니다.

![image.png](/assets/의료인공지능/7_2_Atlas_based_method/image_3.png)

1. 각 T(zn) = T(zn’)가 되는 n개 모두 X에 붙히게 되면 label이 다른 상태로 중첩되어 붙힐 수 있습니다. 이럴 경우 background 부분은 모두 0으로 나오고, foreground부분은 1로 라벨로 판단 할 수 있습니다. 

![image.png](/assets/의료인공지능/7_2_Atlas_based_method/image_4.png)

이때 N개의 background, foreground label을 voting하여 과반수가 넘는 label을 기준으로 하여 X에 대해서 분류 등 간단한 기법을 적용 해 볼 수 있습니다.

또는 X와Y’(정합 이미지) 간의 정렬 정도 또는 유사도를 나타내는 Similarity를 바탕으로 weight를 줄 수 있습니다. X와Y’간의 similarity가 가깝다면(높다면) label값인 z’에 weight를 주는 방식.

데이터가 아주 많다면 많은 정합을 해야하기에 composition이 높아지게 됩니다. registration이 높이기 위해서는 기법을 non-regid registration이라고 하는데, 이를 수행하게 되면 하나의 transformation으로 변형 되는게 아니므로 오랜 시간이 걸린다는 단점이 존재하기도 합니다.

### Patch-Based Label Fusion

composition이 높아지는 문제, non-regid registration의 오래 시간이 걸리는 문제를 해결 하기 위한 Patch-based Label Fusion이 존재합니다.

patch-based label fusion에서는 non-regid registration이 아닌 affine registartion을 사용합니다. 

Transformation matrix를 받는 속도가 빨라지게 되어 정확도 측면에서 떨어지게 되는데, 이를 극복하기 위해 Patch기반 weighted sum을 사용합니다.

![image.png](/assets/의료인공지능/7_2_Atlas_based_method/image_5.png)

좌측의 이미지에 패치를 만들어 X에 가져오게 되면 X에서는 위와 같이 표시가 될 것입니다.

![image.png](/assets/의료인공지능/7_2_Atlas_based_method/image_6.png)

![image.png](/assets/의료인공지능/7_2_Atlas_based_method/image_7.png)

X에 패치가 올라온 부분 위에 어떠한 window를 지정하고 패치들을 이동시키면서 similarity를 계산하게 됩니다. 패치가 오브젝트 가운데 위치하게 되면 similarity가 가장 높게 될 것이고, 외각 지역은 similarity가 낮게 표현 될 것입니다.

![image.png](/assets/의료인공지능/7_2_Atlas_based_method/image_8.png)

모든 patch와 similarity 간의 곱을 통해 실제 label을  구하면 되는데, Appearances(겉모습)가 비슷한 위치에 왔을때 그때의 레이블 값이 부각되게 됩니다.

n번째 이미지에 대해서도 동일하게 해당 모든 patch와 similarity간의 곱을 통해 label값을 구하고 그 값에 대한 sumation을 합니다. 그렇게 되면 전체 segmentation map이 얻어낼 수 있습니다. 

> 이 label fusion 기법은 사람마다 다르겠지만 전체적인 구조가 비슷한 장기에 대해서 잘 작동하는 모습을 보입니다.특별히 학습을 해주는 작업이 없어 이용하기에 상당히 쉽지만, 학습데이터가 많아질 수록 그에 비례해 계산량이 늘어나게 됩니다. registion도 비싼 작업이 될 수 있습니다.
> 
> 
> 그래서 보통 atlas가 많으면, atlas 중에서 유사도가 높은 atlas만 뽑아 작업을 수행하기도 합니다만, 이럴 경우 다수의 atlas 정보들을 다 사용하지 못할 수 도 있습니다.
>