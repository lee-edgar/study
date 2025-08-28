# 10. Masked Self Attention(Masked Multi Head Attention)

트랜스포머에서의 마스크 셀프 어텐션.

왜 트랜스포머에서 미래 정보 차단(Masked self-attention)을 사용하는가 ?

1. 트랜스포머는 병렬 처리를 위해 등장함.
    - 입력 문장을 한번에 전체 넣고, 각 토큰이 서로 주고 받으며 연산(self-attention)
2. 하지만, 텍스트 생성에서는 미래 정보를 알면 안됨.
    1. “나는 밥을 먹고” 라는 문장이 있을때.
    2. 1 단계: “나는”을 보고 → “밥을” 예측
    3. 2단계 : “나는 밥을”을 보고 → “먹고” 예측
    
    이때, 모델이 “먹고”를 예측하려고 할때, self-attention으로 “먹고”라는 정답 토큰을 들여다보면 정답을 보고 맞춘 것이라서 학습 왜곡이 일어난것임.
    
    그래서, mask를 씌워서 아직 예측하지 못한 미래 토큰을 보지 못하게 막는 것임.
    
3. 순차적 예측 유도 ?
    - 왼쪽 → 오른쪽으로 순차적으로 예측하도록 훈련시켜야 실제 생성(inference) 단계에서 일관된 동작.

> 훈련에서는 전체 문장을 알고 있지만, 생성할 때는 미래를 모름. 그렇기 때문에 훈련할 때도 미래를 모른다는 가정하에 훈련이 이뤄져야하기때문에, mask를 사용해 다음 예측 값을 가져버리는 것임
> 

### 일반 self attention

```python
class SelfAttention(nn.Module):
	def __init__(self, embed_dim, atten_dim):
		super().__init__()
		self.query = nn.Linear(embed_dim, atten_dim, bias=False)
		self.key = nn.Linear(embed_dim, atten_dim, bias=False)
		sself.value = nn.Linear(embed_dim, atten_dim, bias=False)
	
	def forward(self, x):
		query = self.query(x)
		key = self.key(x)
		value = self.value(x)
		
		score = torch.matmul(query, key.transpose(-2, -1))
		score = score / key.size(-1)**0.5 #트랜스포머 논문의 norm
		
		attnetion_weight = F.softmax(score, dim=-1) # 확률 적용
		weighted_values = torch.matmul(attention_weights, valeu) # 확률에 value 연산
		return weighted_values
```

### Mask self attention
![image.png](/assets/transformer/10_Masked_Self_Attention(Masked_Multi_Head_Attenti)/image.png)

1. 마스크를 위해 torch.trill 함수 사용 : 삼각형 모양의 matrix
    
    ```python
    tril = torch.tril(torch.ones(4,4))
    print(tril)
    ```
    
    tensor([[1., 0., 0., 0.
                  [1., 1., 0., 0.],
                  [1., 1., 1., 0.,],
                  [1., 1., 1., 1.]])
    
2. random score생성
    
    ```python
    torch.manual_seed(42)
    scores = torch.randn(4,4)
    ```
    
    tensor([[ 1.9269,  1.4873, 0.9007, -2.1055],
                  [ 0.6784, -1.2345, -0.0431, -1.6047],
                  [ -9,7521, 1.6487, -0.3925, -1.4036],
                  [ -0.7279, -0.5594, -0.7688, 0.7624]])
    
3. random score에 마스크 torch.trill 적용
    
    ```python
    torch.manual_seed(42)
    scores = torch.randn(4,4)
    tril = torch.tril(torch.ones(4,4))
    masked_scores = scores.masked_fill(tril == 0, float('-inf'))
    # tril 0값은 -int (-무한)으로.
    print(scores)
    print(masked_scores)
    ```
    
    tensor([[ 1.9269,  1.4873, 0.9007, -2.1055],
                  [ 0.6784, -1.2345, -0.0431, -1.6047],
                  [ -9,7521, 1.6487, -0.3925, -1.4036],
                  [ -0.7279, -0.5594, -0.7688, 0.7624]])
    
    tensor([[ 1.9269,  -inf,       -inf,         -inf],
                  [ 0.6784, -1.2345, -inf,         -inf],
                  [ -9,7521,  1.6487, -0.3925,   -inf],
                  [ -0.7279, -0.5594, -0.7688, 0.7624]])
    

-inf를 사용하는 이유?

![image.png](/assets/transformer/10_Masked_Self_Attention(Masked_Multi_Head_Attenti)/image_1.png)

softmax 적용시  -무한대를 0값을 뽑아내기 위함. 아래 코드에서 확인 가능

```python
torch.manual_seed(42)
scores = torch.randn(4,4)
tril = torch.tril(torch.ones(4,4))
masked_scores = scores.masked_fill(tril == 0, float('-inf'))
attention_weights = F.softmax(masked_scores , dim=-1)
# tril 0값은 -int (-무한)으로.
print(scores)
print(masked_scores)
print(attention_weights)
```

tensor([[ 1.9269,  1.4873, 0.9007, -2.1055],
              [ 0.6784, -1.2345, -0.0431, -1.6047],
              [ -9,7521, 1.6487, -0.3925, -1.4036],
              [ -0.7279, -0.5594, -0.7688, 0.7624]])

tensor([[ 1.9269,  -inf,       -inf,         -inf],
              [ 0.6784, -1.2345, -inf,         -inf],
              [ -9,7521,  1.6487, -0.3925,   -inf],
              [ -0.7279, -0.5594, -0.7688, 0.7624]])

tensor([[ 1,           0,            0,         0],
              [ 0.8714,  0.1286,  0,         0],
              [ 0.0743,  0.8193, 00.1064,   0],
              [ 0.1319,   0.1561,  0.1266, 0.5854]])

MaskedSelfAttention

- 위 masked의 개념을 Self Attention에 적용한다면
    - torch.tril을 이용해 mask를 만들고, mask의 score를 softmax 후 확률로 뽑으면 됨.

```python
class MaskedSelfAttention(nn.Module):
	def __init__(self, embed_dim, atten_dim):
		super().__init__()
		self.query = nn.Linear(embed_dim, atten_dim, bias=False)
		self.key = nn.Linear(embed_dim, atten_dim, bias=False)
		sself.value = nn.Linear(embed_dim, atten_dim, bias=False)
	
	def forward(self, x):
		query = self.query(x)
		key = self.key(x)
		value = self.value(x)
		
		score = torch.matmul(query, key.transpose(-2, -1))#텐서의 마지막 2개 차원을 기준.
		score = score / key.size(-1)**0.5 #트랜스포머 논문의 norm
		
		tril = torch.tril(torch.ones(x.size(1), x.size(1))).to(x.device)
		masked_scores = scores.masked_fill(tril == 0, float('-inf'))
		
		attnetion_weight = F.softmax(masked_scores , dim=-1) # 확률 적용
		weighted_values = torch.matmul(attention_weights, valeu) # 확률에 value 연산
		return weighted_values
```

explain code

```python
tril = torch.tril(torch.ones(x.size(1), x.size(1))).to(x.device)
```

x shape == (4, 4) 가정

- `x.size(1)`은 `4`입니다.
- `torch.ones(4, 4)` → 모든 원소가 1인 4x4 행렬 생성
- `torch.tril(...)` → **하삼각 행렬** (lower triangle)만 유지

```python
masked_scores = scores.masked_fill(tril == 0, float('-inf'))
```

- `tril == 0`인 위치에 `-inf`를 채움
- 이후 softmax를 거치면 `-inf`는 `0` 확률로 바뀌므로, attention weight가 0이 됨 → 학습이나 예측에 영향을 주지 않음

```python
attnetion_weight = F.softmax(masked_scores , dim=-1) # 확률 적용
weighted_values = torch.matmul(attention_weights, valeu) # 확률에 value 연산
```

Softmax로 Attention Weight 계산

- `dim=-1` → **각 row(마지막 차원)** 기준으로 softmax 적용
- 확률 분포로 변환되며, 미래 단어는 `0`, 현재와 과거 단어에만 집중
- `attention_weights`는 shape `(seq_len, seq_len)` (여기선 4x4)

Weighted Sum 계산

- `value`는 shape `(seq_len, embedding_dim)`이라고 가정하면
- `matmul` 결과는 attention이 적용된 representation 벡터가 됩니다.

### dim = -1에 대한 설명.

1. x = torch.randn(2, 3, 4)  # shape: (batch=2, seq_len=3, dim=4)
    
    
    | dim 값 | 의미하는 축 |
    | --- | --- |
    | `0` | batch (2) |
    | `1` | seq_len (3) |
    | `2` or `-1` | dim (4) |
2. 왜 `dim = -1` 을 쓰는가?
- **코드 유연성**: 마지막 차원의 크기가 바뀌어도 코드를 수정할 필요가 없습니다.
- 예를 들어 `F.softmax(x, dim=-1)`은 항상 **"각 토큰의 feature 차원"** 기준으로 softmax를 수행하게 됩니다.
1. 실제 트랜스포머 예
    
    ```python
    scores = torch.matmul(Q, K.transpose(-2, -1)) / sqrt(d_k)
    attn = F.softmax(scores, dim=-1)  # 각 query에 대해 key의 score를 softmax
    ```
    
    이 경우 `dim=-1`은 `[batch, head, seq_len_q, seq_len_k]` 중 `seq_len_k` 축을 따라 softmax 함.
    

### MaskedSelfAttention을 여러개 사용한다면, Masked  Multi Head Attention.

```python
class MaskedSelfAttention(nn.Module):
	def __init__(self, embed_dim, atten_dim):
		super().__init__()
		self.query = nn.Linear(embed_dim, atten_dim, bias=False)
		self.key = nn.Linear(embed_dim, atten_dim, bias=False)
		sself.value = nn.Linear(embed_dim, atten_dim, bias=False)
	
	def forward(self, x):
		query = self.query(x)
		key = self.key(x)
		value = self.value(x)
		
		score = torch.matmul(query, key.transpose(-2, -1))#텐서의 마지막 2개 차원을 기준.
		score = score / key.size(-1)**0.5 #트랜스포머 논문의 norm
		
		tril = torch.tril(torch.ones(x.size(1), x.size(1))).to(x.device)
		masked_scores = scores.masked_fill(tril == 0, float('-inf'))
		
		attnetion_weight = F.softmax(masked_scores , dim=-1) # 확률 적용
		weighted_values = torch.matmul(attention_weights, valeu) # 확률에 value 연산
		return weighted_values
```