# 7. positional encoding

![스크린샷 2025-08-21 14.52.03.png](/assets/transformer/7_positional_encoding/image.png)

Q, K , V로 이뤄진 attention 구조 자체가 token의 순서와 상관없이 모두 연결되어 있기 때문에 각 token의 position정보없이는 순서를 알 수 없음.

예를 들어,  전혀 다른 뜻의 문장을 가지는 두 문장이 있다고 가정합니다.

1. dog eats man : 개가 사람을 먹었다.
2. man eats dog : 사람이 개를 먹었다.

이를 self attention 구조에서 본다면 각각의 token은 모두 이어져있기 때문에 추가적인 위치정보 없이 각 토큰의 임베딩 정보만으로는 문장의 차이를 구분하기가 어려움.

이 두 문장의 차이는 단어의 순서이며 이를 해결하기 위해 트랜스포머 구조에서는 순서 정보를 넣어줘야 하는데 그 방법 중의 하나가 positional Encoding임.

### Transformer구조에 위치 정보를 넣는 방법

1. input embedding 처럼 학습이 가능한 embedding layer(matrix)를 넣는 것
    - “I love you all”이라는 문장의 포지션 정보
        - 세로 :  최대 토큰의 개수 4(40, 1842, 345, 477)
        - 가로 : embedding의 size 20
    - embedding matrix를 만들수 있는데, 처음에는 random하게 initalization처리 되어 있음.
    - i love you all이라는 input tensor를 만들고자 한다면, token으로 부터 embedding vector를 만드는 matrix 결과와 위치정보의 결과의 첫 번째 단어 위치 벡터와 더해서 초기 input dimension “I”에 해당하는 vector를 만듬.
        
        ![스크린샷 2025-08-21 15.16.49.png](/assets/transformer/7_positional_encoding/image_1.png)
        
               (* 우측은 토큰정보, 좌측은 오른쪽 토큰의 position vector)
        
        즉, i love you all의 token index와 token index의 position vector를 서로 더해  각각의 토큰에 해당하는 vector를 만드는 것임(=초기 input dimension의 vector들)
        
        양쪽의 matrix 둘다 embedding layer이기 때문에 처음 상태는 random하게 initialization 되어 있고 아주 많은 양의 데이터로 두 embedding matrix를 학습 시키는 것임
        
2. (position embedding layer Non Train)삼각함수를 이용한 정해진 패턴을 포지션 인코딩으로 활용하는 방법
    
    ![스크린샷 2025-08-21 15.28.13.png](/assets/transformer/7_positional_encoding/image_2.png)
    
    - 포지션 인코딩 레이어에 각각의 값을 학습을  통해 알맞은 값을 트레이닝 시키는 것이 아니라 삼각함수를 사용한 정해진 계산식에 따라서 그 결과 값을 포지션 인코딩 값으로 사용하는 방법임
    - 장점으로는 포지션 임베딩 레이어를 따로 학습 시킬 필요가 없음
3. Rotary Positional Embedding 
    
    단어들의 상대적인 위치를 고려하면서 절대적인 위치를 함께 인코딩 시키는 방법 
    
    어떤 토큰에 벡터가 있다면 그 단어의 위치만큼 그에 해당하는 각도로 임베딩 벡터를 회전시킴