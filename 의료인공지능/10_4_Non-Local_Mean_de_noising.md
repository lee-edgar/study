# 10.4. Non-Local Mean de noising

# Non-local Mean Denoising

![스크린샷 2025-06-17 17.06.31.png](/assets/의료인공지능/10_4_Non-Local_Mean_de_noising/image.png)

Image self-similarity(유사성)

- 사각형 타일의 이미지 : 각각의 비슷한 점들의 similarity(유사성)을 계산해본다면 각각의 점들이 비슷하다고 추측을 할 수 있음.
- 아이디어는 노이즈가 없는 작은 특정 패치를 선정하고, 해당 패치와 높은 similarity를 가진 패치들만 사용한다면, 노이즈가 없는 패치들만 선택하여 weight sum을 통해 에러 및 노이즈를 없애겠다는 목적의 논문.

![스크린샷 2025-06-17 17.13.41.png](/assets/의료인공지능/10_4_Non-Local_Mean_de_noising/image_2.png)

타겟은 p pixel이라고 가정하고, 다양한 포인트들이 생기게 되는데, p와 q의 similarity를 비교하고, q주변의 neighborhood가 보라색으로 패치를 만들고, 결국 패치들 간의 similarity를 구하게 됨.

그 similarity가 d(Np, Nq)이고, exponeital 마이너스 function에 넣게 되었을때 두 패치가 완전이 같다면 1값을 가지는, 높은 웨이티를 가지게 됨.

결과적으로 특정 구간에 노이즈가 발생하더라도, weight sum을 통해 결과들이 average를 통해 노이즈가 줄어 들게 될 것임.