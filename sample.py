import ai
import snake
import numpy as np

WIDTH = 7
HEIGHT = 7
WALLS_NUMBER = 0
REWARDS = (1,)
ACTION_SIZE = 4
STATE_SIZE = (WIDTH, HEIGHT, 3)


def play_human(speed):
    game = snake.Game(WIDTH, HEIGHT, WALLS_NUMBER, REWARDS)
    game.play_new_game(speed)


def train():
    episodes = 1000
    steps = 500
    game = snake.Game(WIDTH, HEIGHT, WALLS_NUMBER, REWARDS)
    model = ai.Model(STATE_SIZE, ACTION_SIZE)
    model.load('model_conv.h5')

    for e in range(episodes):
        game.reset()
        tot_reward = 0
        for step in range(steps):
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
                reward -= 1
            model.remember((state, action, reward, next_state))
        model.replay()
        print('Episode {}: score {}'.format(e + 1, game.score))

        if e % 100 == 99:
            scores = np.zeros(50)
            for i in range(50):
                game.reset()
                step = 0
                while step < steps:
                    if not game.move(model.act_best(game.state())):
                        break
                    step += 1
                scores[i] = game.score
            print('Average/ Min / Max score on a new game: {} / {} / {}'.format(np.mean(scores), np.min(scores), np.max(scores)))

    model.save('model_conv.h5')


def play_ai():
    game = snake.Game(WIDTH, HEIGHT, WALLS_NUMBER, REWARDS)
    model = ai.Model(STATE_SIZE, ACTION_SIZE)
    model.load('model_conv.h5')
    game.play_new_game(10, model.act_best)


#play_human(30)
train()
play_ai()
