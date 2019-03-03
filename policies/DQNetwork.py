from keras.models import Sequential
from keras.layers import *
import keras

class DQNetwork():
    def __init__(self, input_shape, alpha, gamma,
                 dropout_rate, num_actions, batch_size, learning_rate, feature_num):
        self.alpha = alpha
        self.gamma = gamma
        self.dropout_rate = dropout_rate
        self.input_shape = input_shape
        self.feature_num = feature_num
        self.num_actions = num_actions
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.act2idx = {'L': 0, 'R': 1, 'F': 2}

        self.model = Sequential()
        self.model.add(Dense(64, activation='relu', input_shape=self.input_shape))
        self.model.add(Dropout(dropout_rate))
        self.model.add(Dense(1))
        adam = keras.optimizers.Adam(lr=self.learning_rate, beta_1=0.9, beta_2=0.999, epsilon=1e-8)
        self.model.compile(loss='mean_squared_error', optimizer=adam)

    def learn(self, batches):
        bs_int = int(self.batch_size)
        x = np.zeros([bs_int, self.feature_num])
        y = np.zeros(bs_int)
        for idx, batch in enumerate(batches):
            x[idx] = batch['s_t']
            q_hat = (batch['r_t'] + self.gamma * np.max(self.model.predict(batch['s_tp1']))) # here need to do loop as well, which one of the 3 actions gives best q-value.
            y[idx] = q_hat

        h = self.model.fit(x, y, batch_size=bs_int, epochs=1, verbose=0)
        return h.history['loss'][0]
