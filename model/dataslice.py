import pandas as pd

data1 = pd.read_csv('total_train_data.csv')

data1 = data1['query']

print(data1)
