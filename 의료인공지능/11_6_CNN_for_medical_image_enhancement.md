# 11.6. CNN for medical image enhancement

Medical Image Super-Resolution

![스크린샷 2025-06-24 18.16.56.png](/assets/의료인공지능/11_6_CNN_for_medical_image_enhancement/image_1.png)

- MRI Super-resolution
    - 고해상도의 영상을 얻기 위해 스캐너에 상당히 오랜 시간동안 들어가 있어야합니다.
    보통의 mir 같은 경우 low resolution mri와 high resolution mri를 모으고, 사이에 네트워크 학습을 진행 할 수 있습니다. 즉, low resolution ~ network model ~ high resolution형태 구성을 말합니다. 해당 network에는 SRCNN, ResNet, DenseNet 등 알고리즘이 적용되었습니다.
    - mri 같은 경우 테슬라에 따라서 1.5T 스캐너, 3.0T 스캐너처럼, 자기장의 세기에 따라서 영상의 퀄리티가 달라지게 됩니다.
- CT reconstruction
    - MRI는 시간이 문제가 되는데, CT의 경우는 금방 영상이 나오게 됩니다만 방사선의 문제가 있습니다.
    Dose는 환자에게 조사되는 방사선의 양을 뜻합니다.
    - 높은 Dose CT는 노이즈가 적은 대신에, 많은 방사선량을 써서 얻어낸 영상을 말하고,
    낮은 Dose CT는 적은 방사선을 사용하는 대신에 노이즈가 많아져 해상도, 경계 선명도가 떨어지게 됩니다.
    - CT에서의 super resolution은 낮은 Dose의 CT를 네트워크를 통과하여 높은 Dose CT로 만들어내는 방법을 사용하겠습니다.

Medical Image Synthesis(의료 영상 합성)

![스크린샷 2025-06-24 18.43.49.png](/assets/의료인공지능/11_6_CNN_for_medical_image_enhancement/image_2.png)

- MRI - PET generation
    - MRI, PET 두가지를 같이 찍으면 스트럭쳐한 정보를 얻을 수 있습니다. 그 다음 신진대사 정보를 얻을 수 있으며, 실제 PET영상 같은 경우 아무래도 찍는데 번거로운 점이  꽤나 많기 때문에 mri와 pet 페어한 세트로 모아서 둘 사이의 관계를 찾아줄 수 있는 네트워크 학습을 하는 방식을 사용합니다. 추후에 mri만 들어오더라도 pet 영상을 잘 generation해줄 수 있어 유용합니다.
- Data generation for better training model
    - 실제 데이터를 이용하기 보다는 진짜와 같은 영상을 제너레이션 하는 연구들이 많이 진행 되고 있습니다.
    - 병원간의 영상이 다른 경우에도 노말라이제션으로 이러한 기법들을 사용 할 수 도 있습니다.