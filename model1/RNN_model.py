import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense, LSTM, SimpleRNN
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#time step 만큼 시퀀스 데이터 분리

def split_sequence(sequence , step):
    x,y = list(), list()

    for i in range(len(sequence)):
        end_idx = i +step

        if end_idx > len(sequence) -1 :
            break
        seq_x, seq_y = sequence[i:end_idx], sequence[end_idx]
        x.append(seq_x)
        y.append(seq_y)

    return np.array(x),np.array(y)
#sin 함수 학습 데이터
x = [i for i in np.arange(-5,5,0.1)]
y_trian = [np.sin(i) for i in x]

#하이퍼 파라미터
n_timesteps = 15
n_features = 1

#시퀀스 나누기
X_train , y_train = split_sequence(y_trian, step=n_timesteps)
print('shape x:{} / y:{}'.format(X_train.shape,y_train.shape))

#RNN입력 벡터 크기를 맞추기 위해 벡터 차원 크기 변경
# reshape from [samples, timesteps] into [samples, timesteps, features]
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], n_features)
print('X_train.shape = {}'.format(X_train.shape))
print('y_train.shape = {}'.format(y_train.shape))

#RNN  모델 정의
model = Sequential()

model.add(SimpleRNN(units=10, return_sequences=False, input_shape=(n_timesteps, n_features)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

#모델 학습
np.random.seed(0)
from tensorflow.keras.callbacks import EarlyStopping
early_stopping = EarlyStopping(monitor='loss',patience=5,mode='auto')
history = model.fit(X_train,y_train, epochs=1000, callbacks=[early_stopping])

#loss 그래프 생성
plt.plot(history.history['loss'],label='loss')
plt.legend(loc='upper right')
plt.show()

#테스트 데이터셋 생성
X_test = np.arange(1,10,0.1)
calc_y = np.cos(X_test)

#RNN 모델 예측및 로그 저장
y_test = calc_y[:n_timesteps]
for i in range(len(X_test)- n_timesteps):
    net_input = y_test[i : i + n_timesteps]
    net_input = net_input.reshape((1, n_timesteps, n_features))
    y_train = model.predict(net_input, verbose=0)
    print(y_test.shape, y_train.shape, i ,i+n_timesteps)
    y_test = np.append(y_test,y_train)

#예측 결과 그래프 그리기
plt.plot(X_test, calc_y, label='ground truth', color='orange')
plt.plot(X_test, y_test, label='predictions', color='blue')

plt.legend(loc='upper left')
plt.ylim(-2,2)
plt.show()
