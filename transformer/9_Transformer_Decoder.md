# 9. Transformer Decoder

![스크린샷 2025-08-22 16.54.56.png](/assets/transformer/9_Transformer_Decoder/image.png)

각각의 문장을 RNN Model에 넣어서 postive, negative의 classification 목적으로 사용 할 수 있고, 생성형 모델 목적으로 사용 할 수 있습니다.

![스크린샷 2025-08-22 17.37.38.png](/assets/transformer/9_Transformer_Decoder/image_1.png)

input : <'S'> → output : I

![스크린샷 2025-08-22 17.38.10.png](/assets/transformer/9_Transformer_Decoder/image_2.png)

input : I → input : Love

생성형으로 만들기 위해서는 각각의 단어 token을 input으로 넣어주면, input의 다음 단어 token을 output으로 받을 수 있습니다. 초기에는 시작을 알리는 <'S'>를 input으로 넣어주면 최종적으로 I Love you All의 결과를 생성 할 수 있습니다.

![스크린샷 2025-08-22 17.41.22.png](/assets/transformer/9_Transformer_Decoder/image_3.png)

self attention은 각 token들을 서로 참조하고, 업데이트하면서 문장의 context를 이해합니다.

### attention을 생성형으로 만드는 decoder의 핵심 구조.

self attention을 간단히 구조화했고, input으로 들어온 token별 vector로 부터 query, key, value를 계산하고, 그 중 query와 key 간의 score를 통해 value vactor를 업데이트 하는 방식으로 구성합니다.

attention은 모든 단어들의 문맥을 파악해 자연어를 처리하기에 생성형 모델로 바로 적용하기에는 무리가 있습니다.

![스크린샷 2025-08-22 18.00.34.png](/assets/transformer/9_Transformer_Decoder/image_4.png)

생성형 트랜스포머는 여태까지 주어진 서로간의 정보의 문맥을 바탕으로 다음 토큰에 대해서 예측해야합니다.

다시말해, input으로 I vector만 주어졌을때, neural network는 다음에 들어오는 토큰을 예상할 수 없습니다. 

![스크린샷 2025-08-22 18.02.06.png](/assets/transformer/9_Transformer_Decoder/image_5.png)

이를 score matrix에서 표현하였는데, “I”만 주어지게 되면 score matrix에서의 I*I에 해당하는 1 값만 가질 수 있습니다.(1개의 input token이라서 1(전체))

![스크린샷 2025-08-22 18.22.28.png](/assets/transformer/9_Transformer_Decoder/image_6.png)

만약 input token이 2개라고 한다면, query, key에서도 두 가지만 보이게 되며, socre에서도 두 가지 스코어값만 가지게 됩니다.

![스크린샷 2025-08-22 18.23.50.png](/assets/transformer/9_Transformer_Decoder/image_7.png)

즉, input token에 따라서 score matrix도 선정이 되며, token들이 서로 커뮤니케이션하면서 다음 단어를 예측하기 위한 feature를 뽑아내어 학습을 할 수 있습니다. 이는 attention을 생성형으로 만드는 decoder의 핵심 구조입니다.

### 정리

![스크린샷 2025-08-22 18.38.10.png](/assets/transformer/9_Transformer_Decoder/image_8.png)

- input token이 “I” 하나라면, output으로 love가 나오도록 학습을 시키게 됩니다.
- input token이 “I Love you All”이라고 한다면, 마침표(.)가 될 수 있도록 neural network를 학습시키는 것입니다.

neural network가 training step이라면 decoder attention에 대한 최종 output이 모든 token에 대한 score로 나올 것이고 score와 각각의 output token에 대한 ground truth와 비교하며, loss의 최소화를 위해 backpropagation하여 weight를 업데이트를 하며 학습합니다.

학습이 된 모델 실행

![스크린샷 2025-08-22 18.42.38.png](/assets/transformer/9_Transformer_Decoder/image_9.png)

- 맨 처음 iter.  : 처음 I에 대해서 모델에 input으로 하여 q, k, v값을 계산 → 그렇게 만들어진 score matrix는 하나의 값이 나옴. —> I의 value vector인 love로 다음 step input으로 넣어서 lter.
- 1번째 iter의 결과로 I Love의 문장을 생성

![스크린샷 2025-08-22 18.44.28.png](/assets/transformer/9_Transformer_Decoder/image_10.png)

- 2번째 iter의 결과로 i love you의 문장을 생성해냄.

![스크린샷 2025-08-22 18.46.56.png](/assets/transformer/9_Transformer_Decoder/image_11.png)

- 마지막 iter의 결과로 I Love you. (마침표로 문장 생성 완료)