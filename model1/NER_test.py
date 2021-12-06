from utils.Preprocess import Preprocess
from model1.NerModel import NerModel

p = Preprocess(word2index_dic='../dict/chatbot_dict.bin',userdic='../utils/user_dic.tsv')

ner = NerModel(model_name='Ner_model.h5', proprocess=p)

query = '걱정이야. 이러다가는 평생 연애만 하고 결혼은 못 할 거 같아.'

predicts = ner.predict(query)
print(predicts)
