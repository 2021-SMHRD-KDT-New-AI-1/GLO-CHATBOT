from flask import Flask, request,jsonify, abort
import socket
import json

#챗봇 엔진 서버 접속 정보
host = '127.0.0.1'
port = 5050

#Flask 애플리케이션
app = Flask(__name__)

#챗봇 엔진 서버와 통신
def get_answer_from_engine(query):
    #챗봇 엔진 서버 연결
    mySocket = socket.socket()
    mySocket.connect((host,port))

    #챗봇 엔진 질의 요청
    data = query

    mySocket.send(data.encode())

    data_answer = mySocket.recv(2048).decode()

    mySocket.close()
    print(data_answer)
    return data_answer
#챗봇 엔진 query 전송 API

@app.route('/query/<bot_type>', methods=['GET'])
def query(bot_type):

    #body = request.get_json()
    body = request.args
    print(body)

    try:
        if bot_type == 'TEST':
            #챗봇 API 테스트
            ret = get_answer_from_engine(query=body['query'])
            print(ret)
            return ret
        elif bot_type == 'KAKAO':
            pass
        elif bot_type == 'NAVER':
            pass
        else :
            #정의 되지 않은 bot type인 경우 404 에러
            abort(404)
    except Exception as ex:
        #오류 발생시 500
        print(ex)
        abort(500)

if __name__ == '__main__':
    app.run()
