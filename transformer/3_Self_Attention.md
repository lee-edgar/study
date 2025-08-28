# 3. Self Attention

### 3. Self Attention

![image.png](/assets/transformer/3_Self_Attention/image.png)

Self attention의 핵심 구조이며, (Mask Module는 생성형 모델에 쓰이기에 우선 생략)

“I Love You All” 4개의 토큰에 대해서 각 단어별로 일정한 길이의 vector 모양을 가지게 됩니다. 각각의 토큰을 표현하기 위한 숫자들이 쓰여저있습니다. 

***(*토큰 vector의 길이를 20하고  Embedding_dim이라고 가정함.)***

attention의 구조에는 Query, Key, Value는 Linear Layer를 사용해 계산할 수 있습니다. 각각의 단어 vector를 Linear하게 배치하는 역할만 합니다.***(*여기에서의 dimension의 크기는 5, attention_dim이라고 칭함)***

query, key, value 별로 각 단어를 재배치 한 것 처럼 보이지만 뒤에서의 연산에 맞춰 각각의 목적을 지님

1. query vector :  현재 단어가 **다른 단어들과 어떤 관련이 있는지 묻는 질문 벡터**입니다.
    
    → "내가 지금 어떤 단어에 집중해야 할까?"를 표현하는 역할입니다.
    
2. key vector :  Query의 질문에 **응답할 수 있도록 각 단어가 가진 고유한 정보**를 담은 벡터입니다.
    
    → 다른 단어가 자신에게 얼마나 주목해야 하는지를 판단하는 기준입니다.
    
3. value vector : Query와 Key가 잘 맞는 정도(유사도)에 따라 **실제로 전달될 정보**를 담은 벡터입니다.
    
    → 연관도가 높은 단어일수록 더 많이 반영되어 최종 출력에 영향을 줍니다.
    

![image.png](/assets/transformer/3_Self_Attention/image_1.png)

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
        

![image.png](/assets/transformer/3_Self_Attention/image_2.png)

                  <attention 매커니즘 적용 전> 

![image.png](/assets/transformer/3_Self_Attention/image_3.png)

                    <attention 매커니즘 적용 후>

attention 매커니즘을 적용하면, 

1. 첫 번째 배는 “먹었다니”라는 Key가 응답하면서 공간상의 vector를 서서히 좌측으로 밀고, 
2. 두 번째 배는 “아프다”라는 Key가 응답하면서 공간상의 vector를 서서히 우측으로 밀게 됨

### paper에서의 attention의 공식

![image.png](/assets/transformer/3_Self_Attention/image_4.png)

$\sqrt{dk}$
는 softmax적용 전 값이 너무 극단으로 가는것을 막기 위해 smooting처리한 것임.

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
        
        score = torch.matmul(q, k.transpose(-2, -1))
        score = score / k.size(-1) ** 0.5 # smoothing 적용
        
        attention_weights = F.softmax(score, dim = -1)
        weigthed_value = torch.matmul(attention_weights, v)
        
        return weigthed_value
```

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