# 5.5. Weekly Supervised Learning

![image.png](/assets/의료인공지능/5_5_Weekly_Supervised_Learning/image.png)

고비용 라벨링 없이 의료 영상 데이터를 효과적으로 학습시킬 수 있는 방법

의료 영상 분야에서의 이점

1. 라벨링 비용 절감
    - 픽셀 단위 segmentation이나 병변 윤곽선 라벨링은 방대한 시간과 전문의의 노력이 필요합니다.
    - **약지도 학습은 이미지-level 또는 일부 annotation만으로도 학습이 가능**하여 비용과 시간을 크게 절감할 수 있습니다.
2. 데이터 확보 용이
    - 실제 의료기관에서 대규모로 보유하고 있는 데이터는 대부분 **텍스트 진단 기록**이나 **전체 이미지에 대한 판정값(class-level label)**입니다.
    - 이러한 **불완전한 라벨을 활용해도 성능을 낼 수 있다는 점이 큰 장점**입니다.
3. 실제 임상 환경 반영
    - 현장에서는 항상 완전한 정답이 존재하지 않으며, **진단 기록이나 report 기반 정보만 존재하는 경우가 많음**.
    - 약지도는 이런 **실제 임상 데이터를 활용할 수 있는 유연한 방식**입니다.
4. 소량의 정밀 라벨 + 대량의 약라벨 혼합 활용(semi-supervised)
    - 일부 정밀 annotation + 많은 약 annotation을 혼합하여 높은 성능을 달성할 수 있습니다.

의료 영상에서의 주요 활용 사례

1. **병변 분할 (Lesion Segmentation)**
    - 예: 간암, 폐 결절 등에서 **"이 이미지에 병변 있음"** 수준의 라벨만 사용하여 병변 위치까지 추론
    - 기술: **CAM (Class Activation Map)** 기반 localization 기법 활용
2. **암 검출 (Detection)**
    - 암 여부만 라벨링된 CT/MRI 데이터를 이용해 **암 위치까지 예측**하도록 학습
    - 예: 유방암, 폐암, 대장암 CT
3. **기기 판독 자동화**
    - 예: 심전도, 초음파 영상 등에서 전면적 pixel-level 라벨 없이 진단 기록만으로 학습
4. **스크리닝 시스템 구축**
    - 대량의 low-quality report 기반 영상 데이터를 학습하여 **1차 스크리닝 시스템** 구축
    

이상이 있는 병변 부위를 bbox로 detection하거나 segmentation을 해주는데 이를 weakly supervised learning이라고 함.

weakly supervised learning  문제

- image label을 통해 training을 하고 test시 bounding box, detection 문제
- bounding box, segmentation을 위해 pixel label을 붙혀야 하는 문제(단순 bounding box는 쉬워서 weakly supervised learning이 아님)