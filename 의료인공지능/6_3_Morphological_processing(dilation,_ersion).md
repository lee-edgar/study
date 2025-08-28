# 6.3. Morphological processing(dilation, ersion)

![image.png](6%203%20Morphological%20processing(dilation,%20ersion)%2020034bdbf13d80bc8a10edbfe94ae182/image.png)

threholding으로 처리하게 되면 위와 같이 나오는데, 자세히 보면 흰색 안에 검은색으로 점처럼 추가적으로 보이는 것이 있는데 여기에서 조금 더 프로세싱을 해줄 필요가 있음.

morphological processing을 통해서 해당 노이즈들을 쉽게 처리 할 수 있는데, 대표적으로 Dilation과 Erosion 두 가지 방법이 있습니다.

### Dilation

![image.png](6%203%20Morphological%20processing(dilation,%20ersion)%2020034bdbf13d80bc8a10edbfe94ae182/image_1.png)

Dilation(팽창) : 구조 요소(structuring element, kernel, mask)와 입력 이미지가 곂치는 부분이 하나라도 있을 경우 kernel의 중심 위치에 해당하는 픽셀을 1로 설정함.

![image.png](6%203%20Morphological%20processing(dilation,%20ersion)%2020034bdbf13d80bc8a10edbfe94ae182/image_2.png)

 structer element를 정의하여 아래 작업을 수행.

![image.png](6%203%20Morphological%20processing(dilation,%20ersion)%2020034bdbf13d80bc8a10edbfe94ae182/image_3.png)

![image.png](6%203%20Morphological%20processing(dilation,%20ersion)%2020034bdbf13d80bc8a10edbfe94ae182/image_4.png)

Structuring element의 1인 부분이 foreground(객체)와 곂치는지 확인하며 sliding window 방식으로 이미지를 쓸어갑니다.

오른쪽 그림에서는 structuring element의 아래와 오른쪽이 froegorund와 곂치므로 해당 위치의 element 중심에 해당하는 픽셀을 1로 채워줍니다.(* 아래, 오른쪽의 foreground가 이미 1이라서 채우진 않음)

![image.png](6%203%20Morphological%20processing(dilation,%20ersion)%2020034bdbf13d80bc8a10edbfe94ae182/image_1.png)

Structuring element를 다르게 구성 할 수도 있으며, 전체 sliding window방식으로 쓸어주면 위와 같이 물체가 dilation된 결과물을 볼 수 있음.

### Erosion

![image.png](6%203%20Morphological%20processing(dilation,%20ersion)%2020034bdbf13d80bc8a10edbfe94ae182/image_5.png)

Erosion은 dilation과 반대되는 개념으로, foreground가 아닌 background에 적용하게 되며, foreground 부분은 지워지지 않고 background 부분만 지워지는 효과를 볼 수 있음.

Erosion과 Dilation을 적절히 사용해야 함.

1. Erosion 이후 Dilation하는 opening 방법
    - 원본 shape를 유지하며 noise를 제거함
        
        사이즈를 줄여 noise줄이고, 팽창하여 원본 유지
        
2. Dilation 이후 Erosion하는 closing 방법
    - 원본 shaple를 유지마혀 object 내 hole를 제거함.
    
    hole을 dilation하여 채우고 ersion으로 줄여서 원본 유지
    

### 의료 영상에서의 ersion, diation 효과 확인

![image.png](6%203%20Morphological%20processing(dilation,%20ersion)%2020034bdbf13d80bc8a10edbfe94ae182/image_6.png)

1. thresholding

![image.png](6%203%20Morphological%20processing(dilation,%20ersion)%2020034bdbf13d80bc8a10edbfe94ae182/image_7.png)

1. erosion을 통해 noise 제거 및 아래 객체의 축소

![image.png](6%203%20Morphological%20processing(dilation,%20ersion)%2020034bdbf13d80bc8a10edbfe94ae182/image_8.png)

1. 다시 dilation을 통해 아래 객체를 팽창시키며 hole 채우기
2. hole 제거 했으니 원본 유지를 위해 다시 ersion 진행.

> erosion → dilation → erosion → dailation을 통해서 noise제거, hole을 채우고 다시 원본 유지가 됨.
>