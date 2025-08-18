# 6.4. Region growing / Watershed algorithm

![image.png](/assets/의료인공지능/6_4_Region_growing_Watershed_algorithm/image.png)

Morphological processing(dilation, ersion)으로 noise 감소와 hall을 채움에도 완벽하게 처리되지 않을 수 있음.

### Region Growing

![image.png](/assets/의료인공지능/6_4_Region_growing_Watershed_algorithm/image_1.png)

- 붉은색의 input 포인트를 받아 주변으로 255값인지 0값인지 확인하여growing하여 퍼지면서  어느 순간 0값과 만나는 시점에서 growing을 멈추게 됨
- region growing을 통해 얻어낸 부분을 1로 label을 주고, 나머지는 0으로 label을 주게 됩니다. 그렇게나머지는 전부 사라지게 되어 해당 부분만 추출 가능함.

위와 Binary Map가 아닌 일반 영상에서도 Intensity를 이용해 Region Growing방법을 사용 할 수 있음

![image.png](/assets/의료인공지능/6_4_Region_growing_Watershed_algorithm/image_2.png)

                           |Intensity1 - Intensity2| < threshold

- 두 Intensity의 차이를 구하여 threshold 조건에 부합하면 1로 label하고, 부합하지 않으면 차이가 심한 것 이므로 0으로 label처리하는 로직.

### Watershed Algorithm

![image.png](/assets/의료인공지능/6_4_Region_growing_Watershed_algorithm/image_3.png)

region growing기법을 사용하고자 하면 위 세포 이미지에서는 각각의 세포들을 모두 처리를 해야해서 비효율적임. 따라서 automatic 하게 할 수 있는 Watershed Algorithm 기법을 제안함.

![image.png](/assets/의료인공지능/6_4_Region_growing_Watershed_algorithm/image_4.png)

우측 세포 사진의 중간 영역의 단면의 밝기를 통해 좌측 그림을 생각 해볼 수 있음.

![image.png](/assets/의료인공지능/6_4_Region_growing_Watershed_algorithm/image_5.png)

댐으로 이해하면 좋을텐데, 좌측과 같은 구덩이 지형에 물을 채우기 시작하면, 아래부터 채워지기 마련임.

구덩이에 물이 채워지다 보면 맞닿는 부분이 있는데, 그 부분을 경계로 하여 각 구덩이 마다 세포 각각을 구분 할 수 있음.

Region grwoing 기법으로 이해를 해보자면, 구덩이 마다 바닥에 포인트를 찍어서, 경계에 닿을 때 까지 확장해 나간다고 생각 해 볼 수 있음.

맞닿는 부분을 boundry로 구분하여 무언가를 해볼 수 도 있겠다.