import ai
import snake
import numpy as np
import matplotlib.pyplot as plt
import os

WIDTH = 7
HEIGHT = 7
WALLS_NUMBER = 4
REWARDS = (25, 16, 9)
ACTION_SIZE = 4
STATE_SIZE = (2 * WIDTH + 1, 2 * HEIGHT + 1, 3)
MODEL_FILE = 'model.h5'
EPISODES = 2000
STEPS = 250


def play_human(speed):
    game = snake.Game(WIDTH, HEIGHT, WALLS_NUMBER, REWARDS)
    game.play_new_game(speed)


def train():
    game = snake.Game(WIDTH, HEIGHT, WALLS_NUMBER, REWARDS)
    model = ai.Model(STATE_SIZE, ACTION_SIZE)
    if os.path.isfile(MODEL_FILE):
        model.load(MODEL_FILE)

    for e in range(EPISODES):
        game.reset()
        tot_reward = 0
        for step in range(STEPS):
            state = game.state()
            previous_score = game.score
            action = model.act(state)
            alive = game.move(action)
            next_state = None
            reward = game.score - previous_score
            tot_reward += reward
            if alive:
                next_state = game.state()
            else:
                reward -= 100
            model.remember((state, action, reward, next_state))
        model.replay()
        print('Episode {}: score {}'.format(e + 1, game.score))

        if e % 200 == 199:
            scores = np.zeros(100)
            for i in range(100):
                game.reset()
                step = 0
                while step < STEPS:
                    if not game.move(model.act_best(game.state())):
                        break
                    step += 1
                scores[i] = game.score
            print('Episode {} of {}'.format(e + 1, EPISODES))
            print('Average/ Min / Max score on a new game: {} / {} / {}'.format(np.mean(scores), np.min(scores), np.max(scores)))
            model.save(MODEL_FILE)


def benchmark():
    game = snake.Game(WIDTH, HEIGHT, WALLS_NUMBER, REWARDS)
    model = ai.Model(STATE_SIZE, ACTION_SIZE)
    model.load(MODEL_FILE)
    scores = np.zeros(500)
    for i in range(500):
        game.reset()
        step = 0
        while step < STEPS:
            if not game.move(model.act_best(game.state())):
                break
            step += 1
        scores[i] = game.score

    print('Average/ Min / Max score on a new game: {} / {} / {}'.format(np.mean(scores), np.min(scores),
                                                                        np.max(scores)))
    plt.hist(scores)
    plt.show()


def play_ai():
    game = snake.Game(WIDTH, HEIGHT, WALLS_NUMBER, REWARDS)
    model = ai.Model(STATE_SIZE, ACTION_SIZE)
    model.load(MODEL_FILE)
    game.play_new_game(5, model.act_best)


#play_human(20)
#benchmark()
#train()
benchmark()
#play_ai()
