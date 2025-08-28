# 8. Transformer Encoder

![스크린샷 2025-08-22 14.29.02.png](/assets/transformer/8_Transformer_Encoder/image.png)

배운내용

1. RNN의 동작 원리
2. 정보를 추출하는 encoder
3.  생성 기능이 있는 decoder

![스크린샷 2025-08-22 14.33.05.png](/assets/transformer/8_Transformer_Encoder/image_1.png)

번역기능이 중점인 페이퍼

1. 입력된 토큰 → input embedding → positional encoding를 통해 input tensor를 만들고
2. self attention → multi head attention → feed forward가 있는 encoder block을 반복하고 
3. dimension을 줄여주는 Pooling layer → CrossEntropy와 같은 loss 함수를 정의하면
4. loss 값을 최소화 하는 backpropagation을 통해 Neural Net을 학습시킬 수 있음 

이러한 encoder로 만들수 있는 가장 대표적인 text classification 이며 이러한 구조를 효과적으로 이해할 수 있는 방법은 input으로 부터 loss값 까지 전체 tensor의 dimension을 아는 것임.

![스크린샷 2025-08-22 14.43.41.png](/assets/transformer/8_Transformer_Encoder/image_2.png)

Embedding Matrix : 문장을 tokenizer를 통해 토큰 인덱스를 받아 embedding vector로 변환 

Position Matrix(seq_len, embed_dim) : attention의 구조는 token의 순서를 구분 할 수 없기 때문에 모델이 순서를 구분할 수 있도록 위치정보 Position matrix를 만듬

![스크린샷 2025-08-22 14.52.22.png](/assets/transformer/8_Transformer_Encoder/image_3.png)

embedding matrix, position matrix 정보를 더 해 만들어진 input tensor는 batch size가 1이라는 가정하에 

1. **Embedding & Position Encoding**
    - Embedding matrix와 Position matrix를 더해 input tensor 생성
    - (가정) batch size = 1 → 세로: token, 가로: 임베딩 벡터
2. **Layer Normalization**
    - 입력 텐서를 정규화하여 안정적인 학습을 유도
3. **Self-Attention(Q, K, V 계산)**
    - Query(Q), Key(K), Value(V) 매커니즘을 통해 Attention score 계산
4. **Contextual Representation 업데이트**
    - 각 token이 문맥(Context)에 맞게 벡터를 업데이트
5. **Skip Connection (Residual Connection)**
    - 업데이트된 벡터와 기존 텐서를 더함
6. **Feed Forward Block + Activation**
    - Fully Connected Layer와 활성화 함수를 통과시켜 특징 변환
7. **Skip Connection**
    - Feed Forward 결과와 입력을 다시 더함
8. **Encoder Block 반복**
    - 위 구조(3~7번)를 N번 반복
9. **Pooling Layer**
    - 시퀀스 차원을 줄여 분류 등에 적합한 형태로 변환
10. **Loss Function 적용**
    - Cross Entropy 등 손실 함수를 적용해 학습

각 단계별 shape 변화 흐름

```python
1. Input token index → (batch, seq_len)
2. Embedding layer → (batch, seq_len, embed_dim)
3. + Position encoding → (batch, seq_len, embed_dim)
4. Q, K, V 생성 → (batch, seq_len, atten_dim)
5. Attention score 계산 → (batch, seq_len, seq_len)
6. Attention 적용 후 → (batch, seq_len, atten_dim)
7. Feed Forward → (batch, seq_len, embed_dim)

```