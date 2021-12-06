import pymysql
import openpyxl

from config1.DatabaseConfig import * # DB 접속 정보 불러오기

#학습데이터 초기화

def all_clear_train_data(db):
    #기존 학습 데이터 초기화
    sql = '''delete from glo_chatbotdata'''
    with db.cursor() as cursor:
        cursor.excute(sql)

    #auto increment 초기화
    sql = '''ALTER TABLE glo_chatbotdata AUTO_INCREMENT'''
    with db.cursor() as cursor:
        cursor.excute(sql)
