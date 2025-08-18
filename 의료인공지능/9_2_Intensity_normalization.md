# 9.2. Intensity normalization

### Linear Normalization

상대적으로 어두운 MRI 영상 0 ~ 50의 intensity를 가지는 것이 있을 때 0~255값으로 변화 시킬 수 있음.

![image.png](/assets/의료인공지능/9_2_Intensity_normalization/image.png)

1. 위 영상에서의 어두운 intensity의 최소값과 최대값을 구해보면 간격이 짧을 것으로 예상 됨(0 ~ 50)
2. 위 최소값, 최대값인 0 ~ 50의 값을 0 ~ 255 사이의 값으로 영상을 linear function으로 변형 해줌.
3. 50의 intensity의 값은 255값이 될 것이고, 25값은 128정도의 값이 됨.
    
    ![image.png](/assets/의료인공지능/9_2_Intensity_normalization/image_1.png)
    
    수식으로 살펴보자면, 
    
    기존의  intensity : Wmin = 0, Wmax = 50
    
    변화 후 intensity : Imin = 0, Imax = 255
    
    특징 점 F에서의 intiensity 변화 :
     (f-Wmin/Wmax-Wmin) x (Imax - Imin) + Imin
    
    - 특징 점 F에서 intensity 변화는 선형 정규화가 실제로 어떻게 intiensity를 변화시키는지 수치적으로 확인하고, 영상에서 어떤 구조가 강조될지를 해석하기 위해 보는것임. 즉 의미있는 시각 정보의 변화를 확인해보기 위한 과정임.