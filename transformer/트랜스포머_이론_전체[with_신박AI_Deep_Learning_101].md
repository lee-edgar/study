# 트랜스포머 이론 전체[with 신박AI_Deep Learning 101]

## 1. transformer의 self attention메커니즘이 왜 대단한지 ?

![image1.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image1.png)

기존 attention 연구는 입력 시퀀스와 출력 시퀀스 간의 관계에 주목을 했었습니다.

![image2.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image2.png)

트랜스포머의 self-attention은 시퀀시 안에 단어와 단어의 상관관계에 주목을 했다는 것이 획기적인 사고의 전환이라고 할 수 있습니다.

![image3.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image3.png)

단어와 단어의 상관관계를 구하기 위해서 같은 입력 행렬을 두 개의 분리된 네트워크에 넣어서 Q행렬과 K행렬을 만들어 단순히 두 행렬을 곱하는 것만으로 단어와 단어의 상관 관계를 볼 수 있습니다.

이는 입력 문장의 단어를 하나하나 처리하지 않고 모든 단어를 한번에 병렬적으로 처리할 수 있기 때문에 속도가 빠르고, 긴 문장이라고 하더라도 각각의 모든 단얻르 간의 관계를 차별없이 계산할 수 있습니다.

![image4.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image4.png)

실제 트랜스포머 논문에서는 영어-독일어 번역 학습을 위해 37,000개의 토큰을 사용했으나, 설명을 위해 11개의 토큰을 사용합니다.

## 2. Encoder

### input 문장의 embedding vector를 통해 밀집 vector 생성

![image5.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image5.png)

입력 문장이 들어갈때, 단어의 embedding을 처리하는데, 입력 단어 5, 8, 9가 들어왔을때, 각각의 단어들의 embedding vector를 출력합니다. embedding layer는 11개의 단어들을 압축해 길이가 6인 밀집 vector로 바꿔주는 layer입니다.

### 1. Position Encoding

![image6.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image6.png)

트랜스포머에서의 독특한 문장 내 단어의 위치 인코딩 : position encoding

영어는 어순이 매우 주요한데, 단어 순서에 따라 그 의미가 완전히 달라지기 때문입니다.

- The dog bites the man ( 그 개가 그 남자를 물었어요.)
- The men bites the dog (그 남자가 그 개를 물었어요.)

![image7.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image7.png)

고유한 위치정보를 같이 준다면, 개가 물었는지, 개가 물렸는지를 의미를 정확하게 전달 할 수 있으며, 이 경우 트랜스포머가 문장 전체의 의미를 더 잘 처리할 수 있게 된다는 것을 의미합니다.

![image8.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image8.png)

해당 예제에서의 $d_{model}$의 길이는 6이며, pos 포지션에 0, 1, 2가 차례대로 들어가게 됩니다.

![image9.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image9.png)

- 짝수번째 단어에 해당하는 i는 좌측 공식에 대입.

![image10.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image10.png)

- 홀수번째 단어에 해당하는 i는 우측 공식에 대입.

![image11.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image11.png)

단어의 짝수, 홀수에 맞게 각각의 공식을 대입해 위치 인코딩 값을 계산 할 수 있습니다.

### 2. input embedding vector + position embedding vector.

![image12.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image12.png)

계산된 위치 임베딩과 입력 임베딩을 더해서 input embedding vector + position embedding vector를 구할 수 있습니다.

## 3. multi head attention

### Seq2Seq attention vs Transformer Attention

![image13.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image13.png)

<Seq2seq attention>  
Seq2seq에서 살펴본 attention은 입력 시퀀스와 출력 시퀀스 간의 주목해야할 단어를 찾는 어텐션이었다면,

![image14.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image14.png)

<Transformer attention>  
transformer attention은 입력 문장 안에서 단어 간의 관계성을 파악합니다.

이렇듯, 입력 시퀀스 내에서 자체 단어들 간의 관계성을 주목한다 하여 transformer attention 메커니즘을 Self-Attention이라고 부릅니다.

### 행렬곱 연산을 통해 Q, K, V 행렬 구하기

![image15.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image15.png)

input embedding vector + position embedding vector 했던 행렬을 세 개로 복사합니다.

복사한 세개의 행렬을 각각의 행렬(Q, K, V)를 구하기 위해 각기 다른 6x6행렬을 생성 후 행렬곱을 통해 Q, K, V행렬을 구해줍니다.

### Multi head attention의 Q, K의 행렬곱 구하기

![image16.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image16.png)

1. $Q*K^T$의 행렬곱 구하기

![image17.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image17.png)

2. 크기 변환 적용(예제에서의 $d_{model}$의 길이6 → $\sqrt{6}$만큼 나눠주기)

![image18.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image18.png)

3. mask layer는 encoder에서는 사용하지 않고, decoder에서만 사용하기에 생략.  
   softmax layer를 통해 행렬의 값을 확률로 변경

![image19.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image19.png)

- 이렇게 만들어진 3x3의 self attention 행렬은 각각의 단어들이 또 다른 각각의 단어들과 어떤 관계가 있는지 수치로 보여주는 행렬입니다.

4. input + position + attention embedding matrix 생성

![image20.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image20.png)

- softmax layer를 거친 Q, K행렬에 V행렬의 행렬곱 연산을 통해 self-attention이 가미된 (입력+위치+어텐션)임베딩 행렬을 만들어줍니다.

5. Multi head 구성 하기  
   논문에서는 8 개의 haed로 구성된 attention이며, 예시로 2개의 head attention

![image21.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image21.png)

- Q, K, V 단계에서부터 head의 숫자대로 나눠서 self-attention을 계산.  
- 최종 단계에서 다시 행렬들을 연결 concatenate해준 뒤

![image22.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image22.png)

- 완전 연결층. fully connected layer로 multi-head attention의 최종 output을 계산

## 4. Add & Norm

### 1. Add

![image23.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image23.png)

multi-head attention output matrix + 처음 생성한 input+position embedding을 더하는 과정.  
resnet에 도입되었던 skip-connection사용

- 학습과정에서의 기울기 소실 문제 완화
- 기존의 정보를 어느정도 보존하면서 새로운 정보 (어텐션) 가미 효과
- 학습에 좀더 효율적인 효과

### 2. Normalization

![image24.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image24.png)

각 열 별로 먼저 평균과 표준편차를 구하고, 정규화 Normalization 공식을 통해 각 열별로 정규화 진행

## 5. Feed Forward Layer

2개 층으로 이루어진 ReLU를 활성화 함수로 사용하는 단순한 신경구조망 사용했으나 꼭 2계층만 사용하는게아니라 그 이상 많은 층을 구성해도 무방합니다.

![image25.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image25.png)

1. normalization 공식을 통해 얻은 정규화 output을 feed forawrd layer 2개층에 적용함.  
2. 1계층에서 relu 적용해 음수값을 0값으로 만든 output을 2계층에 전달해서, 가중치와 편형과 연산을 통해 계산함. 2계층에서는 output에 relu미적용함.

## 6. 다시한번, Add & Norm적용 → encoder 단의 최종 output

![image26.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image26.png)

- 직전에 feed forward layer output matrix와 feed forward layer이전(1차 add & norm의 output)의 output matrix의 add 연산

![image27.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image27.png)

- normalization을 통해 행렬 정규화를 통해 transformer encoding 단의 최종 output

## 3. Decoder

## 1. 출력 단어 Encoding

![image28.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image28.png)

encoder와 마찬가지로 출력(단어)인코딩과 위치 인코딩 적용합니다. 이때 단어 인코딩과 위치 인코딩은 인코더 파트와 동일한 방식이며, position encoding은 기존에 계산한 값을 그대로 사용 할 수 있음

### 2. output embedding vector + position embedding vector.

![image29.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image29.png)

계산된 위치 임베딩과 출력 임베딩을 더해서 output embedding vector + position embedding vector를 구할 수 있습니다.

## 3. Mask Multi head attention

### 1. 복사한 세개의 행렬을 각각의 행렬(Q, K, V)를 구하기 위해 각기 다른 6x6 행렬과 행열곱 연산을 통해 Q, K, V 행렬 생성

### 2. $Q * K^T$ 행렬을 곱해서 attention matrix 생성.

### 3. 행렬의 크기 변화 Scale도 똑같이 $\sqrt{6}$으로 나눠줌.

### 4. mask attention

원래 transformer decoder의 목적은 출력단어 시퀀스를 생성하는 것입니다. 

![image30.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image30.png)

인코더 : 입력 문장 전체의 의미를 파악해야 하기 때문에 전체 단어들의 관계를 다 파악 해야할 필요가 있습니다.

![image31.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image31.png)

디코더 : 디코더의 경우 출력 문장을 한 단어씩 출력하는 것이 목적이기 때문에 아직 출력되지 않은 단어에 주의를 줄 수는 없는 것이 당연함. 

그래서, 트랜스포머의 디코더 학습 과정에서도 이러한 특성을 반영하여 특정 단어 기준으로 미래에 나오는 단어는 가려서 계산에 영향을 주지 않는 마스크 알고리즘을 사용합니다.

![image32.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image32.png)

< 마스크 알고리즘 >  
마스크 알고리즘을 위에서 attention 행렬에 적용합니다. 

- 주목 하지 말아야 할, 미래에 나와야 할 부분은 -inf를 씌워줍니다. -inf는 추후 softmax layer를 통해 0값으로 출력하기 위함입니다.

![image33.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image33.png)

### 5. Softmax

마스크 알고리즘을 적용한 attention 행렬값을 softmax layer의 input으로하여 연산.

![image34.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image34.png)

### 6. 행렬곱

마스크 행렬 연산의 softmax를 취한 행렬과 V 연산

![image35.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image35.png)

### 7. 행렬 연결 및 완결연결층

![image36.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image36.png)

- 필요 시 행렬 연결(concatenate)하고,  
- 6x6행렬로 fully connected 와 연산을 해주면, mask multi head attention의 최종 output 행렬값이 나옴.

## 4. Add & Norm

동일한 방식의 add & normailzation.

![image37.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image37.png)

## 5. decoder의 두 번째 multi head attention

인코더와 작동 방식이 똑같지만, 입력값만 조금의 차이를 가집니다.

![image38.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image38.png)

- input K, V : encoder의 최종 output 값 * 6x6행렬의 연산 값이 들어오며,  
- input Q : decoder의 mask multi head attention의 output값 * 6x6행렬의 연산 값이 들옵니다.

이후 행렬곱 ~ 크기변화 ~ 소프트맥스 ~ V와의 행렬곱 ~ 행렬 연결 ~ 완전 연결층(Fully Connected Layer)의 과정은 동일합니다.

## 6. Add & Norm ~ Feed Forward ~ Add & Norm

encoder의 add & norm ~ feed forward와 동일함

![image39.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image39.png)

![image40.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image40.png)

![image41.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image41.png)

## 7. 선형 계층 ~ 소프트맥스 ~ 최종 확률 출력

![image42.png](/assets/transformer/트랜스포머_이론_전체[with_신박AI_Deep_Learning_101]/image42.png)

1. 이전 decoder level에서 output행렬을 Input으로 받고,  
2. Vocabulary의 단어로 찾아야히기 때문에, Vocabulary 길이를 복원(11개 token → 6개의 $d_{model}$ → 11개의 token)  
3. Softmax를 통해 최종 출력값을 구하고  
4. 최종 정답인 0, 6, 3과 비교하여 cross entropy 등의 loss function과 backpropagation을 사용해 모든 layer의 weight값들을 조절해가는 것이 트랜스포머의 학습과정입니다.

---
강의 링크 

신박AI : https://www.youtube.com/watch?v=p216tTVxues&list=PLfGJDDf2OqlQkHqKB7uonQGeNRfUo_TMe&index=6