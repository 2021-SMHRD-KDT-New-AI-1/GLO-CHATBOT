import pandas as pd

data=pd.read_csv('user_dic.tsv', header=None)


data[1] = 'NNG'
data.to_csv('user_dic.tsv', mode='w',header=False,index=False)
