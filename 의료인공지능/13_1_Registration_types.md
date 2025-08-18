# 13.1. Registration types

feature 기반의 registration, intensity 기반 registration에 대해서 살펴보기.

대표적인 registration 기법 중  하나인 iterative closest point기법에 대해서 중점적으로    

Registration을 두 가지 기법으로 나눠볼 수 있습니다. 

1. Intensity Registration 기법
2. Feature Registration 기법

이전 강의에서 NCC, mutaul information을 통해서 patch들 간 유사도를 비교하는 방법에 대해 살펴보았습니다. → 이는 intensity 기반의 Registration 기법을 보통 많이 사용

![스크린샷 2025-06-30 18.04.00.png](/assets/의료인공지능/13_1_Registration_types/스크린샷_2025-06-30_18.04.00.png)

intensity 기반의 registration을 할때, 일정한 간격의 컨트롤 포인트 설정을 하고, 각 컨트롤 포인트별 대응점(correspondence)을 찾아주게 됩니다.

![스크린샷 2025-06-30 18.12.58.png](/assets/의료인공지능/13_1_Registration_types/스크린샷_2025-06-30_18.12.58.png)

특정 패치를 선택하고, fixed 영상에서 유사도가 높은 부분을 찾아 줄 수 있겠습니다. 우측(fixed)영상에서 translation, 로테이션 등의 여러 기법을 고려해 유사도가 높은 부분을 찾아낼 수 있습니다.

보통, 이러한 intensity기반의 정합(registration)기법들이 컴퓨테이션이 높습니다. 즉, 모든 컨트롤 포인트에 대해서 코레스 펀던스를 찾아주는 방식.

Feature Based Registration

![스크린샷 2025-06-30 18.56.33.png](/assets/의료인공지능/13_1_Registration_types/스크린샷_2025-06-30_18.56.33.png)

(상단의 일정한 패턴의 포인트는 intensity 기반, 하단의 x표시로 되어 feature 추출 표시가 feature based registration)

intensity 기반의 registration의 높은 컴퓨테이션 문제를 해결하고자 feature 추출 후 feature 기반으로 registration을 하는 방법.

feature 기반의 registration 방법에서는 moving, fixed 양 쪽의 feature를 뽑게됩니다.

이때, moving이미지와 fixed 이미지 간 서로 매칭 되지 않는 feature들이 추출 될 수 있습니다.

추출한 feature에서 moving과 fixed 이미지간의 매칭이 되는 것을 피쳐 매칭이라고 합니다.

feature matching 방법

1. feature descripter. 즉, Moving 이미지에서 먼저 feature를 뽑고
2. fixed 이미지에서 feature를 뽑고 
3. 뽑힌 피쳐들을 descripter 할 수 있는 각각의 moving, feature image에 맞는 feature descripter를 생성함
4. feature descripter들을 비교하여. feature matching해서 대응점(correspondence)을 찾는다.
5. ***대응점(correspondence)를 찾아주면서, 유사도가 높은 대응점(correspondence)들에 높은 weight를 줄 수 있으며, 반대로 유사도가 낮고, 매칭이 잘 안되는 항목에 대해서는 리젝션 처리 할 수 있음***

그래서, 로버스트한 대응점(correspondence)를 이용해 transformation matrix를 추정하기에, 해당 feature based registration은 intensity registration보다 빠른 속도.

피쳐 기반의 기법들이 속도가 빠르기에, 먼저 러프하게 피쳐 기반 정합을 통한 affine 변환, regid 변환 수행 하고 이후에 좀 더 정확한 정합을 위해. non-rigid 정합을 위해 인텐시티 기반 정합을 사용하기도 합니다.

피쳐 뽑는 방법

1. edge
2. corner
3. thresholding 기법을 활용한 segmentation