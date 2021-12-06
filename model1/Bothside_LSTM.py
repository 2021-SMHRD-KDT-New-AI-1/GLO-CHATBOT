import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import preprocessing
from sklearn.model_selection import train_test_split
import numpy as np


#학습파일 불러오기
def read_file(file_name):
    sents = []
    with open(file_name, 'r', encoding='utf-8')as f :
        lines = f.readline()
        for idx, l in enumerate(lines):
            if l[0] == ';' and lines[idx +1][0] =='$':
                tihs_sent=[]
            elif l[0] == '$' and lines[idx -1][0] ==';':
                continue
            elif l[0] == '\n':
                sents.append(tihs_sent)
            else:
                tihs_sent.append(tuple(l.split()))
    return sents
#학습용 말뭉치 데이처를 불러옴
corpus = read_file('dev_modified.txt')

#말뭉치 데이터에서 단어와 BIO태그만 불러와 학습용 데이터셋 생성
sentences, tags =[] , []
for t in corpus:
    tagged_sentence =[]
    sentence, bio_tag =[],[]
    for w in t:
        tagged_sentence.append((w[1],w[3]))
        sentence.append(w[1])
        bio_tag.append(w[3])
    sentences.append(sentence)
    tags.append(bio_tag)
print('샘플 크기 : \n',len(sentence))
print('0번째 샘플 문장 시퀀스 : \n', sentences[0])
print('0번째 샘플 bio태그 : \n', tags[0])
print('샘플 문장 시퀀스 최대 길이 :', max(len(l) for l in sentences))
print('샘플 문장 시퀀스 평균 길이 :', sum(map(len, sentences)/len(sentence)))

#토크나이저 정의
sent_tokenizer = preprocessing.text.Tokenizer(oov_token='OOV')
sent_tokenizer.fit_on_texts(sentences)
tag_toknizer= preprocessing.text.Tokenizer(lower=False)# 태그정보는 lower=False 소문자로 변환x
tag_toknizer.fit_on_texts(tags)

#단어 사전 및 태그 사전 크기
vocab_size = len(sent_tokenizer.word_index)+1
tag_size = len(tag_toknizer.word_index)+1
print('BIO 태그 사전 크기 :', tag_size)
print('단어 사전 크기 :', vocab_size)

