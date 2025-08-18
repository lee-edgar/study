# 13.6. Nonrigid registration via deformable model

스플라인을 이용한 전체적인 레지스트레이션 과정 살펴보기

보통은 non-rigid registartion을 수행하기 전에 affine 레지스트레이션을 먼저 수행하고, 주변부에서 컨트롤  포인트들의 코레스펀던스를 찾게 됨.

moving image → fixed image 변환

![image.png](/assets/의료인공지능/13_6_Nonrigid_registration_via_deformable_model/image.png)

intensity 기반에서 non-rigid registration을 수행하기 전에는 보통 affine registartion을 수행함. 혹은 이 영상이 같은 환자에게서 취득된 것이라고 하면, 보통 시뮬러리티 트랜스포메이션 매트릭스를 구해줍니다.

1. 트랜스포메이션 매트릭스를 세타라고 놓으면, 이 세타에 의해 영상 전체가 변환이 됨 → 영상이 얼추 로테이션이나, 큰 트랜슬레이션은 맞아떨어지게 됨
2.  이후 컨트롤 포인트를 추출하여 영상을 얼추 맞춰짐.  그 포인트들의 코레스펀던스를 찾아주게 됨.
    1. 컨트롤 포인트에 로컬한 패치를 추출했다고 했을때, 이것과 유사한 패치를 fixed 영상에서 찾아줘야 됨.
        
        ![image.png](/assets/의료인공지능/13_6_Nonrigid_registration_via_deformable_model/image_1.png)
        
    2. 찾아줄 때, 이미 1번 작업을 수행했기에 어느 정도의 range 안에서만 이 작업을 수행하게 됨
        
        ![image.png](/assets/의료인공지능/13_6_Nonrigid_registration_via_deformable_model/image_2.png)
        
    3. 어느 정도 영상이 맞춰주었다고 가정하고, fixed 영상의 일정 범위 내에서 이 컨트롤 포인트의 패치와 유사한 패치를 탬플릿 매칭을 하며 쭉 찾아주게 됩니다.
        
        ![image.png](/assets/의료인공지능/13_6_Nonrigid_registration_via_deformable_model/image_3.png)
        
        - template matching을 할 때, 저희가 배웠던 ssd, ncc를 사용 할 수 있음
        - 혹은 서로 다른 타입의 영상일 경우(모달리티가 다른) mutual information을 사용 할 수 있음
    4. c 단계에 의해 코레스펀던스로부터 시뮬러리티에 대한 코스트 구하기
        - 시뮬러리티에 대한 cost = (intensity(fixed image), transformation(moving image))
        즉, 코레스퍼던스(대응점)가 얼마나 비슷한지에 대한 것으로 코스트 정의 할 수 있다는 것임
        - 코레스펀던스가 얼마나 비슷한지에 대한 것으로 코스트를 정의 할 수 있음
    5. 레지스트레이션에서 항상 중요한 것이 이 컨트롤 포인트가 예를 들면, 해당 점에서 좌측 아래로 이동했다고 가정을 해봅니다. 추가로, 유독 한 포인트에 대해서 포인트가 정반대로 갔다고 가정(약간 이상한 상황이라고 볼 수 있음)
        
        ![image.png](/assets/의료인공지능/13_6_Nonrigid_registration_via_deformable_model/image_4.png)
        
          <가정 상황에 대한 영상>
        
        각각의 디포메이션 필드에 차이가 너무 크지 않도록 smooth 텀을 줄 수 있음.
        즉, 트랜스포메이션들의 코레스 펀던스로 찾기 위한 디포메이션 과정.
        
        ![image.png](/assets/의료인공지능/13_6_Nonrigid_registration_via_deformable_model/image_5.png)
        
        - 시뮬러리티가 높으면서, 스무스니스는 편차가(크지 않고 작으면 좋은)유지가 되면 좋음.
        따라서, 시뮬러리티에 대한 cost식에 마이너스를 붙히고, 람다를 더해 최종 코스트 식을 정의 할 수 있음.
        
        마이너스를 붙혔기 때문에, 이 값이 반대로 작아질수록 원하는 방향으로 만들 수 있음
        즉, 전체 식을 보면 전체c를 작게 해줄수 있도록 트랜스포메이션, 로컬한 트랜스 포메이션을 조정을 해줘야함.
        
    6. 업데이트 방법을 통해  컨트롤 포인트들의 코레스펀던스를 찾기.
        
        컨트롤 포인트들을 C라는 기호로 두고 gradient descient를 구하는 식. 컨트롤 포인트들을 계속해서 위와 같은 방식으로 업데이트 → C 값의 변화 → 미분값을 구하기
        위 방식을 통해 컨트롤 포인트들의 코레스펀던스를 찾을 수 있음
        
        ![image.png](/assets/의료인공지능/13_6_Nonrigid_registration_via_deformable_model/image_6.png)
        
3. 최종적으로 affine transformation과 컨트롤 포인트들이 각각 어디로 이동되게 되는지 다 디파인이 되면 디스플라인 인터폴레이션, 스플라인 방법으로 컨트롤 포인트 내부에 있는 부분(리샘플)을 백워드 와핑을 해서 인더폴레이션 처리 할 수 있음.

# Multi resolution

non-rigid registration에서 항상 문제가 되는 것이 컴퓨테이션임.

- affine 수행해도, 모든 컨트롤 포인트에 대한 코레스펀던스를 찾는데 시간이 걸리게 됨.
- 컴퓨테이션을 줄이기 위한 방법으로 multi resolution 기법을 사용 할 수 있음

moving, fixed 영상을 반으로 줄여서 레졸루션을 작게 만듦

![image.png](/assets/의료인공지능/13_6_Nonrigid_registration_via_deformable_model/image_7.png)

그 상태에서 컨트롤 포인트를 러프하게 잡을 수 있음

![image.png](/assets/의료인공지능/13_6_Nonrigid_registration_via_deformable_model/image_8.png)

러프하게 잡은 컨트롤 포인트들을 가지고, 레지스트레이션의 스탭, 어파인 트랜스폼, 컨트롤 포인트들의 매칭점. 최종적으로 복원하는, 복원 해낸 영상을 만들어내는 과정이 상당히 빠르게 동작하게 만든 후 컨트롤 포인트들을 늘려주게 됨

![image.png](/assets/의료인공지능/13_6_Nonrigid_registration_via_deformable_model/image_9.png)

어느정도 레즈스트레이션이 된 걸 바탕으로 위에 레졸루션으로 올라옵니다.

그리고, 다시 러프한 컨트롤 포인트들을 잡고 같은 과정을 수행

![image.png](/assets/의료인공지능/13_6_Nonrigid_registration_via_deformable_model/image_10.png)

여기서 중요 포인트는 어느 정도 여기서 아래 레벨에서 맞췄기 때문에 이 컨트롤 포인트에 써치 레인지를 더 줄여주는게 관건이고, 이후 앞에서 했던 과정들을 반복하며 원본 사이즈로 올라가 작업을 수행하게 됨.