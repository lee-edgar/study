# 7.4. Principle Component Analysis(PCA) NP

PCA는 데이터의 차원을 줄일 때 많이 사용 됩니다.

데이터를 투영 했을 때 분산은 Maximize하는 분포를 찾는 것이 주 목적입니다.

![image.png](7%204%20Principle%20Component%20Analysis(PCA)%20NP%2020234bdbf13d8012b6f9d7e571f461e8/image.png)

2차원 x1축, x2축이 1차원 z1축으로 차원을 줄일 수 있습니다.

![image.png](7%204%20Principle%20Component%20Analysis(PCA)%20NP%2020234bdbf13d8012b6f9d7e571f461e8/image_1.png)

2차원의 x2축을 삭제하고, 각 포인트들을 x1축으로 투영 할 수 있습니다. 파랜색 X 포인트와 검은색 X포인트의 간격이 매우 좁은 걸 볼 수 있습니다. 

PCA목표는 위와 같이 데이터를 한 축의 차원으로 투영 하였을때 분산을 Maximize하는 축을 찾는 것 입니다. 단순히 축에 대한 투영 뿐만 아니라 벡터에 대한 Maximizer하는 분포를 찾는 것이 일반적입니다.

![image.png](7%204%20Principle%20Component%20Analysis(PCA)%20NP%2020234bdbf13d8012b6f9d7e571f461e8/image_2.png)

각 포인트들을 단순히 x1축에 올려서 보기보단, 포인트 그대로 대각선으로 이어지는 축을 기점으로 찾는것이 더 효율적입니다.

PCA를 수학 없이 쉽게 이해하기

1. PCA는 데이터 요약 도구.
- 데이터에 너무 많은 변수(열)가 있으면 복잡해지는데
- PCA는 그 변수들 중에서 가장 중요한 정보만 뽑아서 요약해주는 도구.
- 예를 들어 100개의 열이 있으면, 그걸 2~3개로 줄이는데, 이때 정보는 최대한 유지합니다.
1. 가장 잘 퍼져 있는 방향을 찾는다.
    - PCA는 데이터가 가장 넓게 퍼져 있는 방향(분산이 큰 방향)을 찾습니다.
    - 그렇게 해서 축은 새로 만들고, 데이터를 그 축에 투영하여 요약합니다.
    - 원래의 축(X1, X2, X3..)이 아니라 데이터에 맞춘 새 축을 말하는데, 이걸 주성분(Principal Component)라고 부릅니다.
2. 사용 하는 이유
    - 차원 축소 : 데이터의 차원을 줄여 시각화 하기에 편리합니다.
    - 노이즈 제거  : 덜 중요한 축은 버려버리니 불필요한 잡음을 줄일 수 있습니다.
    - 속도 개선 : 데이터가 작아지니 머신러닝 알고리즘이 더 ㅂ라라지고 정확해 질 수 있씁니다.
    

> 요약부. 
* PCA는 데이터를 압축하면서 정보는 최대한 유지하려는 기술.
* 가장 잘 퍼진 방향(분산이 큰 방향)을 기준으로 새로운 축을 만든다
* 차원 축소, 시각화, 노이즈 제거, 속도 개선이 유용함.
> 

PCA의 목적은 어떤 데이터를 어떤 벡터로 투영 했을 때, 그 투영 된 곳 에서의 다양성(varience)이 커야 합니다.

PCA 개요

PCA는 비지도 학습에 속합니다. 비지도 학습은 레이블이나 목표 변수가 없는 학습 데이터만으로 데이터 구조 및 패턴을 찾는 학습 방법입니다.

### 차원 축소

![image.png](7%204%20Principle%20Component%20Analysis(PCA)%20NP%2020234bdbf13d8012b6f9d7e571f461e8/image_3.png)

### 차원 축소(Dimensionality Reduction)

데이터의 차원(특성의 수)을 줄이며 데이터의 중요한 정보를 최대한 보존하는 것을 의미합니다. 일반적으로 데이터 추출 시, 노이즈 때문에 함수의 차원이 높아지고 비선형성이 커지는 경우가 많습니다. 

차원 축소의 장점은 다음과 같습니다.

1. 계산 효율성 증가 : 데이터의 차원이 감소하면, 모델 학습과 예측에 필요한 계산량이 줄어듦
2. 데이터 시각화 : 차원을 축소함으로써 데이터의 시각적 이해가 쉬워짐
3. 노이즈 제거 : 노이즈와 불필요 정보 제거
4. 과적합 방지 : 차원의 저주 문제를 해결하여 모델의 과적합을 줄임.

### 차원의 저주(Curse of dimensinoality)

데이터의 차원이 증가 할 수록 해당 공간의 크기가 기하급수적으로 증가하며, 데이터 분석 및 모델 학습에 어려움을 초래하는 현상을 의미합니다.

반면, 차원 축소 시 데이터의 일부 정보 손실이 발생 할 수 있으며, 어떤 차원을 유지하고 제거할지 결정 하는 것이 복잡할 수 있습니다.

### PCA 주요 목적

PCA는 ***데이터의 주요 패턴을 캡처해 차원을 줄이***는 분석 기법임. ***핵심 원리는 데이터의 분산을 최대화 하는 주성분을 찾는 것***임. 분산은 데이터가 얼마나 특정 방향으로 퍼져 있는 지 나타내며, 큰 분산은 해당 방향에 데이터의 주요 정보나 패턴이 조함되어 있음을 의미함. 

큰 분산은 해당 방향에 데이터의 주요 정보나 패턴이 포함되어 있음을 의미함.  따라서, 분산이 큰 주성분 방향으로 데이터를 투영함으로써 차원을 줄이면,정보의 손실을 최소화 할 수 있고 데이터 사이의 차이점을 명확하게 할 수 있음.

PCA 과정

![image.png](7%204%20Principle%20Component%20Analysis(PCA)%20NP%2020234bdbf13d8012b6f9d7e571f461e8/image_4.png)

PCA를 수행할 때는 데이터의 구조를 가장 잘 반영하는 기저를 찾는 것이 중요함. 이를 ***최적의 기저(Optimal Bases)***라고 부르며, PCA에서는 자동으로 분산이 최대가 되는 방향, 즉 데이터 간의 중복성이 가장 적은 방향을 최적의 기저로 찾아냄. 

만약, 중복성이 높은 기저를 선택하면 비슷한 정보를 중복하여 포함하게 되므로, PCA의 주 목적인 정보 압축과 패턴 추출에 방해가 됨.

![image.png](7%204%20Principle%20Component%20Analysis(PCA)%20NP%2020234bdbf13d8012b6f9d7e571f461e8/image_5.png)

이때 기저들은 서로 수직이어야 함.

1. 평균 계산
2. 데이터 중심화(Centering) : 각 데이터에서 평균을 빼서 중심으로 데이터를 모음. 센터링을 하지 않을 경우 주성분 방향이 일치하지 않아 데이터의 분포가 이상해지기 때문임.
3. 공분산(Covariance) 행렬 계산 : 평균을 0으로 normalization하여 convariance matrix를 구한다.
4. 고유값과 고유벡터 계산 : 
    - 공분산 행렬에 decomposition을 적용해 고유값(Eigenvalue)과 고유벡터(Eigenvector)를 구함. 이때, Singular Value Decomposition(SVD)를 사용하는데 이는 선형대수에서 사용하는 기법으로 다른 matrix행과 열을 사용해 정방행렬로 만들어거 값을 구하는데 사용하는 기법임.
    - 2D의 경우 eigenvalue와 eigenvector가 각 2개씩 나오게 되며, eigenvector로 얻어낸 2개의 축을 이용해 1D로 Proejction.
        
        ![image.png](7%204%20Principle%20Component%20Analysis(PCA)%20NP%2020234bdbf13d8012b6f9d7e571f461e8/image_6.png)
        
        - 람다1의 방향은 빨간 화살표
        - 람다2의 방향은 파란 화살표
        
        ![image.png](7%204%20Principle%20Component%20Analysis(PCA)%20NP%2020234bdbf13d8012b6f9d7e571f461e8/image_7.png)
        
        - 만약 람다2를 고려하지 않는다면, 람다1의 방향 화살표로 이동하게 됨.
        - 추후 람다1에 대해서 복원을 한다면 붉은색의 람다1 방향의 라인에 투영된 결과가 얻어지게 됨.
5. 주성분 선택 : 가장 큰 고유값을 갖는 고유벡터로부터 원하는 수의 주성분 선택

![image.png](7%204%20Principle%20Component%20Analysis(PCA)%20NP%2020234bdbf13d8012b6f9d7e571f461e8/image_8.png)

추후 eigenvector를 하나만 뽑아서 계산하면 아래와 같이 차원 축소 된 모습을 볼 수 있으며, 차원 축소 된 값을 다시 복원을 할 수 있으나, 완벽하게 X값으로 복원이 되지는 않고 축 위의 X로 복원이 됨.

![image.png](7%204%20Principle%20Component%20Analysis(PCA)%20NP%2020234bdbf13d8012b6f9d7e571f461e8/image_9.png)

### **활용 예시**

- **Active Shape Model (ASM)**
    
    → landmark 위치들의 변화를 PCA로 압축하여 shape variation을 모델링
    
- **Texture PCA**
    
    → 조직의 질감(texture) 특징 추출 및 군집
    
- **Anomaly Detection**
    
    → 정상 영상의 PCA 분포에서 벗어나는 패턴을 이상으로 탐지
    

[https://maloveforme.tistory.com/221](https://maloveforme.tistory.com/221)

[https://aigong.tistory.com/126](https://aigong.tistory.com/126)

[https://velog.io/@khp3927/Medical-Image-Segmentation-Active-shape-model](https://velog.io/@khp3927/Medical-Image-Segmentation-Active-shape-model)