import pandas as pd

ner = pd.read_csv('ner_word.csv')

print("{} : {}".format(ner.iloc[:,1:2],ner.iloc[:,2:]))

