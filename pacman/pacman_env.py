import numpy as np
from PIL import Image, ImageDraw
import cv2
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time

style.use("ggplot")

SIZE = 15           # size of grid
HM_EPISODES = 50000 # number of episode iterations
WALL_PENALTY = 200
FOOD_REWARD = 25
MOVE_PENALTY = 1
SHOW_EVERY = 1000
STEPS = 200
LEARNING_RATE = 0.1
DISCOUNT = 0.95

class QTable:
    def __init__(self):
        self.table = {}
        for x1 in range(-SIZE+1, SIZE):
            for y1 in range(-SIZE+1, SIZE):
                for x2 in range(-SIZE+1, SIZE):
                    for y2 in range(-SIZE+1, SIZE):
                        # there are 4 discrete actions
                        self.table[((x1, y1), (x2, y2))] = [np.random.uniform(-4,0) for i in range(4)]

    def update(self, obs, action, new_obs, reward):
        max_future_q = np.max(self.table[new_obs])
        current_q = self.table[obs][action]

        if reward in [FOOD_REWARD, -WALL_PENALTY]:
            new_q = reward
        else:
            new_q = (1-LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

        self.table[obs][action] = new_q


class Maze:
    BLOCK_N = (255,255,255)
    FOOD_N = (0,255,0)
    PLAYER_N = (0,255,255)
    ENEMY_N = (0,0,255)

    def __init__(self, arr):
        self.grid = arr

    def hitWall(self, blob):
        return self.grid[blob.x][blob.y]

    def render(self, player, enemies, food):
        env = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
        image = Image.fromarray(env, "RGB")

        for x in range(SIZE):
            for y in range(SIZE):
                if self.grid[x][y] == 1:
                    env[x][y] = self.BLOCK_N

        # render blob
        player_x, player_y = player
        env[player_x][player_y] = self.PLAYER_N

        # render enemy
        for enemy in enemies:
            enemy_x, enemy_y = enemy
            env[enemy_x][enemy_y] = self.ENEMY_N

        # render food
        food_x, food_y = food
        env[food_x][food_y] = self.FOOD_N

        img = Image.fromarray(env, "RGB")
        img = img.resize((500,500))
        return img

class Blob:
    def __init__(self, coord):
        self.x = coord[0]
        self.y = coord[1]

    def __str__(self):
        return f"{self.x}, {self.y}"

    # observation space is going to be relative position (if not it is too complex)
    def __sub__(self, other):
        return (self.x-other.x, self.y-other.y)

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def action(self, choice):
        if choice == 0:   self.move(x=1, y=0)
        elif choice == 1: self.move(x=-1, y=0)
        elif choice == 2: self.move(x=0, y=1)
        elif choice == 3: self.move(x=0, y=-1)

    def move(self, x=False, y=False):
        self.x += x
        self.y += y

        if self.x < 1:        self.x = 1
        elif self.x > SIZE-2: self.x = SIZE-2
        if self.y < 1:        self.y = 1
        elif self.y > SIZE-2: self.y = SIZE-2

    # prevent blobs from jumping over one another on the map
    def jump(self, other, choice_self, choice_other):
        if (self.x == other.x) and (self.y+1 == other.y) and (choice_self == 3) and (choice_other == 2):
            return True
        elif (self.x == other.x) and (self.y == other.y+1) and (choice_self == 2) and (choice_other == 3):
            return True
        elif (self.x+1 == other.x) and (self.y == other.y) and (choice_self == 1) and (choice_other == 0):
            return True
        elif (self.x == other.x+1) and (self.y == other.y) and (choice_self == 0) and (choice_other == 1):
            return True
        return False

maze = Maze(arr=[
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,1,0,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,1,0,1,0,1],
    [1,0,1,0,1,0,0,0,0,0,1,0,1,0,1],
    [1,0,0,0,1,0,1,1,1,0,1,0,0,0,1],
    [1,0,1,0,1,0,0,0,0,0,1,0,1,0,1],
    [1,0,1,0,1,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,1,0,0,1,0,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,0,1,0,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
])

# initialize qtable for player and enemy
q_table = QTable()
q_table_e1 = QTable()

# start episodes
episode_rewards = []
for episode in range(HM_EPISODES):
    player = Blob([1, 1])
    enemy1 = Blob([SIZE-4, SIZE-2])
    food = Blob([SIZE-2, SIZE-2])

    if episode % SHOW_EVERY == 0:
        print(f"on # {episode}")
        print(f"{SHOW_EVERY} ep mean {np.mean(episode_rewards[-SHOW_EVERY:])}")
        show = True
    else:
        show = False

    episode_reward = 0
    for i in range(STEPS):
        # record observation
        obs = ((player.x, player.y), (enemy1.x, enemy1.y))
        # move player and enemy
        action = np.argmax(q_table.table[obs])
        player.action(action)
        action_e1 = np.argmax(q_table_e1.table[obs])
        enemy1.action(action_e1)
        # update observation
        new_obs = ((player.x, player.y), (enemy1.x, enemy1.y))

        # compute and update new q value for player
        if (maze.hitWall(player)) or (player == enemy1) or (player.jump(enemy1, action, action_e1)):
            reward = -WALL_PENALTY
        elif player == food:
            reward = FOOD_REWARD
        else:
            reward = -MOVE_PENALTY

        q_table.update(obs, action, new_obs, reward)

        # compute and update new q value for enemy
        if maze.hitWall(enemy1):
            reward_e1 = -WALL_PENALTY
        elif (enemy1 == player) or (enemy1.jump(player, action_e1, action)):
            reward_e1 = FOOD_REWARD
        else:
            reward_e1 = -MOVE_PENALTY

        q_table_e1.update(obs, action_e1, new_obs, reward_e1)

        # show image
        if show:
            img = maze.render((player.x, player.y), [(enemy1.x, enemy1.y)], (food.x, food.y))
            cv2.imshow("", np.array(img))

            if reward == FOOD_REWARD or reward == -WALL_PENALTY or reward_e1 == -WALL_PENALTY:
                if cv2.waitKey(250) & 0xFF == ord("q"):
                    break
            else:
                if cv2.waitKey(30) & 0xFF == ord("q"):
                    break

        episode_reward += reward
        if reward == FOOD_REWARD or reward == -WALL_PENALTY or reward_e1 == -WALL_PENALTY:
            break

    episode_rewards.append(episode_reward)
