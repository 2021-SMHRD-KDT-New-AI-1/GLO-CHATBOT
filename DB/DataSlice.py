from konlpy.tag import Okt
from collections import Counter
import tsv,csv
import pandas as pd
#반복되는 단어 300개 추출하여 사전으로 만는 로직

f = open('copus_data_1.txt', 'r', encoding='utf-8')
data = f.read()

okt = Okt()
noun = okt.nouns(data)
for i,v in enumerate(noun):
    if len(v)<2:
        noun.pop(i)
count = Counter(noun)



noun_list = count.most_common(1000)
for v in noun_list:
    print(v[:3])


with open('user_dic.tsv','w',newline='',encoding='utf-8') as f :
    tsvw = csv.writer(f)
    for v in noun_list:
        tsvw.writerow(v)

