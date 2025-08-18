# 13.5. Nonrigid Registration via B-spline

살짝 복습.

![스크린샷 2025-07-04 23.15.08.png](/assets/의료인공지능/13_5_Nonrigid_Registration_via_B-spline/스크린샷_2025-07-04_23.15.08.png)

각각의 포인트마다 interploation을 하게 되면 computation이 높다.

1. intensity interpolation(좌측)
- 0, 1을 각각의 컨트롤 포인트라고 두고. fixed 영상에서 매칭되는 매칭점들을 찾을 수 있다.
- 첫번째 포인트의 값이1이고, 두번째 포인트의 값이 5라고 한다면, 단순히 리니어 하게 중간 값을 3이라고 유추해볼 수 있음
1. Cubic interploation (우측)
    - 0과 1의 값이 주어질때, -1, 2값을 추가하여, 라인에 대해서 에스티메이션

Spline based Registration

![스크린샷 2025-07-04 23.24.17.png](/assets/의료인공지능/13_5_Nonrigid_Registration_via_B-spline/스크린샷_2025-07-04_23.24.17.png)

좌측의 moving을 바탕으로 fixed image의 매칭점들을 찾을 수 있음

![스크린샷 2025-07-04 23.25.57.png](/assets/의료인공지능/13_5_Nonrigid_Registration_via_B-spline/스크린샷_2025-07-04_23.25.57.png)

moving 점들이 x,y축으로 이동된 x값을 찾아 줄 수 있습니다. 찾아군 값을 바탕으로 이 식을 define을 합니다.

![스크린샷 2025-07-04 23.27.40.png](/assets/의료인공지능/13_5_Nonrigid_Registration_via_B-spline/스크린샷_2025-07-04_23.27.40.png)

define하는 과정에서 위 moving의 네 점으로 디파인을 하는게 아닙니다. 스플라인 기반 기법의 경우 컨트롤 포인트 주변의 16개의 포인트를 이용해 디포메이션 하여 사각형 내의 어떤 점들의 변화를 예측 하게 됩니다.

![스크린샷 2025-07-04 23.29.34.png](/assets/의료인공지능/13_5_Nonrigid_Registration_via_B-spline/스크린샷_2025-07-04_23.29.34.png)

사각형 내의 어떤 점들 사이에 위치한 중간의 점들의 이동은 이미지 처럼 될 것입니다

위 내용들은 컨트롤 포인트들의 매칭점을 안다고 가정했을 때, 디포메이션을 바탕으로 컨트롤 포인트 사이 점들이 어떻게 변화되는지를 알 수 있습니다.