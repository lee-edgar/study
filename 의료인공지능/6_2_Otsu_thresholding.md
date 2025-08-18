# 6.2. Otsu thresholding

threshoding은 문턱값이라고해서 어떠한 값을 정의해주고, 그 값보다 크거나 작은 부분들은 뽑아내주는 기법을 말함.

![image.png](/assets/의료인공지능/6_2_Otsu_thresholding/image.png)

threshod를 이용한 조건 설정 : 좌측 영상에서의 흰 부분(대략 밝기255정도?)을 추출하고 싶을때, 200보다 큰 밝기의 값을 추출하라고 한다면 200보다 밝은 값들은 1로 처리하고, 그러지 못한 값들은 0으로 처리하여 우측 영상처럼 해당 영역을 강조 할 수 있음.

- 보통의 threshold값을 manumal로 정해주기 마련인데, 자동으로 정하고 싶을때 Otsu threshoding 이라는 기법이 존재함.

### Ostu Thresholing

Ostu Thresholding은 이미지 이진화(binarization) 하는 대표적인 방법 중 하나임. 히스토그램 기반의 자동 임계값 선택 방식을 말하며, 의료 영상에서는 조직(organ), 병변(lesion), 종양(tumor) 등을 분리하는데 기초 단계로 많이 쓰임.

![image.png](/assets/의료인공지능/6_2_Otsu_thresholding/image_1.png)

> 히스토그램의 픽셀 분포(0~255)를 바탕으로, 두 클래스(배경, 객체)의 확률과 평균 차이에 따른 클래스 간 분산이 최대가 되는 임계값을 찾아 이미지를 자동으로 이진화하는 기법.
>