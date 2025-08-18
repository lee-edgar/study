# 6.1. Introduction to medical image segmentation

![image.png](/assets/의료인공지능/6_1_Introduction_to_medical_image_segmentation/image.png)

segmentation은 시간 차를 두고(longitudinal study) 어떤 영역에 대해서 어떠한 변화가 일어났는지 혹은 특정 장기, 종양, 영역 등을 알 수 있으며 진단하는데 있어 판단의 근거가 되기도 합니다.

![image.png](/assets/의료인공지능/6_1_Introduction_to_medical_image_segmentation/image_1.png)

segmentation 기법들.

- thresholding, region growing : 영상의 특정 밝기 값, 컬러 값 정보를 바탕으로 segmentation 수행.
- graph cut, active contour model :  영상의 정보와 prier의 정보를 이용함(특정 영역이 스무스 해야한다 던지.. )

classification에서는 대부분 학습 기법에 대해서 공부했다면, segmentation은  active shape model을 학습해서 그 결과를 얻어내는 그런 기법.

- activate shape model, FCN, U-Net, DeepLab들은 딥러닝 기반이라 트레이닝 데이터가 필요함.