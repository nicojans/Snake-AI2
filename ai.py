import tensorflow as tf
import numpy as np
import random

GAMMA = 0.99
EPSILON_MIN = 0.05
EPSILON_DECAY = 0.995


class Memory:
    def __init__(self, max_memory):
        self._max_memory = max_memory
        self._samples = []

    def append(self, sample):
        self._samples.append(sample)
        if len(self._samples) > self._max_memory:
            self._samples.pop(0)

    def sample(self, no_samples):
        if no_samples > len(self._samples):
            return random.sample(self._samples, len(self._samples))
        else:
            return random.sample(self._samples, no_samples)


class Model:
    def __init__(self, state_size, action_size):
        self._state_size = state_size
        self._action_size = action_size
        self._memory = Memory(200000)
        self._epsilon = 1
        self._model = self._build_model()

    def _build_model(self):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(16, (3, 3), input_shape=self._state_size, activation=tf.nn.relu),
            tf.keras.layers.Conv2D(32, (3, 3), activation=tf.nn.relu),
            tf.keras.layers.Conv2D(32, (3, 3), activation=tf.nn.relu),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(32, activation=tf.nn.relu),
            tf.keras.layers.Dense(self._action_size)
        ])
        model.compile(optimizer=tf.train.AdamOptimizer(), loss='mse', metrics=['accuracy'])
        return model

    def act(self, state):
        if np.random.rand() <= self._epsilon:
            return random.randrange(self._action_size)
        return self.act_best(state)

    def act_best(self, state):
        return np.argmax(self._model.predict(state.reshape((1,) + self._state_size)))

    def remember(self, sample):
        self._memory.append(sample)

    def replay(self):
        batch = self._memory.sample(1000)
        states = np.array([val[0] for val in batch])
        next_states = np.array([(np.zeros(self._state_size) if val[3] is None else val[3]) for val in batch])
        predict_states = self._model.predict(states)
        predict_next_states = self._model.predict(next_states)
        targets = np.zeros((len(batch), self._action_size))

        for i, b in enumerate(batch):
            action, reward, next_state = b[1], b[2], b[3]
            targets[i] = predict_states[i]
            target = reward
            if next_state is not None:
                target += GAMMA * np.amax(predict_next_states[i])
            targets[i][action] = target

        self._model.fit(states, targets, verbose=0)

        if self._epsilon > EPSILON_MIN:
            self._epsilon *= EPSILON_DECAY

    def save(self, file_name):
        self._model.save_weights(file_name)

    def load(self, file_name):
        self._model.load_weights(file_name)
