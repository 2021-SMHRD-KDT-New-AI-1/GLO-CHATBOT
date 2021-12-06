class FindAnswer:
    def __init__(self, db):
        self.db = db

    #검색 쿼리 생성
    def _make_query(self, intent_name, intent_emo_name):
        sql = "select answers from glo_chatbotdata where situations='{}' and emotions='{}' order by rand() limit 1" .format(intent_name,intent_emo_name)
        print(sql)

        return sql

    #답변 검색
    def search(self, intent_name, intent_emo_name):
        #의도명과 개체명으로 답변 검색
        print(intent_name, intent_emo_name)
        sql = "select answers from glo_chatbotdata where situations='{}' and emotions='{}' order by rand() limit 1" .format(intent_name,intent_emo_name)
        answer = self.db.select_one(sql)
        print(sql)
        #검색되는 답변이 없으면 의도명만 검색
       # if answer is None:
         #   sql = self._make_query(intent_name, intent_emo_name)
        #    answer=self.db.select_one(sql)

        return answer['answers']
