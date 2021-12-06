import csv
from konlpy.tag import Komoran
from random import  *

date_file = 'date.csv'
word_file = 'ner_word.csv'
sent_file = '주문조합.csv'

komoran = Komoran(userdic='../utils/user_dic.tsv')

file = open("corpus.txt", 'w',encoding='cp949')
with open(date_file, mode='r', encoding='utf-8') as df:
    dr = csv.reader(df)
    for k, r in enumerate(dr):

        word_sel = randint(1, 243)
        with open(word_file, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)

            for i, row in enumerate(reader):
                if i != word_sel: continue

                sel = randint(1, 155)
                with open(sent_file, mode="r", encoding="utf-8") as qf:
                    qreader = csv.reader(qf)
                    for qi, qrow in enumerate(qreader):
                        if(qi != sel): continue

                        sentence = []
                        tmp = r[0].split(' ')
                        for t in tmp:
                            date = t.split(':')
                            sentence.append(tuple(date))

                        word = row[0].split(':')
                        sentence.append(tuple(word))

                        q = qrow[0]
                        q = q.replace('\ufeff', '')
                        pos = komoran.pos(q)
                        for p in pos:
                            x = (p[0], 'O', p[1])
                            sentence.append(x)
                        break

                    # 파일 저장
                    raw_q = ";"
                    res_q = '$'
                    line = ""
                    for i, s in enumerate(sentence):
                        raw_q += "{} ".format(s[0])
                        res_q += "{} ".format(s[0])
                        if s[1] == 'B_DT':
                            line += "{}\t{}\t{}\t{}\n".format(i + 1, s[0],'NNG', 'B_WORD')
                        elif s[1] == 'B_WORD':
                            line += "{}\t{}\t{}\t{}\n".format(i + 1, s[0], 'NNG', 'B_WORD')
                        elif s[1] == 'NNG':
                            line += "{}\t{}\t{}\t{}\n".format(i + 1, s[0], 'NNG', 'B_WORD')
                        #elif s[1] == 'B_WORD':
                        else:
                            line += "{}\t{}\t{}\t{}\n".format(i + 1, s[0], s[2], 'O')

                    print(raw_q)
                    print(res_q)
                    print(line)
                    file.write(raw_q + "\n")
                    file.write(res_q + "\n")
                    file.write(line + "\n")

file.close()
