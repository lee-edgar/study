# 8.5. Segmentation using 3D CNN

![image.png](/assets/의료인공지능/8_5_Segmentation_using_3D_CNN/image.png)

3D CNN에서 V-Net을 사용했을 때의 구조.

아래로 내려가는 것은 Max Pooling 2배를 적용 한 것 이므로 1/2로 변화되는 모습을 보이며, Channel은 2배씩 증가 됨.

예시, 원본 128x128x64에 3x3x3의 필터 16개를 적용하고 컨볼루션하게 되면, 

downsampling ~

1. 128x12x64x1 → conv(3x3x3x16) → 128x128x64x16
2. 128x128x64x16 → maxpool(2x2x2) → conv  3x3x3x32 = 64x64x32x32
3. 64x64x32x32 → maxpool(2x2x2)→ conv 3x3x3x64 = 32x32x16x64
4. 32x32x16x64 →  maxpool(2x2x2) → conv 3x3x3x128 = 16x16x8x128
5. 16x16x8x128 →  maxpool(2x2x2) → conv 3x3x3x256  =8x8x4x256

upsampling ~ 최종 128x128x64(u-net에서 prediction하면 조금 작아지긴 함)

1. 8x8x4x256 → upconv(2x2x2) = 16x16x8x128 → concat(skip step4) =16x16x8x256 → conv(3x3x3x128) = 16x16x8x128
2. 16x16x8x128 → upconv(2x2x2) = 32x32x16x64 → concat(skip step3) =32x32x16x128 →
 conv(3x3x3x64) =32x32x16x64
3. 32x32x16x64 → upconv(2x2x2) = 64x64x32x32 → concat(skip step2) → 64x64x32x64 →
conv(3x3x3x32) = 64x64x32x32
4. 64x64x32x32 → upconv(2x2x2) = 128x128x64x16 → concat(skip step1) → 128x128x64x32 →
conv(3x3x3x16) = 128x128x64x16
5. 128x128x64x16 → conv(1x1x1xn_casses) = 128x128x64x(n_class)

> 원본 128x128x64에 3x3x3 필터 16개를 적용하고 컨볼루션 하게 되면 downsampling 1~5단계에서 공간은 1/2씩 줄고, 채널은 2배씩 증가함. 
이후 upsampling 경로에서는 반대로 공간은 2배씩 복원되며, encoder의 feature map과 concat되어 skip connection이 형성되고 최종 128x128x64x(n_classes) 형태의 segmentation map이 생성 됨.
> 

### Patch-wise segmentation

![image.png](/assets/의료인공지능/8_5_Segmentation_using_3D_CNN/image_1.png)

V-Net과 같은 3D Segmentation 네트워크는 대용량 영상 처리에 있어 patch 단위로 학습하는 방식이 일반적입니다.

하지만, 이 경우 전체 영상에서의 위치 정보나 장기 간 구조적 관계 등 전역적인 맥락이 손실 될 가능성이 있습니다.

모델이 영상의 전체적인 구조나 맥락을 이해하지 못하게 만들며 정확한 경계 예측이나 위치 기반 판단에 한계를 초래 할  수 있어, 전역 정보 보존을 위한 다양한 기법들이 연구되고 있습니다.