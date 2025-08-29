# 트랜스포머 이론 전체(with_나동빈)

2021년 기준으로 현대의 자연어 처리 네트워크에서 핵심이 되는 논문입니다.  
논문의 원제목은 **Attention Is All You Need**이며, 트랜스포머는 RNN이나 CNN을 전혀 필요로 하지 않는 특징을 가지고 있습니다.

![image1.png](/assets/transformer/트랜스포머_이론_전체(with_나동빈)/image1.png)

문장 단어의 순서 정보를 주기 어려워 **positional encoding**을 사용하여 순서에 대한 정보를 줄 수 있습니다. 

![image2.png](/assets/transformer/트랜스포머_이론_전체(with_나동빈)/image2.png)

문장을 input embededding matrix에 넣게 되면, 각 단어와 embed_dim으로 구성된 matrix.

![image3.png](/assets/transformer/트랜스포머_이론_전체(with_나동빈)/image3.png)

RNN을 사용하지 않기 때문에 트랜스포머는 위치 정보를 포함하고 있는 임베딩을 사용해야 하기 때문에,  
input embedding matrix와 동일한 차원을 가지는 positional encoding matrix를 만들어서 element-wise하여 더해줍니다.  
→ 이를 통해 network에서 단어의 순서를 알 수 있습니다.

### Positional Encoding. attention을 통해 연관성 높은 단어 정보를 학습

![image4.png](/assets/transformer/트랜스포머_이론_전체(with_나동빈)/image4.png)

위치에 대한 정보. positional encoding 정보를 multi-head attention에 넣어서 임베딩이 끝난 이후 attention을 진행하게 됩니다.  

즉, 입력 문장의 정보와 입력 문장의 포지션 정보를 input으로 하여 multi-head attention에 넣어주는 것입니다.  

“임베딩이 끝난 이후에 어텐션(attention)을 진행한다” : encoder 파트에서 사용되는 attention은 self-attention이라고 해서 각각의 단어가 서로에게 어떠한 연관성 스코어를 통해 연관성이 높은 단어들의 정보를 학습 하는데 사용 할 수 있습니다. 

### 잔여학습(Residual learning). 빠른 Global optima 찾기

![image5.png](/assets/transformer/트랜스포머_이론_전체(with_나동빈)/image5.png)

추가적으로 **Residual Learning** 테크닉을 사용합니다.  
어떠한 값을 layer를 거쳐서 단순히 반복적으로 갱신하는 게 아니라 특정 layer를 건너뛰면서 복사가 된 값을 그대로 넣어주는 기법을 사용합니다.  

이렇게 해줌으로써 전체 네트워크는 기존 정보를 입력 받으면서 추가적으로 잔여된 부분만 학습하도록 하기 때문에  
모델의 수렴 속도가 빨라지고, 학습 난이도가 낮아지면서 global optima를 찾을 확률이 높아지기 때문에 residual learning을 채택합니다.  

이후 Normalization을 적용하여 결과를 내보냅니다.

### 전체 Encoder와 Decoder 수행 순서

![image6.png](/assets/transformer/트랜스포머_이론_전체(with_나동빈)/image6.png)

Encoder에 입력값이 들어오고, 여러 개의 encoder layer를 반복하여  
가장 마지막에서 나온 encoder 출력 값이 Decoder의 두 번째 Multi-head Attention에 들어가게 됩니다.  

Decoder 파트에서는 매번 출력할 때마다 입력 소스 문장 중에서 어떤 단어에 가장 많은 초점을 두어야 하는지 알려주기 위함입니다.  

Decoder 파트도 여러 개의 layer로 구성되며 마지막 layer에서 나온 출력 값이 실제로 번역을 수행한 결과가 되는 것이며,  
이때 각각의 Decoder Layer는 Encoder 마지막 Layer에서 나온 출력값을 입력으로 받습니다.

![image7.png](/assets/transformer/트랜스포머_이론_전체(with_나동빈)/image7.png)

- 일반적으로 트랜스포머에서 layer 개수는 encoder와 decoder는 동일하게 맞춰줍니다.

![image8.png](/assets/transformer/트랜스포머_이론_전체(with_나동빈)/image8.png)

- 트랜스포머에서도 encoder, decoder의 구조를 따르게 되는데, RNN을 사용하지 않으며, encoder와 decoder를 다수 사용합니다.

### RNN(LSTM)과 Transformer의 작동 차이

- RNN, LSTM을 사용할 때는 고정된 크기를 사용하고 입력 단어의 개수만큼 반복적으로 Encoder layer 거쳐서 매번 hidden state 만들었다고 하면,  
- Transformer에서는 입력 단어 자체가 하나로 쭉 연결되어서 한 번에 입력이 되고 한 번에 attention 값을 구할 수 있습니다.  

즉, 위치에 대한 정보를 한꺼번에 넣어서 한 번에 encoder를 거칠 때마다 병렬적으로 출력값을 구해낼 수 있기 때문에  
일반적인 RNN 사용했을 때와 비교하여 계산 복잡도가 낮게 형성됩니다.

![image9.png](/assets/transformer/트랜스포머_이론_전체(with_나동빈)/image9.png)

**Scaled Dot-Product Attention** :  

각각의 단어가 다른 단어와 얼마나 연관성이 있는지 구하는 것입니다.  
예: *i am a teacher*라는 문장이 있을 때, 각각의 단어가 다른 단어와 얼마나 연관성을 가지는지 위해서 self-attention을 측정.  

- Query : 무언가를 물어보는 주체 → *i*  
- Key : 무언가를 물어보는 대상 → *i, am, a, teacher*  

query가 key에 대해서 attention score를 구해서 value 값과 곱해 attention value 값을 구하는 방식.

**Multi-Head Attention** :  

1. 입력으로 들어온 값들은 세 개로 복제가 되어서 각각 Value, Key, Query로 들어가게 됨  
2. 각각의 Value, Key, Query는 Linear layer에서 행렬곱 연산  
3. h개로 구분된 각각의 쿼리 쌍들을 만들어냄 (여기서 h는 head의 개수)  
4. attention에서 입력값과 출력값을 concat → 동일한 dimension 유지 후 Linear 수행  

![image10.png](/assets/transformer/트랜스포머_이론_전체(with_나동빈)/image10.png)

1. **Encoder Self-Attention** : 각각의 단어가 서로 어떠한 연관성을 가지는지 attention을 통해 구하고, 전체 문장에 대한 representation을 running 할 수 있도록 함.  
2. **Masked Decoder Self-Attention** : Decoder에서 self-attention을 수행할 때는 각각의 출력 단어가 다른 단어들을 모두 참고하지 않고, 앞쪽 단어만 참고 가능.  
   - 예: “나는 축구를 했다” → “나는 축구를”까지만 알고 뒤의 “했다”는 참고 불가 (치팅 방지).  
3. **Encoder-Decoder Attention** : query는 decoder에 있고, key와 value는 encoder에 있음.  
   - 즉, 각각의 출력 단어(decoder)가 입력 단어(encoder)들 중 어떤 단어에 가중치를 줄지 계산.

![image11.png](/assets/transformer/트랜스포머_이론_전체(with_나동빈)/image11.png)

예를 들어, 위와 같은 입력 문장이 들어왔을 때, 각각의 단어들은 모든 단어들에 대해서 attention score 값을 구할 수 있음(가중치를 어떻게 주는지를 계산).

![image12.png](/assets/transformer/트랜스포머_이론_전체(with_나동빈)/image12.png)

![image13.png](/assets/transformer/트랜스포머_이론_전체(with_나동빈)/image13.png)

일반 임베딩 값에 **Positional Encoding 함수(PE)**를 적용해 위치 인코딩 matrix를 뽑아낼 수 있음.
