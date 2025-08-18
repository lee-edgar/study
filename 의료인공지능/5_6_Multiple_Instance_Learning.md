# 5.6. Multiple Instance Learning

![image.png](/assets/의료인공지능/5_6_Multiple_Instance_Learning/image.png)

Multiple Instance Laerning의 문제 : test 열쇠 꾸러미로 열 수 있나? 없나? 를 맞추는 것.

1번째 줄의 열쇠 꾸러미로 문을 열 수 있다 → postive trainging sample 이라고함.

2번째 줄의 열쇠 꾸러미로는 문을 열 수 없다 → Negative training sample 이라고함.

![image.png](/assets/의료인공지능/5_6_Multiple_Instance_Learning/image_1.png)

작은 패치가 있는 영상을 통째로 넣어주기 보다는 작은 패치를 탐지 할 수 있는 classififer를 만들어 최종 전체 영상의 레이블을 결정한다.

열쇠꾸러미 예시를 들때, 하나의 열쇠만 맞으면 문이 열리듯이, 위 cancer1에서의 4개의 패치 중 하나의 패치가 cancer일 경우 cancer라고 판단을 내릴 수 있음.

Instance classifier가 잘 작동하게 되면 실제 영상에서 어떤 부위에 cancer가 있는지 까지 맞출 수 있기에 어느 정도 Weakly supervised Learning 문제와도 상당히 연관성이 깊다고 볼 수 있음.

> 영상 단위 레이블이 있을때, 그리고 어떠한 병변이 작을 때 patch를 이용한 Multiple Instance Learning을 이용해주는게 효과적일 수 있다.
>