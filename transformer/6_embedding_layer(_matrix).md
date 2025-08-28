# 6. embedding layer(*matrix)

encoder의 input embedding에 대해서.

![스크린샷 2025-08-21 13.57.39.png](/assets/transformer/6_embedding_layer(_matrix)/image.png)

input embedding으로 들어가는 inputs은 Token index가 들어가게 됨

(참고 : Token index를 리턴하는 Tokenizer는 transformer와 별개로 독립적으로 학습하며 따로 새로운 챕터로 만들 수 있을 정도로 광범위 하지만, 매우 간단하게 설명하고 넘어갈 예정임)

token index를 리턴하는 tokenizer는 문장을 컴퓨터가 이해하기위해 쪼개주는 역할.

여러 학습 된 tokenizer model들을 선택 할 수 있으며, 각각의 tokenizer를 사용해서 token단위로 나눠지며, 각각의 token은 tokenizer model에서 학습이 완료된 output 숫자를 받게 됨.

tokenizer input : (i love you all) → 각각의 token 단위로 나눠 token output index : [40, 1842, 345, 477] (*각기 다른 tokenizer model의 token index number는 모두 다름)

---

![스크린샷 2025-08-21 14.37.10.png](/assets/transformer/6_embedding_layer(_matrix)/image_1.png)

Embedding Layer

Embedding layer를 사용하여 4개의 token index → size 20 embed_dim vector로 변경하는 역할을 하는데, 파이토치는 별도 layer인  ***torch.nn.Embedding*** class 존재함

torch.nn.Embedding class는 하나의 아주 큰 look-up table(matrix)이 가지는데, 현재 GPT2 Tokenizer를 사용하기에, 50만 개의 세로 사이즈와 우리가 사용하는 embeding dimension 20의  가로 사이즈를 가짐

                 ***Embedding Matrix = GPT2 Tokenizer * embedding dimension = (50k * 20)***

Embedding Matrix(layer)를 처음 만들면, 그 안의 값들은 랜덤하게 초기화 되어있음. 랜덤하게 초기화 되어있는 embedding layer는 neural network를 학습시키며 그 안의 값들도 같이 학습하게 됨

### Embedding layer의 동작 원리

![스크린샷 2025-08-21 14.52.03.png](/assets/transformer/6_embedding_layer(_matrix)/image_2.png)

“I love you all”은 GPT2 tokenizer를 통해 인덱스 넘버 [40, 1842, 345, 477]를 가지는데, embedding matrix를 포함한 neural net이 학습이 되었다면

neural net은 token number(embedding matrix)에서 40번째에 해당하는 vector를 뽑아서 초기 입력값 20 size embed_dim의 “I”에 해당하는 부분에 집어 넣고 transformer를 시작하게 됨

즉, ***embedding matrix는 Transformer input으로 들어가는 tensor를 만들어내는 matrix(layer)***라고 할 수 있음. 그 위치는 transformer의 encoder구조의 input embedding과 positional Encoding파트 중간임.