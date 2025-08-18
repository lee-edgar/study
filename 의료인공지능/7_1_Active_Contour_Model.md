# 7.1. Active Contour Model

![image.png](/assets/의료인공지능/7_1_Active_Contour_Model/image.png)

Graph Cut처럼 특정 픽셀의 정경과 배경을 정해주는 방식 아닌 관심 물체 근처에 러프한 바운더리를 그려주는 방식.

![image.png](/assets/의료인공지능/7_1_Active_Contour_Model/image_1.png)

경계가 점차 업데이트 되면서 세그멘테이션이 진행 되고, 가장 우측과 같이 원하는 부분까지의 바운더리로 수렴하는 모습을 볼 수 있음.

![image.png](/assets/의료인공지능/7_1_Active_Contour_Model/image_2.png)

각각의 점들로 경계 바운더리를 표현할 수 있음

 V(1) = (x1, y1), V(2) = (x2, y2)  …   V(n) = (xn, yn)

Active Contour Model은 이 점들의 집합에 대한 식을 정의함.

![image.png](/assets/의료인공지능/7_1_Active_Contour_Model/image_3.png)

![image.png](/assets/의료인공지능/7_1_Active_Contour_Model/image_4.png)

위와 같이(5점, 1점 등)원하는 결과의 바운더리에 우리가 만든 경계가 놓여 있을때 최솟값이 나오도록 식을 정의 할 수 있음.

에너지 이큐에이션을 통해 정의하여 이 식을 최소화 하는 최적화를 진행 해 볼 수 있음

![image.png](/assets/의료인공지능/7_1_Active_Contour_Model/image_5.png)

여러개의 V(s)값들의 V포인트에 대한 집합으로 E(에너지)로서 정의하고 모든 s에 대해서 에너지를 더한 최종 값 에너지 Esnake를 정의하게 됨. 이때 snake는 업데이트 되는 커브 모양이 뱀과 같이 생겼다고 해서 snake 에너지식 이라고 하기도 함.

우선, E(V(s))에 대해서 정의해야하는데, 사용자가 원해는 대로 약간의 수정이 가능함.

### Edge-based Externel Energy

![image.png](/assets/의료인공지능/7_1_Active_Contour_Model/image_6.png)

일반적으로 세그멘테이션을 위해 쉽게 해볼 수 있는 가정 :  ‘경계가 뚜렷한 곳에서의 바운더리가 생길것이다’.

경계에서 뚜렷하게 그레디언트 차이가 나는 것을 볼 수 있음.

그레디언트의 스퀘어 값을 수식으로 만들게 되면, 경계가 클때 에너지가 커지게 됨

모든 포인트에서 에너지 엣지의 값을 구해 합치면, 총 에너지 식을 구할 수 있음.

아마도 그레디언트가 큰 곳에서는 마이너스 값이 커지게 되고, 이 점들이 그레디언트가 큰 곳으로 가게되면 전체적인 에너지 값이 줄어들게 되는데, 

$$
Eedge​=−∣∇I(x,y)∣2
$$

> 요약부. 그레디언트가 큰 영역(경계 부근)에서는 E(edge)값이 더 작아지므로, snake가 그 쪽으로 끌려가게 됩니다.
> 

> 요약부. gradient가 차이가 나는 경계가 뚜렷한 영역에서는 영상의 gradient 크기가 커지므로 이 값을 음수로 사용하는 에너지 항은 해당 위치에서 더 작아지게 됩니다. Snake curve는 전체 에너지를 최소화 하려 하기 때문에, 자연스럽게 경계 쪽으로 끌려가게 됩니다.
> 

### Line-based External Energy(Intensity). 경계 대비 기반이 아닌, 픽셀(intensity) 자체를 기반으로 한 에너지 정의

![image.png](/assets/의료인공지능/7_1_Active_Contour_Model/image_7.png)

예를 들어, 흰색 배경에 검은색 물체가 있다고 가정함.(위는 흰배경에 검은 물체, 아래는 검은 배경에 흰 물체)

흰색 부분은 255값이겠고, 검은색 물체의 바운더리 부분은 0 가까운 값이 될 것 입니다.

위와 같이 영상에서 영역화 하고 싶은 물체의 특징을 생각해 인텐시티를 정의한 에너지를 Extenral Energy라고 함.

에너지 항 예시 : 

$$
Eline​=±I(x,y)
$$

밝은 영역(255) 혹은 어두운 영역(0)을 선호하는 모델 설계 가능( foreground / background 차이에 따라 ± 선택) 

> 밝은 배경에 어두운 물체라면, 어두운 영역으로 끌어들이기 위해 $Eline​=I(x,y)$와 같은 식을 사용하고, 반대로 어두운 배경에 밝은 물체는 마이너스 intensity. $Eline​=−I(x,y)$를 정의 할 수 있습니다.
> 
> 
> 이러한 (위와 같은) 에너지 항들은 외부 이미지 특성에 따라 snake를 유도하기 때문에 External Energy에 해당합니다.
> 

$$

$$

### External Energy만으로 발생하는 한계

External Energy만으로 결과가 잘 나오면 좋은데 그러지 못함.

![image.png](/assets/의료인공지능/7_1_Active_Contour_Model/image_8.png)

위쪽의 화살표에서는 타겟 경계를 잘 찾을 수 있지만,

좌측 하단의 포인트 부분은 반대쪽으로 잘못된 경계를 찾게 될 수 있는데, 그렇게 되면 물체의 쉐입이 내가 원화는 쉐입이 아니게 될 수 있으며, 업데이트가 멈추는 문제가 발생할 수 있음

> 수정부. 외부 에너지에만 의존할 경우, 영상의 일부 영역에서 경계가 약하거나(강한 엣지가 없거나), 잡음이 있을 때 잘못 된 위치로 수렴하거나 수렴이 멈추는 경우가 있습니다. 이런 문제를 보완하기 위해 곡선 형태적 특성(쉐입과 모양)을 반영하는 Internal Energy 항이 필요합니다.
> 

### Internal Energy(스무스한 곡선 유지)

![image.png](/assets/의료인공지능/7_1_Active_Contour_Model/image_9.png)

위 쉐입만을 가지고 에너지를 정의하는데. 예를 들어 가까운 이웃 점들은 서로 비슷한 위치일 확률이 높기에 snake의 부드러움을 유지하는 특징을 식에 반영 할 수 있습니다.

![image.png](/assets/의료인공지능/7_1_Active_Contour_Model/image_10.png)

왼쪽의 경계가 울퉁불퉁하고, 복잡한 쉐입의 이미지에 Internal Energy를 작용해 오른쪽의 부드러운(스무스한) 경계의 쉐입으로 수렴하는 예시를 볼 수 있습니다.

> 정리.
Active Contour Model은 초기 곡선을 시작으로 이미지의 경계에 맞게 점차 수렴해 나가는 방식의 segmentation 알고리즘입니다.
외부 에너지(External Energy)는 이미지의 경계, 밝기 등으로 기반하여 snake를 유도하며,
내부 에너지(Internal Energy)는 곡선의 부드럼움과 연속성을 유지할 수 있습니다.
가장 흔한 외부 에너지는 gradient 크기를 사용하는 edge-based 방식이며, intensity 기반에서 사용됩니다.
하지만 외부 에너지 만으로는 불완전 할 수 있어, 내부 에너지 항을 통해 불필요한 굴곡을 억제하고 스무스한 결과를 유도합니다.
이러한 에너지 최소화 방식은 수치해석을 통해 반복적으로 곡선을 업데이트하며 최적의 경계를 찾아 낼 수 있습니다.
>