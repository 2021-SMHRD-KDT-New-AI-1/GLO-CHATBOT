import pickle

from konlpy.tag import Komoran

class Preprocess:
    def __init__(self,word2index_dic='', userdic=None):
        # 형태소 분석기 초기화
        if(word2index_dic != ''):
            f = open(word2index_dic, 'rb')
            self.word_index = pickle.load(f)
            f.close()
        else:
            self.word_index=None


        self.komoran = Komoran(userdic=userdic)

        # 제외할 품사
        # 관계언 , 기호, 어미, 접미사 제거
        self.exclusion_tags =[
            'JKS','JKC','JKG','JKO','JKV','JKQ',
            'JX','JC',
            'SF','SP','SS','SE','SO',
            'EP','EF','EC','ETN','ETM',
            'XSN','XSV','XSA'
        ]
    #형태소 분석기 POS 제거
    def pos(self,sentence):
         return self.komoran.pos(sentence)

     #불용어 제거 후 필요한 품사 정보만 가져오기
    def get_keywords(self, pos ,without_tag=False):
        f = lambda x : x in self.exclusion_tags
        word_list=[]
        for p in pos:
            if f(p[1]) is False:
                word_list.append(p if without_tag is False else p[0])
        return word_list


    def get_wordidx_sequence(self, keywords):
        if self.word_index is None:
            return []
        w2i = []

        for word in keywords:
            try:
                w2i.append(self.word_index[word])
            except KeyError:
                #해당 언어가 없는 경우 'OOV'로 처리
                w2i.append(self.word_index['OOV'])
        return  w2i
