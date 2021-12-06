from config1.DatabaseConfig import *
from utils.DataBase import Database
from utils.Preprocess import Preprocess
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#전처리 객체 생성
p = Preprocess(word2index_dic='../dict/chatbot_dict.bin',userdic='../utils/user_dic.tsv')

#질문/답변 학습 디비 연결 객체 생성
db = Database(
    #host=DB_HOST, user=DB_USER, password=DB_PASSWORD, port=DB_PORT,db_name=DB_NAME
    host='project-db-stu.ddns.net',
    user='campus_g_a_1125',
    password='123456',
    port=3307 ,
    db_name='campus_g_a_1125'
)
db.connect()# 디비 연결

#원문
query = '모든 게 끝난 느낌이야. 투자했던 주식이 폭락했어.'

#의도 파악
from model.intent.IntentModel import IntentModel
intent = IntentModel(model_name='../model/intent/intent_model.h5',proprocess=p)
predict = intent.predict_class(query)
intent_name = intent.labels[predict]

#감정태그 인식
from model.intent.IntentModel_emo import IntentModel_emo
intent_emo = IntentModel_emo(model_name='../model/intent/intent_model_emo.h5',proprocess=p)
predict_emo = intent_emo.predict_class(query)
intent_emo_name = intent_emo.labels_emo[predict_emo]

print('질문 :', query)
print('='*40)
print('의도 파악 : ', intent_name)
print('감정명 인식 : ', predict_emo)
print('답변 검색에 필요한 감정 태그 : ', intent_emo_name)
print('='*40)

#답변검색
from utils.FindAnswer import FindAnswer

try:
    f = FindAnswer(db)

    answer = f.search(intent_name, intent_emo_name)
    print('DB 연결 성공')
except:

    answer = '무슨말인지 모르겠어요 다시 이야기 해주세요!'

print('답변 : ', answer)

db.close() #디비연결 끊기
