# 4. Multi-Head Attention

![image.png](/assets/transformer/4_Multi-Head_Attention/image.png)

![image.png](/assets/transformer/4_Multi-Head_Attention/image_1.png)

기존의 Self Attention에서 최종 결과물 attention feature를 얻을 수 있습니다.

![image.png](/assets/transformer/4_Multi-Head_Attention/image_2.png)

                                 <self attention에서 얻은 최종 결과물 attentaion feature>

### multi head attention은 attention feature를 여러 개 뽑아낸 것.

![image.png](/assets/transformer/4_Multi-Head_Attention/image_3.png)

- input 20 embed_dim을 attendin_dim이 5가 되는 Linear Layer를 통해 Query, Key, Value Matrix를 만들고  vector size 5를 가지는 attention feature matrix를 output으로 갖는 가짊.

![image.png](/assets/transformer/4_Multi-Head_Attention/image_4.png)

- 똑같은 Attention 구조를 갖는 네 개의 block을 동시에 적용하고 네 개의 서로다른 attenion feature를 갖는 output tensor를 만들어 내는 것이 핵심임.
- 이후 네 개의 다른 attenion feature를 갖는 output tensor들을 concatednation 하여 하나로 붙힐 수 있습니다.
- concatednation 된 tensor는 서로 다른 네 개의 attention feature를 가지는 tensor를 연결한 형태.
    
    → 처음 input 으로 넣었던 20의 embed_dim과 동일한 output size를 가지게 됨.
    
    → 마지막으로, 여기에 다시 한번 activation function이 없는 Linear Layer 적용하면
    
    → vector를 재배열 했지만 네개의 feature attention을 내장한 하나의 multi head attention을 뽑을 수 있음(dimision size 20)
    

### self attention을 활용해 multi head attention 코드 구성

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
    
class MultiHeadAttention(nn.Module):
    def __init__(self, embed_dim, num_heads): # head 개수로 attention dimension size를 구할 수 있음.
        super().__init__()
        
        atten_dim = embed_dim * num_heads # 예제에서의 input embed_dim은 20, head의 개수는 4. 따라서 num_heads = 5
        
        # head 개수만큼 self attention block 생성
        self.attentions = 
	        nn.ModuleList([SelfAttention(embed_dim, atten_dim) 
		        for _ in range(num_heads)])
            # self.attention0, self.attention1, self.attention2, self.attention3의 for 루프임.
        self.fc = nn.Linear(atten_dim, embed_dim)
    
    def forward(self,x ):
        # attention들을 각각 불러내서 clac
        head_outputs = []
        for attention in self.attentions:
            head_outputs.append(attention(x))
            
        # append으로 만들어진 output들을 concat을 사용해 하나로 합치기
        concatenated_head = torch.cat(head_outputs, dim = -1)
        output = self.fc(concatenated_head) # fc layer를 통해 재배열
        return output
```

![image.png](/assets/transformer/4_Multi-Head_Attention/image_5.png)

transformer의 encoder 부분의 multi head attention을 구성 한 것임.