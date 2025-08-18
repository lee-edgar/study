# 10.5. Denoising with Dictionary[이해X]

### 딕셔너리가 고정되었다고 가정 하고, alpha값 구하기.

![image.png](/assets/의료인공지능/10_5_Denoising_with_Dictionary[이해X]/image.png)

이전 강의 Non-local Mean Denoising에서는 주변의 비슷한 패치들을 찾아서 패치 내부의 노이즈들을 없애주었습니다.

Denoising with Dictoionary는 패치들을 사전형태로 먼저 찾아 놓고, 특정 이미지가 들어왔을때 딕셔너리에서 비슷한 패치들을 가져와서 Denoising 하겠다는 아이디어를 가지고 학습의 개념이 들어가게  됩니다.

- Non-local mean denoising은 비슷한 patch를 지속적으로 찾아야하기 때문에 느림.
- Dictionary Learning은 Traninging은 시간이 걸릴 수 있지만 weight값을 찾기만 하면 되기에 Test에서는 빠른 결과를 보임.

![image.png](/assets/의료인공지능/10_5_Denoising_with_Dictionary[이해X]/image_1.png)

|y-x|가 작아야 원본 이미지 복원이 가능하고,

weight(alpha)가 sparse하다는 가정으로 x는 smooth한 영상이 만들어짐

왼쪽의 영상이 노이즈 낀 관측 영상, 오른쪽의 영상은 찾아내고 싶은 영상

노이즈 낀 관측 영상(observation을 깨끗한 영상으로 복원(reconstruction)

간단한 영상으로 알아보자.

![스크린샷 2025-06-18 16.50.45.png](/assets/의료인공지능/10_5_Denoising_with_Dictionary[이해X]/스크린샷_2025-06-18_16.50.45.png)

타겟 영상 y와 여러개의 딕셔너리(d1, d2,d3,d4,d5)가 있습니다.

딕셔너리 중에서 y값과 가장 코릴레이션이 높은, 비슷한 패치들을 고를 수 있습니다.

![스크린샷 2025-06-18 18.10.18.png](/assets/의료인공지능/10_5_Denoising_with_Dictionary[이해X]/스크린샷_2025-06-18_18.10.18.png)

d2가 가장 비슷한 패치로 뽑혔다고 가정해본다면,

                                                        resdual = | y - d2 * alpha(어떠한 값)|.

resdual의 최소화 하는 값. 즉, alpha(어떠한값)의 최소 값을 찾을 것 입니다. 

다시 resdual(d2), 최소화하고 남은 값에 대해서 가장 코릴레이션이 높고, d2를 제외한 d1, d3, d4, d5에 대해서 가까운 값을 찾게 됩니다.(d5)

![스크린샷 2025-06-18 18.16.40.png](/assets/의료인공지능/10_5_Denoising_with_Dictionary[이해X]/스크린샷_2025-06-18_18.16.40.png)

resiudal(d5)에 대해서 residual의 최소회 하는 값을 찾게 됩니다. 이러한 방식으로 alpha값들을 구하고, 딕셔너리와 alpha값들의 연산을 통해 X값을 얻게 됩니다. 여기서의 X는 y값과 같지 않습니다. 최소화 하는 값(residaul)을 가지는 과정에서 다양한 smooth한 패치들이 연산되기 때문입니다.