from utils.Preprocess import Preprocess

sent ='나 지금 너무 우울해 너는 어때?'


#전처리 객체 생성
p = Preprocess(userdic='../utils/user_dic.tsv')

#형태소 분석기 실행
pos = p.pos(sent)

#품사 태그와 같이 키워드 출력
ret = p.get_keyword(pos,without_tag=False)
print(ret)

#품사태그 없이 키워드 출력
ret = p.get_keyword(pos, without_tag=True)
print(ret)
