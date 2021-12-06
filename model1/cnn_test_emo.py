import tensorflow as tf
import pandas as pd
from tensorflow.keras.models import Model, load_model
from tensorflow.keras import preprocessing

#데이터 읽어 오기
train_file = 'emo.csv'
data = pd.read_csv(train_file, delimiter=',')
featuers = data['questions'].tolist()
labels = data['emo'].tolist()


#단어 인덱스 시퀀스 벡터
corpus = [preprocessing.text.text_to_word_sequence(text) for text in featuers]
tokenizer = preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(corpus)
sequences = tokenizer.texts_to_sequences(corpus)


MAX_SEQ_LEN = 20 #단어 시퀀스 벡터 크기
padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN,padding='post')

#테스트용 데이터셋 생성
ds = tf.data.Dataset.from_tensor_slices((padded_seqs, labels))
ds = ds.shuffle(len(featuers))
test_ds = ds.take(2000).batch(20)

#감정분류 CNN 모델 불러오기
model = load_model('cnn_model_emo.h5')
model.summary()
model.evaluate(test_ds, verbose=2)


#테스트용 데이터셋의 10212번째 데이터 출력
print('단어 시퀀스 : ',corpus[1230])
print('문장 : ', corpus[1230])
print('단어 인덱스 시퀀스 : ', padded_seqs[1230])
print('문장 분류(정답) : ', labels[1230])

#테스트용 데이터셋의 10212번째 데이터 감정 예측
picks = [1230]
predict = model.predict(padded_seqs[picks])
predict_class = tf.math.argmax(predict, axis=1)
print('감정 예측 점수 : ', predict)
print('감정 예측 클래스 : ', predict_class.numpy())
