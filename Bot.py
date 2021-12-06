import threading
import json

from config1.DatabaseConfig import *
from utils.DataBase import Database
from utils.BotsServer import BotServer
from model.intent.IntentModel import IntentModel
from utils.Preprocess import Preprocess
from model1.NerModel import NerModel
from utils.FindAnswer import FindAnswer




#전처리 객체 생성
p = Preprocess(word2index_dic='dict/chatbot_dict.bin',userdic='utils/user_dic.tsv')

#의도파악 모델
intent = IntentModel(model_name='model/intent/intent_model.h5',proprocess=p)

#개체명 인식 모델
ner = NerModel(model_name='model1/ner_model.h5', proprocess= p)


def to_client(conn, addr, params):
    db=params['db']
    try:
        db.connect()

        #데이터 수신
        read= conn.recv(2048) #수신 데이터가 있을 때 까지 블로킹
        print('====================')
        print('Connection from : &s' % str(addr))

        if read is None or not read:
            #클라이언트 연결이 끊어지거나 오류가 있는 경우
            print('클라이언트 연결 끊어짐')
            exit(0)
            #json 데이터로 변환
            recv_json_data = json.load(read.decode())
            print('데이터 수신 : ',recv_json_data)
            query = recv_json_data['questions']

            #의도파악
            intent_predict = intent.predict_class(query)
            intent_name = intent.labels[intent_predict]

            #개체명 파악
            ner_predict =ner.predict(query)
            ner_tag = ner.predict_tags(query)

            #답변검색
            try:
                f = FindAnswer(db)
                answer_text = f.search(intent_name)
                answer = f.tag_to_word(ner_predict, answer_text)

            except:
                answer ='죄송해요, 무슨 말 인지 모르겠어요. 조금 더 공부할게요.'

            send_json_data_str ={
                'questions': query,
                'answers' : answer,
                'intents' : intent_name,
                'ner' : str(ner_predict)

            }
            message = json.dumps(send_json_data_str) # json 객체를 전송가능한 문자열로 변환
            conn.send(message.encode())

    except Exception as ex:
        print(ex)

    finally:
        if db is not None:
            db.close()
        conn.close()

if __name__ == '__main__':
    #질문/답변 학습 db연결 객체 생성
    db = Database(
        host='project-db-stu.ddns.net',
        user='campus_g_a_1125',
        password='123456',
        port=3307 ,
        db_name='campus_g_a_1125'
    )
    print('DB 접속')
    print(DB_PORT)
    print(DB_PASSWORD)

    #봇 서버 동작
    port = 5050
    listen = 100
    bot = BotServer(port, listen)
    bot.create_sock()
    print('bot start')

    while True:
        conn, addr = bot.ready_for_client()
        params = {
            'db':db
        }
        client = threading.Thread(target=to_client, args=(
            conn,
            addr,
            params
        ))
        client.start()
