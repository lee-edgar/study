# 2. Transformer Summary(Encoder)
![image.png](/assets/transformer/2_Transformer_Summary(Encoder)/image.png)

### 뜻은 다르지만, 동일한 단어 케이스

![image.png](/assets/transformer/2_Transformer_Summary(Encoder)/image_1.png)

word embedding은 일정한 길이의 숫자 vector로 표현할 수 있습니다. 주어진 문장 “ 배를 먹었더니, 배가 아프다”를 예시로 들어보면, 서로의 뜻이 다르지만 같은 단어를 가지고 있습니다. 두 단어를 vector 공간상에 표현해보자면 동일한 공간에 위치할텐데, 우리가 서로 다른 뜻이라는 것은 배를 설명하는 ‘먹었더니’, ‘아프다’로 구분하기 때문입니다.

### Attention 구조 활용

![image.png](/assets/transformer/2_Transformer_Summary(Encoder)/image_2.png)

같은 공간에 위치했던 vector들이 attention구조를 통해 문맥을 파악 할 수 있기 때문에, vector 공간에서 위치를 구분지어낼 수 있으며, text processing이 쉬워진 결과를 볼 수 있습니다.

- 더 좋은 feature를 뽑아낼수 있으며, 이는 classification, translation, g eneration에서 강점을 보이겠습니다.

![image.png](/assets/transformer/2_Transformer_Summary(Encoder)/image_3.png)

### 트랜스포머 구조 잘라보기

1. rnn과 마찬가지로 encoder(input), decoder(output) 파트로 구분하기
2. Input Embedding : 단어 혹은 토큰을 vector로 표현
3. Positional Encoding : 각 단어, 토큰의 위치를 vector화 해서 넣어주는 것
    - 토큰 단위로 숫자를 매겨주는 것
4. resdual network 사용 
5. norm layer :  batch normalization 
6. feed forward module : neural net 특성인 Non-Linearity를 주기 위해 FC + ReLU 사용

multi-Head Attention. 즉 self attention을 중점으로 공부하면 됨

### Self Attention

![image.png](/assets/transformer/2_Transformer_Summary(Encoder)/image_4.png)

Self attention의 핵심 구조이며, (Mask Module는 생성형 모델에 쓰이기에 우선 생략)

“I Love You All” 4개의 토큰에 대해서 각 단어별로 일정한 길이의 vector 모양을 가지게 됩니다. 각각의 토큰을 표현하기 위한 숫자들이 쓰여저있습니다. 

***(*토큰 vector의 길이를 20하고  Embedding_dim이라고 가정함.)***

attention의 구조에는 Query, Key, Value는 Linear Layer를 사용해 계산할 수 있습니다. 각각의 단어 vector를 Linear하게 배치하는 역할만 합니다.***(*여기에서의 dimension의 크기는 5, attention_dim이라고 칭함)***

query, key, value 별로 각 단어를 재배치 한 것 처럼 보이지만 뒤에서의 연산에 맞춰 각각의 목적을 지님

1. query vector : 각각의 단어들의 다른 어떤 단어에 집중할지 질문하는 matrix 만듦(다른 단어와 관계를 알아보려는 특정 단어. 즉, 현재 처리 중인 토큰)
2. key vector :  query가 만든 질문의 응답하는 tensor생성. embedding 모델에 의해서 단어를 vector화 시킨 것.
3. value vector : query 와 key가 matching 된 경우에 응답하는 tensor. 각 단어의 관련성을 평가한 후 현재 단어를 나타내기 위해 업데이트 되는 값

![image.png](/assets/transformer/2_Transformer_Summary(Encoder)/image_5.png)

<*embeding_dim : token vector의 길이 20, atten_dim : token vector의 길이 5>

1. 20, embed_dim을 각각의 Query, Key, Value의 동일한 5, atten_dim으로 생성합니다.
2. Query. 질문에 대한 답을 하기 위해  $K^T$로 변경.
3. $K^T$를 Q에 multiple matrix연산을 하게되면 4x4메트릭스를 가지게 되며, 이를 Query와 Key 간의 score matrix로 둘 수 있습니다.
    1. Q의 “I”에 대한  Vector와 $K^T$의 “I”에 대한 Vector가 매칭되어 계산이 되는 모습을 score matrix에서 확인 할 수 있음.
    2. 1행1열의 값은 query의 “I”와 key의“I”가 매칭되어 계산하고, 1행2열의 값은 query의 “I”와 Key의 “Love”가 매칭되어 계산이 되는 방식임.
    3. 즉, score matrix는 query “I”에 맞춰서 key의 하나하나의 값이 매칭되어서 만들어지는 값임.
4. score matrix를 score로 나타낼 수 있는데, 일반적으로 같은 단어들끼리 관계가 높기 때문에 높은 score를 얻게 됨. 문맥상으로 query “I”에 맞춰서 다른 단어들의 관계가 높다면, 그 단어의 score는 높게 잡힘.
5. 그렇게 각각의 score값들을 계산 할 수 있는데, 해당 스코어들을 그대로 쓸 수 없기 때문에 각 행의 score값들의 합이 1이 될 수 있도록 row의 방향으로 softmax를 적용함.
6. softmax가 적용된 score matrix에 value matrix를 가져와서 곱하게 된다면, 결과tensor들은 각각의 vector 리프리젠테이션이 합성되어 결과를 나타내게 됨.
    1. 예를 들어, score matrix에서 softmax가 적용된 I,I가 0.9, 0, 0.1, 0이고, value matrix를 곱한다면, 
        - “I” vector =   “I” * 0.9
        - “you” vector = “you” * 0.1
        
        두 개의 vector를 더한 값이 “I” vector 1열에 들어오게 되면서 기존의 “I”vector에서 새로운 “I” + 0.1만큼 추가된 “I + 0.1”를 얻게 되는 것임. 즉, 기존의 I와 새로운I의 공간상의 좌표가 다르게 표시된다는 것임(*배를 먹었더니, 배가 아프다” 문장에서의 배에 대한 단어의 다름을 알 수 있다는 것임)
        

![image.png](/assets/transformer/2_Transformer_Summary(Encoder)/image_6.png)

                  <attention 매커니즘 적용 전> 

![image.png](/assets/transformer/2_Transformer_Summary(Encoder)/image_7.png)

                    <attention 매커니즘 적용 후>

attention 매커니즘을 적용하면, 

1. 첫 번째 배는 “먹었다니”라는 Key가 응답하면서 공간상의 vector를 서서히 좌측으로 밀고, 
2. 두 번째 배는 “아프다”라는 Key가 응답하면서 공간상의 vector를 서서히 우측으로 밀게 됨

### paper에서의 attention의 공식

![image.png](/assets/transformer/2_Transformer_Summary(Encoder)/image_8.png)

$\sqrt{dk}$
는 softmax적용 전체 구간의 값이 너무 극단으로 가는것을 막기 위해 smooting처리한 것임.

$QK^T$는 score matrix를 말함.

### self attention code

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

embed_dim = 20
atten_dim =5

class SelfAttention(nn.Module):
    def __init__(self, embed_dim, atten_dim):
        super().__init__()
        self.query = nn.Linear(embed_dim, atten_dim)
        self.key = nn.Linear(embed_dim, atten_dim)
        self.value = nn.Linear(embed_dim, atten_dim)
        
    def forward(self, x):
        q = self.query(x)
        k = self.key(x)
        v = self.value(x)
        
        # K.transpose : (seq_len x atten_dim) -> (atten_dim x seq_len) 
        # matmul 연산에 대한 차원 맞추기 위해 transpose
        score = torch.matmul(q, k.transpose(-2, -1)) 
        score = score / k.size(-1) ** 0.5 # smoothing 적용
        
        attention_weights = F.softmax(score, dim = -1) # 
        weigthed_value = torch.matmul(attention_weights, v)
        
        return weigthed_value
```

### code 추가 설명 :         score = torch.matmul(q, k.transpose(-2, -1))

k.transpose(-2, -1) : transpose(dim1, dim2)에 대해서 지정한 두 차원의 순서를 바꾸는 것입니다. 여기서 마이너스 인덱스는 뒤에서부터 차원 번호를 세는 방법입니다.
예를 들어, (batch_size, seq_len, atten_dim)에서 

- -1 : 마지막 차원(atten_dim)
- -2 : 마지막에서 두 번째 차원(seq_len)

k의 shape : (batch_size, seq_len, atten_dim)

- k.transpose(-2, -1) 적용시 → (batch_size, atten_dim, seq_len)

왜 이렇게 계산을 하느냐 ?

Self-Attention의 score의 계산 공식은 다음과 같습니다.

$$
Score = Q * K^T
$$

- Q : (batch, seq_len, atten_dim)
- K : (batch, seq_len, atten_dim) → matmul 연산을 위해서 K를 transpose 해서 (batch, atten_dim, seq_len) 형태로 만들어야 
(seq_len x atten_dim) x (atten_dim x seq_len) = (seq_len x seq_len) 형태의 score 행렬을 만들 수 있음.

요약

1. self attentaion을 통해 각각의 단어들이 서로를 보면서(I, Love, you, all) 문맥을 파악하고

$$
Q * K^T
$$

1. 그 값을 통해 vector값을 update한다.

$$
softmax(Q * T^)V
$$

1. 최종 smoothing $\sqrt{d_k}$을 적용한 공식은 아래와 같다.
    
    $$
    Attention(Q, K, V) = softmax(\frac{Q*K^T}{\sqrt{d_k}})V
    $$
    

[https://www.youtube.com/watch?v=DdpOpLNKRJs&list=PLDV-cCQnUlIb6aku7jnMrvyka3Qazn8R1&index=8](https://www.youtube.com/watch?v=DdpOpLNKRJs&list=PLDV-cCQnUlIb6aku7jnMrvyka3Qazn8R1&index=8)

[https://simpling.tistory.com/3](https://simpling.tistory.com/3)