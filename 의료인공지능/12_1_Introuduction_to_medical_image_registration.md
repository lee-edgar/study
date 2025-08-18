# 12.1. Introuduction to medical image registration

registration은 두 영상 간의 매칭점들을 찾아주고, 그 매칭점들을 바탕으로 Transformation matrix를 예측하고, 예측된 Matrix를 바탕으로 영상을 변환해주는 과정

Image Registration(정합)

- 서로 다른 각도, 스케일 혹은 다른 위치에 잇는 두 영상을 서로잘 맞게끔 맞춰주는작업.

![image](/assets/의료인공지능/12_1_Introuduction_to_medical_image_registration/image_1.png)

(3차원의 영상)3년 전의 건강검진, 올해의 건강검진의 결과를 보고 3년간의 결과를 의사들이 비교해가면서 확인하는 작업은 꽤나 오랜 시간이 걸림 → 같은 type, subject이 시간에 따라서 어떻게 변화하는지 알아보기 위해 정합으로 처리

- 시간에 따라서 어떠한 변화가 있는지 알아보는 스터디를 longitudinal study를 하고, 이 과정에서 정합이 필요합니다.
- 이 외에도 같은 사람에서의 같은 서브젝트에 대해서 다른 타입의 영상을 취득 할 수 도 있습니다.
    
    → 예를 들어, mri를 찍으면서 동시에 PET 영상을 찍는 경우
    

PET만 봐서는 실제 activation만을 보고, 실제 뇌에서의 어느 부분인지 정확하게 알기가 힘든데 다른 타입의 영상을 잘 맞춰가게되면, MRI의 특징으로 실제 뇌에서의 위치를 파악 할 수 있습니다.

- MRI의 경우 구조적인 정보.
- PET의 경우 신진대사 정보.

Label fusion

여러 사람들의, 다수의 mri 영상들을 모아서 평균 뇌의 지도를 만드는 경우에, 서로의 정합을 먼저하고 뇌의 특정 부위에서는 어떠한 특정 변화가 있는지 알아내는 연구를 할 수 도 있습니다.

혹은, 일정 데이터에 대한 레이블을 가지고 있다고 할 때, 레이블을 바탕으로 새로운 사람의 영상이 들어왔을 때, 레이블 퓨전을 쓴다던지 혹은 학습 기법을 통해 영상을 자동으로 분석해주는데 있어서 정합이 사용 될 수 있습니다.

![스크린샷 2025-06-25 13.19.00.png](/assets/의료인공지능/12_1_Introuduction_to_medical_image_registration/image_2.png)

transformation matrix : 전통적으로 매칭점들을 찾고 이들간에 변형을 표현해 줄 수 있는 트랜스포메이션 매트릭스 찾아서 정합을 수행하는 방법

iterative closest point(ICP) : transformation matrix를 찾기 위해 매칭점들을 찾는 아이디어

- rigid, non rigid, affine등의 변환들이 있습니다.