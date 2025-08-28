# 11. char level GPT(*Self Attention / Masked Multi Head Attetion /  Transformer Generator) Code 전반

## 1. Self Attention에서 Maksed를 추가하여 Masekd Self Attention 생성.

- 일반 Self Attention에서 Masked를 적용시켜 masked self attention을 생성합니다. 아래의 masked로 masked self attention을 생성합니다.

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

```python
# masked
tril = torch.tril(torch.ones(x.size(1), x.size(1))).to(my_device)
masked_scores = scores.masked_fill(tril == 0, float('-inf'))
```

---

## 2. Masked Self Attention을 N번 반복하여 Masked Multi Head Attention 생성하기

                                                           < Masked Self Attention >

![image.png](/assets/transformer/11_char_level_GPT(_Self_Attention_Masked_Multi_Head_Attention)/image.png)

```python
#                          <Masked Self Attention 구현 코드>
class MaskedSelfAttention(nn.Module):
    def __init__(self, embed_dim, atten_dim):
        super().__init__()
        self.query = nn.Linear(embed_dim, atten_dim, bias=False)
        self.key = nn.Linear(embed_dim, atten_dim, bias=False)
        self.value = nn.Linear(embed_dim, atten_dim, bias=False)
    def forward(self, x):
        query, key, value = self.query(x), self.key(x), self.value(x)
        scores = torch.matmul(query, key.transpose(-2, -1))
        scores = scores / key.size(-1)**0.5
        tril = torch.tril(torch.ones(x.size(1), x.size(1))).to(my_device)
        masked_scores = scores.masked_fill(tril == 0, float('-inf'))
        attention_weights = F.softmax(masked_scores, dim=-1)
        weighted_values = torch.matmul(attention_weights, value)
        return weighted_values
```

```python
#                          <MaskedMultiheadAttention 구현 코드>
class MaskedMultiheadAttention(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        attention_dim = embed_dim // num_heads
        self.attentions = nn.ModuleList([MaskedSelfAttention(embed_dim, attention_dim) for _ in range(num_heads)])
        self.fc = nn.Linear(embed_dim, embed_dim)
    def forward(self, x):
        head_outputs = []
        for attention in self.attentions:
            head_output = attention(x)
            head_outputs.append(head_output)
        concatenated_heads = torch.cat(head_outputs, dim=-1)
        output = self.fc(concatenated_heads)
        return output
```

- MaskedSelfAttention을 N번 반복해서 MaskedMultiheadAttention 생성

---

## 3. Feed Foward 구성

![image.png](/assets/transformer/11_char_level_GPT(_Self_Attention_Masked_Multi_Head_Attention)/image_1.png)

```python
#                          <FeedFoward 구현 코드>

class FeedFoward(nn.Module):
    def __init__(self, embed_dim, ff_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(embed_dim, ff_dim),
            nn.GELU(),
            nn.Linear(ff_dim, embed_dim))
    def forward(self, x):
        return self.net(x)
```

- Feed Forawrd 네트워크 구현

---

## 4. Transformer Decoder Block 구현

![image.png](/assets/transformer/11_char_level_GPT(_Self_Attention_Masked_Multi_Head_Attention)/image_2.png)

```python
class TransformerDecoderBlock(nn.Module):
    def __init__(self, embed_dim, n_head):
        super().__init__()
        self.layer_norm1 = nn.LayerNorm(embed_dim)
        self.multihead_atten = MaskedMultiheadAttention(embed_dim, n_head)

        self.layer_norm2 = nn.LayerNorm(embed_dim)
        self.feed_forward = FeedFoward(embed_dim, 4*embed_dim)

    def forward(self, x):
        x = x + self.multihead_atten(self.layer_norm1(x))
        x = x + self.feed_forward(self.layer_norm2(x))
        return x
```

- transformer decoder block 생성 구현
- 앞의 첫 번째 Layer Norm , 뒤의 두 번째 Layer Norm 적용
- skip connection 적용(multihead attention, feed forward 부분)

---

## 5. transformer generator

![image.png](/assets/transformer/11_char_level_GPT(_Self_Attention_Masked_Multi_Head_Attention)/image_2.png)

- 전체 TransformerDecoderBlock의 N번 반복, character embedding, position encoding, output.

```python
class TransformerGen(nn.Module):
    def __init__(self, char_size, embed_dim, n_heads, n_layers, block_size):
    '''
	    char_size : 알파벳 개수
	    embed_dim : 내부 트랜스포머 embedding dim
	    n_heads : head의 개수 
	    n_layers : 트랜스포머 deocder 개수
      block_size : attention이 볼 수 있는 최대 글자 수
    '''
        super().__init__()
        self.block_size = block_size
        self.char_embedding = nn.Embedding(char_size, embed_dim)
        
        # Embedding layer를 통해 정의
        self.positional_encoding = nn.Embedding(block_size, embed_dim) 
        self.transformer_blocks = nn.Sequential(
	        *[TransformerDecoderBlock(embed_dim, n_heads) for _ in range(n_layers)]
	      )
        self.ln_f = nn.LayerNorm(embed_dim)
        self.fc= nn.Linear(embed_dim, char_size) # fc로 decoder의 최종 output

    def forward(self, x):
        char_embeddings = self.char_embedding(x)  # [batch_size, seq_length, embed_dim]
        positions = torch.arange(0, x.size(1), device=x.device).unsqueeze(0)  # [1, seq_length]
        pos_embeddings = self.positional_encoding(positions)  # [1, seq_length, embed_dim]
        x = char_embeddings + pos_embeddings
        x = self.transformer_blocks(x)
        x = self.ln_f(x)
        logits = self.fc(x)
        return logits
    
    def generate(self, idx, max_len=100):
		    '''
			    def forawrd 기반으로 generate
		    '''
        with torch.no_grad():
            for _ in range(max_len):
                idx_cond = idx[:, -self.block_size:]
                logits = self(idx_cond)
                logits = logits[:, -1, :]
                probs = F.softmax(logits, dim=-1)
                idx_next = torch.multinomial(probs, num_samples=1)
                idx = torch.cat([idx, idx_next], dim=-1)
        return idx
```

---

## 6. 파라미터 정의(실제 character level을 위해 큰 사이즈로)

32개의 embedding,  4개의 head, 8개의 내부 attention dimension(32/4) , 4개의 layer, 16개의 네트워크가 한번에 볼 수 있는 글자 수

![image.png](/assets/transformer/11_char_level_GPT(_Self_Attention_Masked_Multi_Head_Attention)/image_3.png)

```python
n_embed = 32
n_heads = 4
n_layers = 4
block_length = 16
```

# 성경 데이터 살펴보기

### 데이터 로드

```python
with open("bible.txt", 'r', encoding='utf-8') as f:
	text = f.read()
print(text[:1000])
```

* Genesis 1:1	In the beginning God created the heaven and the earth.
* Genesis 1:2	And the earth was without form, and void; and darkness [was] upon the face of the deep. And the Spirit of God moved upon the face of the waters.
* Genesis 1:3	And God said, Let there be light: and there was light.
* Genesis 1:4	And God saw the light, that [it was] good: and God divided the light from the darkness.
* Genesis 1:5	And God called the light Day, and the darkness he called Night. And the evening and the morning were the first day.

### 성경 구성 확인하기

```python
# here are all the unique characters that occur in this text
chars = sorted(list(set(text)))
vocab_size = len(chars)
print(''.join(chars))
print(vocab_size)
```

!(),-.0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWYZ[]abcdefghijklmnopqrstuvwxyz—’
77

```python
# create a mapping from characters to integers
stoi = { ch:i for i,ch in enumerate(chars) }
itos = { i:ch for i,ch in enumerate(chars) }
encode = lambda s: [stoi[c] for c in s] # encoder: take a string, output a list of integers
decode = lambda l: ''.join([itos[i] for i in l]) # decoder: take a list of integers, output a string
print(encode("nocope deeplearning"))
print(decode(encode("nocope deeplearning")))
```

"nocope deeplearning"의 Encode : [62, 63, 51, 63, 64, 53, 2, 52, 53, 53, 64, 60, 53, 49, 66, 62, 57, 62, 55]

"nocope deeplearning”의 Encode를 다시 Decode 적용 : nocope deeplearning

```python
import torch
encoded_text = encode(text)
data = torch.tensor(encoded_text, dtype=torch.long)
print(text[:100])
print(data[:100])
```

데이터 : 

- KJV
King James Bible: Pure Cambridge Edition - Text courtesy of [www.BibleProtector.com](http://www.bibleprotector.com/)
Genesis 1:1	I

위 데이터의 Encoding 결과 : 

- tensor([32, 31, 43,  1, 32, 57, 62, 55,  2, 31, 49, 61, 53, 67,  2, 23, 57, 50,
60, 53, 19,  2, 37, 69, 66, 53,  2, 24, 49, 61, 50, 66, 57, 52, 55, 53,
2, 26, 52, 57, 68, 57, 63, 62,  2,  7,  2, 41, 53, 72, 68,  2, 51, 63,
69, 66, 68, 53, 67, 73,  2, 63, 54,  2, 71, 71, 71,  8, 23, 57, 50, 60,
53, 37, 66, 63, 68, 53, 51, 68, 63, 66,  8, 51, 63, 61,  1, 28, 53, 62,
53, 67, 57, 67,  2, 10, 19, 10,  0, 30])

학습용 배치만들기.

지금까지 쉬운 설명을 위해 batch size를 1로 두었습니다. 

학습용 데이터셋이 있다면, 이 중 에서 랜덤으로 학습시킬 데이터를 텍스트의 길이만큼 잘라서 사용합니다.

여기서의 사이즈라 함은 트랜스포머가 소화할 수 있는 개수를 말함.

파라미터의 Block의 사이즈를 16으로 두었기 때문에 16개씩 배치를 통해 글자를 뽑아내면 됨.

![image.png](/assets/transformer/11_char_level_GPT(_Self_Attention_Masked_Multi_Head_Attention)/image_4.png)

예를 들어, bacth size가 4라고 아래에서 가정했습니다. 이것이  neural network에 input으로 들어갈 데이터이고, 여기서 loss 계산을 위한 target를 뽑아야 합니다.

character level 레벨의 생성형 neural network는 주어진 character의 다음 글자를 예측하는 것인데, 그 말은 학습용으로 사용할 label은 input의 그 다음 글자면 충분하다는 것입니다.

예를 들어 character a,b,c,d,e순서가 있다고 가정.

![image.png](/assets/transformer/11_char_level_GPT(_Self_Attention_Masked_Multi_Head_Attention)/image_5.png)

a 다음에 대한 글자, a b 다음에 대한 글자, a b c다음에 대한 글자를 예측 해야하는데, 
우리는 a 다음에 올 글자, a b 다음에 올 글자, a b c 다음에 올 글자에 대해서 알고 있습니다.

(a _ / a b _ / a b c _ )에서 ‘_’ 를 예측 해야 하는데, 우리는 예측 해야 할 ‘_’에 대해서 알고 있습니다.

![image.png](/assets/transformer/11_char_level_GPT(_Self_Attention_Masked_Multi_Head_Attention)/image_6.png)

![image.png](/assets/transformer/11_char_level_GPT(_Self_Attention_Masked_Multi_Head_Attention)/image_7.png)

- prevailed upon the earth에 맞는 레이블의 각각의 input에 다음 글자를 우측의 예시처럼 뽑아사용 할 수 있는데 이것이 ground truth가 됨

![image.png](/assets/transformer/11_char_level_GPT(_Self_Attention_Masked_Multi_Head_Attention)/image_8.png)

- 이를 code로 나타내면.

```python
torch.manual_seed(1337)
batch_size = 4 # how many independent sequences will we process in parallel?
block_length = 16

def get_batch(data, batch_size, block_length):
    # generate a small batch of data of inputs x and targets y
    
    ix = torch.randint(len(data) - block_length, (batch_size,))
    # 랜덤으로 block_lenght길이 만큼 데이터를 뽑고, 4개의 배치로 나눠줍니다.
    # 위 사진에서의 and의 맨 앞글자 a, prevailed의 p, (공백)and에서의 공백 .. 
    # 처럼 맨 앞글자를 뽑아냄.
    
    batch_input = torch.stack([data[i:i+block_length] for i in ix])
    # input은 랜덤으로 뽑인 index로 부터 block_length만큼 뽑아냄.
    batch_target = torch.stack([data[i+1:i+block_length+1] for i in ix])
    # Target는 batch input으로 부터 하나씩 shift한 부분을 뽑아냄.
    return batch_input, batch_target

batch_input, batch_target = get_batch(train_data, batch_size=1, block_length=16) #try batch_size=4
print(batch_input)
print(batch_target)
```

batch_input : tensor([[60, 52,  8,  1, 37, 67, 49, 60, 61,  2, 13, 13, 19, 11,  0, 47]])
batch_target : tensor([[52,  8,  1, 37, 67, 49, 60, 61,  2, 13, 13, 19, 11,  0, 47, 29]])

- 보기 쉽게 batch_size를 1로 두었으며, batch_input과 batch_target의 관계를 예측 전과 예측 후로 연관지어 이해할 수 있음.
    1. batch input의 0번째 60 다음으로 올 값은 batch_target의 52. 
    2. batch input의 1번째 52 다음으로 올 값은 batch_target의 8.
    

학습 코드

```python
for steps in range(1000000): # increase number of steps for good results...

    input_batch, target_batch = get_batch(train_data, batch_size, block_length)
    input_batch = input_batch.to(my_device)
    target_batch = target_batch.to(my_device)
    
    logits = model(input_batch)
    logits = logits.view(-1, logits.size(-1))
    target_batch = target_batch.view(-1)
    
    loss = F.cross_entropy(logits,target_batch)
   
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if steps % 10000 == 0:
        print("Step: {}, Loss: {}".format(steps, loss.item()))
        first_idx = torch.zeros((1,1), dtype=torch.long).to(my_device)
        print(decode(model.generate(idx = first_idx, max_len=500)[0].tolist()))
```

학습된 모델을 가지고 character를 하나씩 생성 하는 러프한 절차에 대해서

![image.png](/assets/transformer/11_char_level_GPT(_Self_Attention_Masked_Multi_Head_Attention)/image_9.png)

1. neural network의 output을 확률 softmax를 적용해서  character별 확률로 바꾸고 , 그 중 하나의 character를 뽑아 다시 neural network에 input으로 사용.
    - 예시) 그 하나의 character를 a라고 가정하여, input으로 a를 넣어주고, a 다음 글자 a _ 를 찾아주면 되는데, 이를 neural network에 넣어서 softmax를 통해 a 다음 _ 를 b라는 것을 알 수 있음.
    - 이제, a b에 대해서 알았으니 a b를 다시 neurnal network에 넣어서 a b 다음 _를 찾음. → c의 결과를 얻고, 다시 a b c를 neurnal network에 넣어서 ~~~ .
2. block_length를 16으로 설정 했기 때문에, 예측한 character의 block_length가 16이 넘어가면, 앞의 character를 활용하여 neural network input으로 들어갈 수 없음.
3. input에 대해서 output의 -1번째. 즉, 맨 마지막 character 예측 하는 것이 중요하고 나머지는 무시해도 무방할 정도임. 아래 generate 코드를 살펴볼 수 있음.
    
    ![image.png](/assets/transformer/11_char_level_GPT(_Self_Attention_Masked_Multi_Head_Attention)/image_10.png)
    
    ```python
    class TransformerGen(nn.Module):
        def __init__(self, char_size, embed_dim, n_heads, n_layers, block_size):
            super().__init__()
            pass
        def forward(self, x):
    	    pass
    
        def generate(self, idx, max_len=100):
            with torch.no_grad():
                for _ in range(max_len):
                    idx_cond = idx[:, -self.block_size:]
                    logits = self(idx_cond)
                    logits = logits[:, -1, :] # 맨 마지막 character 예측 값만 가져온다.
                    probs = F.softmax(logits, dim=-1) # 맨 마지막 character 예측 값의 P.
                    idx_next = torch.multinomial(probs, num_samples=1) # P에 기반한 index뽑아
                    idx = torch.cat([idx, idx_next], dim=-1) 
                    # 현재 글자idx, 예측 글자idx_next를 붙혀서 idx로 만들어서, 
                    # for loop를 통해 input으로 넣어줌 : idx_cond = idx[:, -self.block_size:]
            return idx
    ```
    

다시, 학습 코드로 돌아와서. 성경을 character level로 학습해서 transfomer decoder를 만들었고  실행하면.

step0. 맨 처음 step에서는 성경의 형태는 아니지만, epoch별로 점 점 더 성경같은 output을 생성해 나아갑니다.

```python
for steps in range(1000000): # increase number of steps for good results...

    input_batch, target_batch = get_batch(train_data, batch_size, block_length)
    input_batch = input_batch.to(my_device)
    target_batch = target_batch.to(my_device)
    
    logits = model(input_batch)
    logits = logits.view(-1, logits.size(-1))
    target_batch = target_batch.view(-1)
    
    loss = F.cross_entropy(logits,target_batch)
   
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if steps % 10000 == 0:
        print("Step: {}, Loss: {}".format(steps, loss.item()))
        first_idx = torch.zeros((1,1), dtype=torch.long).to(my_device)
        print(decode(model.generate(idx = first_idx, max_len=500)[0].tolist()))
```

```
Step: 0, Loss: 4.4446539878845215
	LeRiL02B’PDt-[8TgaGMHsID(	InkpWQN(VmBo]?!T-]aWM6F?w;VYrsYQrb	f6FBIgDqMT4wehOG?]Uzlx3eWVFwlh9euBoCO7C(GRC4;e[OcftpoDGG7SRM
q9	q	S w!tIWGn[P(W	Q4a9wbE]b-Z6EICo[k[gO3m]VWYJF3
Em[Wle-T9(bStIjfgb g )—T6iwckh696MIBvH
tEHI2rItg’s8L]syag3JYgZ W)k.	Cf]]) vO5’9(YW0o9l8HW,x xseYIDd’(eW5	)qg)K5(6kl7tbV!)xZkg[[xMbdMlhIDwW		a6uKyT		Ab6BpNg kp5J
vp’oSD385P!]v:YcF;eVMhI!MggpBjW)WWvB?YHkIWgg(Shl G	:B9-W4tmaW;’0Op9xrnpffaU y(;OnQzwnV7)DuYOO[jWI[ JCv):M-kfiHi
nmq—)VpBHl9p5VyKn2QHaS?p4Lg5ty],;BM]][F)hg9V.9-?A3Ml9W
```

```
Step: 10000, Loss: 1.5253053903579712
	Hank when hear unto fas the securve healf [it are wildes on; as] kings.
1 Kis 17:4	Asn fo; the dease, wall to the shall take onher Begair] wired, were sayity, He house sidituldonys, [and] taker of God, and and eer, and ways Jordin.
Jornes.
2 Keprare 2:41	An, the portigighte, and offame to degrforge and everabiy to day, them and gord thine hiss and have servigeth to jecave heark gord tonst, and aris said.
Iyessalm 24:1	Sroice they of their heart spake the earred, tild.
Proar 12:17	And lern a man
```

```
Step: 20000, Loss: 1.571069359779358
	And that said poor Ouberning of the boctring the eart wiles.
Jeremiah 58:30	Foolon amotnoot be him.
Luke 28:3	Jesther out of Corys charmled abents, and may writh the save opemparael: therefore hath thou prople, and was vine yourt of withith me son; I was the sor as with a said wim [is] we gondoml be the turne man the could thy vear: a [how] there sons upon the sorrinjudg of the LORD grecoung have there set with the sapcord unto mallasi to my out of ornad; but, and they deday.
1 Chronicles 0:8	Th
```

```
Step: 830000, Loss: 1.342114806175232
	Again the other duker know that hateth in their boad in him about basgorm? at I ask now.
John 12:39	Of Pharaoh he shall fill:
2 Chronicles 11:20	In the image, and all thy conto awty, and the dand of you also whereory the evil.
Zechariah 6:2	Saint up he also that they covered him into the high of thyreof,
Ezekiel 39:25	They seed told sore Levites, and all the land, [is] a dew?
2 Hamus 28:5	That I may brethren him with the eeters was are no woman; they breadst them.
Job 4:12	Now hundred over; for
```