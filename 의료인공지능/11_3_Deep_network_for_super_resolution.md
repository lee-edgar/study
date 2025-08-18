# 11.3. Deep  network for super resolution

처음 제안된 super resolution의 경우 layer가 3가지만 이용 가능 했었음.

이 연구는 서울대학교 연구팀에서 제안됨

![스크린샷 2025-06-20 22.15.10.png](/assets/의료인공지능/11_3_Deep_network_for_super_resolution/image_1.png)

SRCNN과 비슷한 구조를 가지고 있습니다.

처음에는 작은 크기의 LR에서 인터폴레이션을 진행하여 같은 사이즈의 LR영상과 HR영상을 생성하고, 다수의(20개의) 컨볼루션 레이어를 사용합니다

![스크린샷 2025-06-20 22.50.50.png](/assets/의료인공지능/11_3_Deep_network_for_super_resolution/image_2.png)

### 1. resiudal

20개의 layer를 통과해서 나오는 output인 residual과 LR영상을 더해서 최종적으로 HR 영상을 만들게 됩니다.

LR에서 바로 HR 영상을 만드는 것보다는, 중간에 residual을 이용해 HR영상을 만들어냅니다. 

- residaul은 아무래도 만들어야할 정보가 많지 않기 때문입니다.
- 이후 많은 네트워크 모델에서 residual learning이 많이 사용됩니다.

### 2. gradient clipping

> ***어떠한 threshold값을 정하고, 어떠한 gradient가 threshold보다 크다면, threshold 값 정도 까지만 업데이트 되게끔 강제하는 것이 gradient clipping 기법.***
> 

이 연구에 대한 논문에선 SRCNN이 학습을 할 때 너무 오랜 시간이 걸린다는걸 지적합니다.

학습이 오래걸린다는 것은 어쩌면 learning rate를 결정해야한다는 말이기도 합니다.

learning rate가 너무 작으면 수렴 속도 ↓, 너무 높으면 발산 확률 ↑ 의 문제가 발생하게 되는데, 이때 gradient clipping를 사용할 수 있습니다

![스크린샷 2025-06-20 22.52.19.png](/assets/의료인공지능/11_3_Deep_network_for_super_resolution/image_3.png)

- 해당 점에서의 gradient를 구하게 되면, gradient는 별로 크지 않습니다

![스크린샷 2025-06-20 22.55.00.png](/assets/의료인공지능/11_3_Deep_network_for_super_resolution/image_4.png)

- 두 번째 포인트에서의 gradient를 구하게 되면 gradient가 상당이 크게 됩니다. 이 상황에서 알파 값도 크다면, 꽤나 큰 간격으로 점프 될 가능성이 있습니다.
- 이와 같은 문제를 방지하기 위해 gradient clipping 사용.

> ***어떠한 threshold값을 정하고, 어떠한 gradient가 threshold보다 크다면, threshold 값 정도 까지만 업데이트 되게끔 강제하는 것이 gradient clipping 기법임.***

그래서, gradient clipping 기법을 사용 할때는 상대적으로, 알파값과 learning rate값을 크게 설정하기에 gradient가 작을 경우 빠르게 움직이게 됩니다. 
SRCNN의 경우 알파 값이 작기에, 수렴하는 속도가 느려 학습이 느리다라고 주장합니다.
알파 값을 크게하면 발산 등의 문제를 clipping으로서 해결한것입니다.
> 

# Laplacian Pyramid Network

![스크린샷 2025-06-20 23.07.41.png](/assets/의료인공지능/11_3_Deep_network_for_super_resolution/image_5.png)

                                             녹색 화살표 : upsamlpling, 붉은색 화살표 : CNN

딥한 네트워크를 사용하면서, 처음부터 업샘플링을 진행하는게 아니라 업샘플링 하는 네트워크를 넣어주어 단계적으로 업샘플링을 진행합니다. 또한, 업샘플링 네트워크 사이에 CNN 네트워크를 다수 사용합니다.
***원하는 최종 해상도까지 단계적(pyramid)으로 CNN → upsampling의 반복***

![스크린샷 2025-06-20 23.12.39.png](/assets/의료인공지능/11_3_Deep_network_for_super_resolution/image_6.png)

1. **각 스테이지의 업샘플 출력**
    - 단계별로 업샘플된 영상(아래쪽)과,
    - 같은 레벨에서 CNN이 예측해낸 **잔차(residual)** 맵(위쪽 파란 블록)이 준비됩니다.
2. **잔차 추출 & 합산**
    - “업샘플된 영상 + 그 단계에서 예측된 잔차”를 더해 주면
    - 원본에 좀 더 디테일이 살아난 중간 해상도가 완성됩니다.
3. **다음 단계로 전달**
    - 합쳐진 중간 해상도를 다시 **다음 레벨의 입력**으로 사용
    - 또 CNN → 업샘플 → 잔차 합산 과정을 거칩니다.
4. **최종 출력**
    - 피라미드의 맨 꼭대기(가장 고해상도)까지 올라오면
    - 각 단계의 잔차들이 모두 반영된, 최종 고해상도 영상이 완성됩니다.

업샘플링 된 것(아래 영역)과 중간에 업샘플링 된곳에서(위쪽 영역의 파란색 부분의 업샘플링 레이어)의 feature map으로 부터 estmation 한 residaul을 sum 이후 최종 scale 영상이 만들어 지게 됩니다. 이때 여러번의 업샘플랭 레이어에서의 resiudal하는 과정을 순회하면서 최종 에스티메이션한 레지듀얼과, 업샘플링을 통해 얻은 해상도를 합쳐 결과를 내는 방식입니다.