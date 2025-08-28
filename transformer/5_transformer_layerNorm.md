# 5. transformer layerNorm

Batch Normalization에 대해서 잠시 복습.

![image.png](/assets/transformer/5_transformer_layerNorm/image.png)

### 문제 정의

만약 해당 activation function안으로 모든 input data가 아래쪽에 몰려있거나, 위쪽에 몰려 있다면 backpropagation을 위한 gradient(기울기)가 0되면서 neural net이 학습되지 않음. 

### Normalization의 필요성

위와 같은 문제에 의해서 통계적인 개념을 활용해 정규화를 시키게 됨.

normalize를 시키기 위해서 input sample data로 부터 평균과 분산을 계산하고 각 샘플들에 대해서 정규화를 하면 그 input data들은 표준 정규 분포를 보여줌.

 하지만 여러 neural에 동일한 정규화 된 데이터들만 들어간다면 neural이 의미가 사라짐 → Neural Net에 normalize layer에 학습이 되는 parameter. 감마, 베타를 적용 할 수 있음.

1. 정규화 된 데이터가 더 좁은 분포를 가질 수 있게 하거나 
2. 더 넓은 분포를 가질 수 있게 해줌 
3. 데이터를 좌우로 움직히는 시프트 할 수 있음

### Layer Norm

![스크린샷 2025-08-21 13.27.36.png](/assets/transformer/5_transformer_layerNorm/image_1.png)

- (참고)과거의 transpose의 encoder 부분은 multi-head attention과 feed forward 이후에 norm layer가 존재했으나, 요즘 들어서는 multi-head attention과 feed forward 앞 부분에 위치하게 됨

![스크린샷 2025-08-21 13.30.43.png](/assets/transformer/5_transformer_layerNorm/image_2.png)

layer norm은 bacth normalization과 동일한 원리를 가지는데 정규화에 있어서 통계를 내는 감마, 베타를 계산하는 dimension만 다르다고 보면 됨.

multi head attention에 들어가기 전에 layer norm을 적용하게 되는데, 

1. embed_dim에 각 평균과 분산을 각 토큰 별로 계산해서 표준화를 시킴
2. layer norm에 학습되는 파라미터인 감마와 베타는 embed_dim을 element별로 학습
3. layer norm는 batch dimension을 전혀 신경쓰지 않기 때문에 batch의 길이를 1이라고 봐도 무방함.

![스크린샷 2025-08-21 13.31.34.png](/assets/transformer/5_transformer_layerNorm/image_3.png)

트랜스포머 관점에서 보자면, input data에 layer norm을 적용하고 정규화 된 input data를 기반으로 multi head attention을 적용하고,

그 다음, 기본 input data와 multi head attention의 output을 add하면 됨

multi head attention, self attention

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
    def __init__(self, embed_dim, num_heads): 
    # head 개수로 attention dimension size를 구할 수 있음.
        super().__init__()
        
        atten_dim = embed_dim * num_heads 
        # 예제에서의 input embed_dim은 20, head의 개수는 4. 따라서 num_heads = 5
        
        # head 개수만큼 self attention block 생성
        self.attentions = 
	        nn.ModuleList([SelfAttention(embed_dim, atten_dim) 
		        for _ in range(num_heads)])
            # self.attention0, self.attention1, self.attention2, self.attention3의 for roop
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

feed forward

```python
class FeedForward(nn.Module):
	def __init__(self, embed_dim, ff_dim):
		super().__init__()
		self.net = nn.Sequential(
			nn.Linear(embed_dim, ff_dim), # embedding dimension -> FeedForward linear
			nn.ReLU(),
			nn.Linear(ff_dim, embed_dim) # FeedForward -> embedding dimension linear
		)
	def forward(self, x):
		return self.net(x)
```

self attention과 multi head attention을 가지고 있는 transformer block

위에서 만든 self attention, multi head attention, feed forward들을 transformer block에서 구조화

```python
class TransformerBlock(nn.Module):
	def __init__(self, embed_dim, n_head)
	super().__init__()
	self.layer_norm1 = nn.LayerNorm(embed_dim)
	self.multihead_atten = MultiheadAttention(embed_dim, n_head)
	
	self.layer_norm2 = nn.LayerNorm(embed_dim)
	
	# 1. FeedForward는 input embed dimension으로 부터 4배의 embed dimension으로 올리고
	# 2. activation function을 적용하는 함
	self.feed_forward = FeedForward(embed_dim, 4*embed_dim)
	
	
	def forward(self, x):
		# normization 된 값에 multihead attenion적용 후 원래 데이터에 추가(resudal net와 유사)
		x = x + self.multihead_Atten(self.layer_norm1(x))
		x = x + self.feed_forward(self.layer_norm2(x))
		return x 
```

### 최종 요약

![스크린샷 2025-08-21 13.54.46.png](/assets/transformer/5_transformer_layerNorm/image_4.png)

input data는 layer norm으로 정규화 되고 → 정규화 된 데이터를 기반으로  multi-head attention을 거쳐서 output이 나옴 → 해당 output에 초기  input data를 다시 넣어서 resdual network를 구성하는 동시에 normalize 된 Feed Forward Network를 적용 해줌 이 과정에서 output이 나오게 되는데, 해당 output에서 resudal connection을 연결해 줌으로서 전체적인 transformer의 encoder block이 완성이 되는 것임.

위 전체 프로세스를 반복적으로 수행 하면 오리지널 트랜스포머 구조에서 하단의 이미지 좌측부분을 수행한것이 되며, multi-head attention과 feed forward 이후에 norm을 붙히는게 아닌 이전에 붙힌 모양으로 구현된것임

![스크린샷 2025-08-21 13.57.39.png](/assets/transformer/5_transformer_layerNorm/image_5.png)