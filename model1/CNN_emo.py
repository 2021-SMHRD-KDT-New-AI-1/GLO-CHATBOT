import pandas as pd
import tensorflow as tf
from tensorflow.keras import preprocessing
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dense,Dropout,Conv1D,GlobalMaxPool1D,concatenate

#데이터 읽기
train_file = 'emo.csv'
data = pd.read_csv(train_file, delimiter=',')
features = data['questions'].tolist()
labels = data['emo'].tolist()

#단어 인덱스 시퀀스 벡터
corpus = [preprocessing.text.text_to_word_sequence(text) for text in features]
tokenizer = preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(corpus)
sequences = tokenizer.texts_to_sequences(corpus)
word_index = tokenizer.word_index

MAX_SEQ_LEN = 20 #단어 시퀀스 크기
padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN)


#학습용, 검증용, 테스트용 데이터셋 생성
#학습셋:검증셋:테스트셋 = 7:2:1
ds = tf.data.Dataset.from_tensor_slices((padded_seqs,labels))
ds = ds.shuffle(len(features))

train_size = int(len(padded_seqs)*0.7)
val_size = int(len(padded_seqs)*0.2)
test_size = int(len(padded_seqs)*0.1)

train_ds = ds.take(train_size).batch(20)
val_ds = ds.skip(train_size).take(val_size).batch(20)
test_ds = ds.skip(train_size+val_size).take(test_size).batch(20)


#하이퍼 파라미터 설정
dropout_prob = 0.5
EMB_SIZE =128
EPOCH = 5
VOCAB_SIZE = len(word_index)+1

#CNN 모델 정의
input_layer = Input(shape=(MAX_SEQ_LEN))
embedding_layer = Embedding(VOCAB_SIZE, EMB_SIZE, input_length=MAX_SEQ_LEN)(input_layer)
dropout_emb = Dropout(rate=dropout_prob)(embedding_layer)

conv1 = Conv1D(filters=128,
               kernel_size=3,
               padding='valid',
               activation=tf.nn.relu)(dropout_emb)
pool1 = GlobalMaxPool1D()(conv1)


conv2 = Conv1D(filters=128,
               kernel_size=4,
               padding='valid',
               activation=tf.nn.relu)(dropout_emb)
pool2 = GlobalMaxPool1D()(conv2)

conv3 = Conv1D(filters=128,
               kernel_size=5,
               padding='valid',
               activation=tf.nn.relu)(dropout_emb)
pool3 = GlobalMaxPool1D()(conv3)


#3,4,5-gram 이후 합치기
concat = concatenate([pool1,pool2,pool3])

hidden = Dense(128,activation=tf.nn.relu)(concat)
dropout_hidden = Dropout(rate=dropout_prob)(hidden)
logits = Dense(8, name='logits')(dropout_hidden)
predictions = Dense(8, activation=tf.nn.softmax)(logits)

#모델생성
model = Model(inputs=input_layer, outputs=predictions)
model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss='sparse_categorical_crossentropy',
              metrics=[tf.keras.metrics.SparseCategoricalAccuracy()])


#모델 학습
model.fit(train_ds, validation_data=val_ds,epochs=EPOCH, verbose=1)
#verbose는 학습의 진행 상황을 보여줄 것인지 지정을 하는데 verbose를 1로 세팅하면 학습이 되는 모습을 볼 수 있다.


#모델평가(테스트 데이터셋 이용)
loss, accuracy = model.evaluate(test_ds, verbose=1)
print('Accuracy : %f' %(accuracy*100))
print('loss : %f' %(loss))

#모델저장
model.save('cnn_model_emo.h5')

