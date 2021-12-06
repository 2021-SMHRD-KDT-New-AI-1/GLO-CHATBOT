from utils.Preprocess import Preprocess
import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from model.intent.IntentModel import IntentModel
from tensorflow.keras import preprocessing

intent_labels = {0:'기쁨',1:'당황',2:'분노',3:'불안',4:'상처',5:'슬픔',6:'우울',7:'인사' }
#객제 생성(사전, 학습 데이터 불러오기)

p = Preprocess(word2index_dic='../../dict/chatbot_dict.bin',userdic='../../utils/user_dic.tsv')
model = load_model('intent_model_emo.h5')
#의도 분류 모델 정의
intent = IntentModel(model_name='intent_model_emo.h5',proprocess=p)


query = input('>> 의도 입력')
pos = p.pos(query)
keywords = p.get_keywords(pos, without_tag=True)
seq = p.get_wordidx_sequence(keywords)
sequences = [seq]

# 단어 시퀀스 벡터 크기
from config1.GlobalParams import MAX_SEQ_LEN
padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')

predict = model.predict(padded_seqs)
predict_class = tf.math.argmax(predict, axis=1)
print(query)
print("의도 예측 점수 : ", predict)
print("의도 예측 클래스 : ", predict_class.numpy())
print("의도  : ", intent_labels[predict_class.numpy()[0]])
