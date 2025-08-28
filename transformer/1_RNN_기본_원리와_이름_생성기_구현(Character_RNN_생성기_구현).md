# 1. RNN 기본 원리와 이름 생성기 구현(Character RNN 생성기 구현)

![image.png](/assets/transformer/1_RNN_기본_원리와_이름_생성기_구현(Character_RNN_생성기_구현)/image.png)


한번에 표현하거나, 시간의 순서에 따라 표현하거나. 모두 동일한 RNN

 

![image.png](/assets/transformer/1_RNN_기본_원리와_이름_생성기_구현(Character_RNN_생성기_구현)/image_1.png)

![image.png](/assets/transformer/1_RNN_기본_원리와_이름_생성기_구현(Character_RNN_생성기_구현)/image_2.png)

“The” 단어 벡터가 input으로 들어가면, 내부의 0의 값을 가지는 hidden state h0가 input과 붙으면서 

fully connection layer tanh를 통해 hidden state h1을 업데이트함.

![image.png](/assets/transformer/1_RNN_기본_원리와_이름_생성기_구현(Character_RNN_생성기_구현)/image_3.png)

food 단어 vector가 input으로 들어가고, 기존의 hidden state h1이 input과 붙으면서 fullyconnection layer tanh를 통해 hidden state h2를 업데이트함

![image.png](/assets/transformer/1_RNN_기본_원리와_이름_생성기_구현(Character_RNN_생성기_구현)/image_4.png)

최종적으로 모든 vector에 hidden state ~ fullyconnection layer tahn ~ hidden state h4를 업데이트 하고나면 최종 output tensor를 통해 해당 문장의 postive, negative 구분을 함

위 설명에 대한 코드.

```python
import torch
import torch.nn as nn

class MyRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size)
    # input_size, hidden_size = 4, output_size = 2 
        super().__init__()

        self.hidden_size = hidden_size
        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.h2o = nn.Linear(hidden_size, output_size) 

    def forward(self, input, hidden):
        combined = torch.cat((input, hidden))
        hidden = torch.tanh(self.i2h(combined))
        output = self.h2o(hidden)
        return output, hidden

    def get_hidden(self):
        return torch.zeros(1, self.hidden_size)
  
rnn_model = MyRNN(input_size=4, hidden_size=4, output_size=2 )
hidden = rnn_model.get_hidden()

# the food is good
  
# output_tensor0, hidden = rnn_model(input_tensor0, hidden) # the
# output_tnesor1, hidden = rnn_model(input_tensor1, hidden) # food
# output_tensor2, hidden = rnn_model(input_tensor2, hidden) # is
# output_tensor3, hidden = rnn_model(input_tensor3, hidden) # good

_, hidden = rnn_model(input_tensor0, hidden) # hidden layer만 알면 됨
_, hidden = rnn_model(input_tensor1, hidden) # hidden layer만 알면 됨
_, hidden = rnn_model(input_tensor2, hidden) # hidden layer만 알면 됨
output_tensor3, _ = rnn_model(input_tensor3, hidden) # out layer만 알면 됨

# 좀 더 복잡하게 하기 위해서는 hidden_size를 늘리거나, 여러 층을 쌓아주면 됨.

```

# CHARACTER LEVEL Classification RNN

![image.png](/assets/transformer/1_RNN_기본_원리와_이름_생성기_구현(Character_RNN_생성기_구현)/image_5.png)

이름 기반 성별 분류 RNN

이 모델은 이름의 철자를 문자 단위(character-level_로 받아, RNN을 통해 성별을 예측합니다.

1. 각 문자는 26개의 알파벳에 대한 one-hot encoding 형태로 표현됨. 예로, `"abby"`의 경우 `'a'`, `'b'`, `'b'`, `'y'` 각각이 길이 26짜리 one-hat vector로 변환됨.
2. RNN의 입력 차원은 26(알파벳 개수)이고, 은닉 상태(hidden state)는 크기 32개의 vector를 사용함.
3. RNN은 각 시점(time step)마다 입력 문자 vector와 이전 시점의 은닉 상태를 결합해 새로운 은닉 상태를 계산함.
    1. 1번째 시점: `'a'` → h₁ 계산
    2. 2번째 시점: `'b'` + h₁ → h₂ 계산
    3. 3번째 시점: `'b'` + h₂ → h₃ 계산
    4. 4번째 시점: `'y'` + h₃ → h₄ 계산
4. 마지막 시점의 은닉 상태 h₄는 최종 출력층으로 전달되어, `[1, 0]`(예: 남성), `[0, 1]`(예: 여성) 형태의 라벨과 비교됩니다.
    - 예측값과 실제 라벨 간의 **Cross Entropy Loss**를 계산한 뒤, 역전파(Backpropagation)를 통해 가중치를 업데이트합니다.
    - 전체 이름 데이터셋에 대해 이 과정을 반복하면, 이름을 기반으로 성별을 예측하는 모델이 학습됩니다

관련 코드는 https://github.com/lee-edgar/study/blob/main/rnn/genderClassification.ipynb에서 확인 가능.

# Generation이 적용된 RNN

![image.png](/assets/transformer/1_RNN_기본_원리와_이름_생성기_구현(Character_RNN_생성기_구현)/image_6.png)

이미지를 RNN 기반의 신경망(Neural Network)에 넣으면,

**강아지일 확률**과 **고양이일 확률**을 나타내는 점수(Score)를 출력합니다.

예를 들어,

- 고양이 점수: 2
- 강아지 점수: -3

이 점수에 **Softmax**를 적용하면,

- 고양이: 98%
- 강아지: 2%

이 값들이 분류 확률(Classification Probability)가 됩니다.

즉, 모델이 “이 이미지는 고양이일 확률이 98%”라고 판단하는 것입니다.

이런 분류 원리는 이미지 인식뿐 아니라, 텍스트 생성·이미지 생성 같은 생성 모델(Generation)에도 응용될 수 있습니다.

![image.png](/assets/transformer/1_RNN_기본_원리와_이름_생성기_구현(Character_RNN_생성기_구현)/image_7.png)

알파벳을 예를 드는데, 간단히 하기 위해 a,b,c로 대신함.

예를 들어,

- a  점수 : 2
- b 점수 : 1
- c 점수 : -1

이 점수에 softmax를 적용하면,

- a : 0.7
- b : 0.26
- c : 0.04

이를 확률 분포로 보고, 하나의 character로 sampling 하면 해당 확률에 따른 알파벳을 선택할 수 있음. → 이렇게 선택된 알파벳 하나가 생성모델로 부터 나오는 하나의 character임.

확률에 따른 sampling code

```python
import torch

probability = torch.tensor([0.7, 0.2, 0.1])

print(f"sampled index: {torch.multinomial(probability, 1).item()}")
print(f"sampled index: {torch.multinomial(probability, 1).item()}")
print(f"sampled index: {torch.multinomial(probability, 1).item()}")
print(f"sampled index: {torch.multinomial(probability, 1).item()}")
print(f"sampled index: {torch.multinomial(probability, 1).item()}")
print(f"sampled index: {torch.multinomial(probability, 1).item()}")
print(f"sampled index: {torch.multinomial(probability, 1).item()}")
print(f"sampled index: {torch.multinomial(probability, 1).item()}")
print(f"sampled index: {torch.multinomial(probability, 1).item()}")

sampled index: 0
sampled index: 1
sampled index: 0
sampled index: 0
sampled index: 0
sampled index: 2
sampled index: 0
sampled index: 0
sampled index: 0
```

- 70%의 확률 : 0
- 20%의 확률 : 1
- 10%의 확률 : 2

![image.png](/assets/transformer/1_RNN_기본_원리와_이름_생성기_구현(Character_RNN_생성기_구현)/image_8.png)

위와 같은 sampling을 RNN에 적용.

input : 26개

- 알파벳  26개 + <'S'> 시작 토큰 1개, <'E'> 종료 토큰 1개

생성 모델로 부터 첫 번째 character를 출력하기 위해서는 RNN에 시작 토큰을 넣어주고, 생성을 마무리 하는 끝 토큰도 넣어 줘야함.

→ 생성할 output인 이름의 길이는 정해져 있지 않음. 즉, 짧은 이름도 있고 긴 이름도 있기 마련인데, 끝을 의미하는 <'E'> 토큰을 넣어줘야 생성을 멈출 수 있음

28개의 input vector로 rnn을 생성하고, hidden state를 1024로 가정하고, output은 28개로 가정함(input과 같이)

- output에서는 <'S'> 시작 토큰이 필요 없으나, 어차피 training을 통해 시작 토큰이 output으로 나올 확률은 0에 가깝기에 output vector size를 28로 두어도 무방함.

![image.png](/assets/transformer/1_RNN_기본_원리와_이름_생성기_구현(Character_RNN_생성기_구현)/image_9.png)

1. RNN으로 one-hot encoding 된 <'S'> 토큰이 들어옴. 
2. 초기값을 가진 hidden state h0가 concatnation 되면서 내부 hidden state h1을 업데이트 함
3. 그에 따른 output  score를 구해 softmax 적용 
4. softmax 값을 확률 분포로 바꿈.
5. 주어진 확률 분포값을 바탕으로 sampling을 통해 나온 character 하나가 RNN생성 모델에서 나온 첫 번째 character가 됨

1 ~ 5번의 과정을 <'S'>, 26개의 알파벳, <'E'> 만큼 iter하며, 이때 h값은 증가하게 됨.

<'E'> 끝 토큰이 들어오게 되면, 이름 생성을 멈추고 RNN은 최종 ‘LEO’라는 이름을 만들어 냄.

→ 1번째는 L, 2번째는 E, 3번째는 O, 4번째 <'E'> 토큰을 받으면서 이름 생성을 마무리.

코드로 구현

```python
import pandas as pd
import torch

df = pd.read_csv('./deepLearning/rnn/name_gender_filtered.csv')
unique_chars = set()

for name in df['Name']:
    unique_chars.update(name)
sorted_chars = sorted(list(unique_chars)) # set으로 중복제거
df

```

![image.png](/assets/transformer/1_RNN_기본_원리와_이름_생성기_구현(Character_RNN_생성기_구현)/image_10.png)

```python
sorted_chars = sorted(set(''.join(sorted_chars)))
stoi = {s:i for i,s in enumerate(sorted_chars)}#문자와 인덱스 dict 매핑
stoi['<S>'] = len(stoi)
stoi['<E>'] = len(stoi)
itos = {i:s for s,i in stoi.items()} # 인덱스와 문자의 dict 매핑
print(itos)
print('--')
print(stoi)
```

itos (*index:string dict mapping): {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z', 26: '<'S'>', 27: '<'E'>'}
—
stoi (*string :index dict mapping) :`{'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25, '<'S'>': 26, '<'E'>': 27}`

```python
import torch
import torch.nn.functional as F

def name_to_one_hot(name):
# 주어진 이름으로 원핫 인코딩 된 텐서를 만드는 함수
    # 시작 및 종료 토큰 추가
    tokenized_name = ['<S>'] + list(name) + ['<E>']
    # 문자를 정수 인덱스로 변환
    int_tensor = torch.tensor([stoi[char] for char in tokenized_name])
    # 원핫인코딩
    one_hot_encoded = F.one_hot(int_tensor, num_classes=len(stoi)).float()
    return one_hot_encoded

print(name_to_one_hot("nocope"))
```

![image.png](/assets/transformer/1_RNN_기본_원리와_이름_생성기_구현(Character_RNN_생성기_구현)/image_11.png)

이름 ‘nocope’에 대한 텐서의 결과임

- 토큰화: `['<'S'>', 'n', 'o', 'c', 'o', 'p', 'e', '<'E'>']`
- 인덱스 변환: `[26, 13, 14, 2, 14, 15, 4, 27]` (예시)
- 원-핫 인코딩: shape `(8, 28)`
    - 8은 문자의 개수(시작+6글자+종료)
    - 28은 전체 vocabulary 크기 (a-z + <'S'>, <'E'>)

### RNN정의

```python
import torch.nn as nn
n_letters = len(stoi)

class MyRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()

        self.hidden_size = hidden_size
        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.h2o = nn.Linear(hidden_size, output_size)

    def forward(self, input, hidden):
        combined = torch.cat((input, hidden), 1)
        hidden = torch.tanh(self.i2h(combined))
        output = self.h2o(hidden)
        return output, hidden

    def get_hidden(self):
        return torch.zeros(1, self.hidden_size)

n_hidden = 1024
rnn_model = MyRNN(n_letters, n_hidden, n_letters)
```

### 이름 생성 DEF

```python
@torch.no_grad()
def generate_name():
    rnn_model.eval()
    start_token_idx = torch.tensor(stoi['<S>']) # 시작토큰 처음 넣기
    one_hot_encoded = F.one_hot(start_token_idx, num_classes=len(stoi)).float()
    hidden = rnn_model.get_hidden()
    char_list = []
    for i in range(20): 
		    # 1. RNN Model을 통해서 나온 score텐서(out_score[0])
        out_score, hidden = rnn_model(one_hot_encoded[None,:],hidden)
        # 2. softmax를 적용해 확률분포로 변경
        score_probability = F.softmax(out_score[0], dim=-1)
        # 3. 확률분포로 샘플링
        out_idx = torch.multinomial(score_probability, 1).item()
        # 4. Ending 토큰 <'E'>가 나오면 이름 생성 break
        if out_idx == stoi['<E>']:
            break
        char_list.append(itos[out_idx])
        one_hot_encoded = F.one_hot(torch.tensor(out_idx), num_classes=len(stoi)).float()
    print(''.join(char_list))

generate_name()
```

- **목적:** 학습된 RNN으로 문자 단위 **이름을 생성**
- **핵심 흐름:**
    1. `<'S'>`(시작 토큰)를 원-핫으로 만들어 **첫 입력**으로 사용
    2. `rnn_model(one_hot[None, :], hidden)` → **점수(score)**와 **다음 hidden** 출력
        - `one_hot[None, :]` : 배치 차원 추가 `(1, vocab)`
    3. `softmax`로 **확률분포** 계산
    4. `torch.multinomial`로 **샘플링**해 **다음 글자 인덱스** 선택
    5. `<E>`가 나오면 **종료**, 아니면 이어서 **다음 입력**으로 사용
    6. 최대 길이(예: 20) 도달 시 안전 종료
- `@torch.no_grad()` + `eval()` : **추론 모드**, 그래디언트/드롭아웃 비활성화

> 현재는 “학습 전”이라 무작위 문자열이 나오는 것이 정상
> 
> 
> (예: `lojg`, `culdle`, `cagken`)
> 

학습을 진행 후 우리가 원하는 값(기대하는 값)

![image.png](/assets/transformer/1_RNN_기본_원리와_이름_생성기_구현(Character_RNN_생성기_구현)/image_12.png)

- input : <'S'> → output : L
- input :L → output : E
- input : E → output : O
- input : O → output : <'E'>

즉, <'S'>를 RNN 모델에 input하여, h1이 업데이트가 되면서 softmax 적용된 스코어의 값이 우리가 기대하는 output값은 L이고, 이러한 기대를 loss로 표현하여 one hot eocnding 된 gt와 비교하면서 Loss0. → 1epoch를 돌면서 loss1, loss2, loss3를 구할 수 있음

최종 전체 loss를 구하면 되는데, 각각의 character쌍으로 나온 loss들을 더해주면 됨샛total loss = (loss0+loss1+loss2+loss3)

total loss를 기반으로 backpropagation 수행하면서 weight 업데이트 하면, 트레이닝의 1싸이클이 진행 된 것임. 이 과정을 leo뿐만 아니라 모든 이름에 대해서 학습을 진행한다면, 해당 rnn 모델은 이름을 생성하는 생성기 모델이 됨.

### 학습 코드

```python

from torch.optim import Adam

loss_fn = nn.CrossEntropyLoss()
optimizer = Adam(rnn_model.parameters(), lr=0.0001)

for epoch_idx in range(100):
    shuffled_df = df.sample(frac=1).reset_index(drop=True)
    crnt_loss = 0.
    rnn_model.train()
    for index, row in shuffled_df.iterrows():
				# 1. 이름 데이터를 가져와서 <S>, <E>의 원핫 인코딩 텐서 받아옴.
        name_one_hot = name_to_one_hot(row['Name'])
        hidden = rnn_model.get_hidden()
        rnn_model.zero_grad()

        losses = []
        # 2. 각 character 별로 input tesnor, target tensor를 받아
        for char_idx in range(len(name_one_hot)-1):
            input_tensor = name_one_hot[char_idx]
            # target_char : rnn input으로 들어가는 바로 다음 charcater
            target_char = name_one_hot[char_idx+1]  
            target_class = torch.argmax(target_char, -1)
            # target_char 매칭된 output score를 받아 crossentropy 계산.
            out_score, hidden = rnn_model(input_tensor[None,:],hidden)
            # loss list append
            losses.append(loss_fn(out_score[0], target_class))
        # 3. 전체 loss 구하기
        loss = sum(losses)
        # 4. backpropagation
        loss.backward()
        optimizer.step()
        crnt_loss += loss.item()

    generate_name()
    average_loss = crnt_loss / len(df)

    print(f'Iter idx {epoch_idx}, Loss: {average_loss:.4f}')

```

### 학습 이후 이전(랜덤한 알파벳)과 다르게 좀 더 이름에 가까운 character 생성

```python
generate_name()
generate_name()
generate_name()
generate_name()
generate_name()
generate_name()
generate_name()
generate_name()
generate_name()
generate_name()
```

- ceairi
- lewnor
- valgwin
- shala
- ezmera
- raffamau
- kia
- jenavieve
- carlette
- sheily

확률값들중 0.01의 아주 낮은 확률값이 선택 된다면, 살짝 이상한 이름이 생성 될 수는 있음.

![image.png](/assets/transformer/1_RNN_기본_원리와_이름_생성기_구현(Character_RNN_생성기_구현)/image_13.png)

이를 해결 하기 위해 보수적으로, 최소한 10%가 되는 확률만 선택되도록 조건을 걸어 낮은 확률의 샘플링 값을 쳐낼 수 있음

RNN 다시 한번, 가볍게 복습

### RNN 기반 문장 분류 (Classification Model)

![image.png](/assets/transformer/1_RNN_기본_원리와_이름_생성기_구현(Character_RNN_생성기_구현)/image_14.png)

1. 첫 hidden0과 thsi vector가 만나서 업데이트하여 hidden1을 생성
2. hidden1에 food vector가 만나서 업데이트하여 hidden2를 생성
3. hidden2에 is vector가 만나서 업데이트하여 hididen3을 생성
4. hidden3에 good vector가 만나서 업데이트하여 hidden4를 생성.
5. hidden4 생성 이후 문장이 끝났기 때문에 내부 히든스테이드(hidden4)를 기반으로 output tensor를 생성
6. output tensor를 바탕으로 주어진 문장이 postive, negative인지 classification 수행

### RNN 기반 문장 생성 (Generation Model)

rnn 기반 generation model. <'S'>, I, Love, you, <'E'>

![image.png](/assets/transformer/1_RNN_기본_원리와_이름_생성기_구현(Character_RNN_생성기_구현)/image_15.png)

1. rnn에 처음시작 <'S'>을 주면, 처음 내부 히든 스테이트와 합쳐(hidden 0) 업데이트하고 hidden1을 생성
2. 이를 기반으로 output tensor를 그려내고 
3. 확률분포. softmax로 바꿔 sampling하면 하나의 단어를 추출 할 수 있음.
4. 해당 단어를 rnn의 두 번째 input으로 들어가고 이를 vector화 시켜 rnn에 다시 넣으면 , 기존의 hidden state와 합해져서 내부 state를 한번더 update하여 hidden2 생성하고, 1~3번째를 다시 반복함.
5. 마지막 you를 넣어서 sampling했을 때, <'E'> 엔딩 토큰이 나오게 함.

### RNN 기반 번역 구조: Encoder–Decoder 메커니즘

rnn으로 classification과 genration을 할 수 있고, 번역. translation을 할 수도 있음.

![image.png](/assets/transformer/1_RNN_기본_원리와_이름_생성기_구현(Character_RNN_생성기_구현)/image_16.png)

길이가 정해져 있지 않은 “I am hungry”를 “나는 배고프다”로 번역하는 것이 전형적인 sequence to sequence라고 할 수 있음. 이를 rnn으로 만들어 낸다고 하면, 

1. rnn에 I, am, hungry에 해당하는 vector가 순차적으로 들어가고, hidden state는 vector화 된 어떠한 상태를 가지고 있음
2. 이 상태로 부터 generation model을 적용하면 번역이 되는 것임.
3. vector화 된 hidden state를 가져와서 처음 <'S'> 토큰을 넣어줌
4. hidden state를 업데이트하고 output tesor가 나오고 softmax를 적용해 확률분포를 얻고 그 중 가장 높은 확률의 값을 뽑는데 그 값은 “나는”이 될 것임
5. 이 “나는” 값을 다시 RNN에 넣고, 이전 hidden state( hidden0 → <'S'> → hidden1)를 받아서 업데이트 후 softmax를 통해 가장 높은 값의 단어 “배고프다”를 가져옴.
6. “배고프다”를 다시 rnn에 넣어서 이전의 hidden state를 받아 업데이트하고, <'E'> output을 낼 수 있음

여기서 어떠한 hidden state를 가지는 vector화 된 상태. 번역 RNN부분을 두 부분으로 나눌 수 있음.

1. input에 대한 모든 정보를 hidden state에 넣는 부분 : Encoder
2. 모든 정보가 들어있는 hidden state로 부터 출력을 만들어 내는 부분 : Decoder

만약 문장의 길이가 매우 길다면, 더 많은 RNN이 필요하고, backpropagation하는 과정에서의 gradient가 무수히 많이나오게 될 것이며,  번역을 위해 아주 많은 정보가 작은 hidden state로 모두 encoding이 되야하기에 과거에는 LSTM, GRU가 나왔고, 현재는 transformer가 모두 대체함.