import numpy as np
from PIL import Image, ImageDraw
import cv2
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time

style.use("ggplot")

SIZE = 11           # size of grid
HM_EPISODES = 500 # number of episode iterations
WALL_PENALTY = 300
MOVE_PENALTY = 1
ESCAPE_REWARD = 25
SHOW_EVERY = 50
STEPS = 200

start_q_table = None # or filename

LEARNING_RATE = 0.1
DISCOUNT = 0.95

BLOCK_N = (255,255,255)
PLAYER_N = (255,0,0)

class Maze:
    def __init__(self, arr):
        self.grid = arr

    def hitWall(self, blob):
        return self.grid[blob.x][blob.y]

    def render(self, blob):
        env = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
        image = Image.fromarray(env, "RGB")

        for x in range(SIZE):
            for y in range(SIZE):
                if self.grid[x][y] == 1:
                    env[x][y] = BLOCK_N

        blob_x, blob_y = blob
        env[blob_x][blob_y] = PLAYER_N

        img = Image.fromarray(env, "RGB")
        img = img.resize((300,300))
        return img

class Blob:
    def __init__(self):
        self.x = 1
        self.y = 0

    def __str__(self):
        return f"{self.x}, {self.y}"

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

        if self.x < 0:        self.x = 0
        elif self.x > SIZE-1: self.x = SIZE-1
        if self.y < 0:        self.y = 0
        elif self.y > SIZE-1: self.y = SIZE-1

maze = Maze(arr=[
    [1,1,1,1,1,1,1,1,1,1,1],
    [0,0,0,1,0,0,0,0,0,0,1],
    [1,1,0,0,0,1,1,1,1,1,1],
    [1,0,0,1,1,0,0,1,1,0,1],
    [1,0,1,1,0,0,0,0,0,0,1],
    [1,0,0,0,1,0,1,1,0,1,1],
    [1,1,1,0,1,0,0,1,0,0,1],
    [1,0,0,0,1,1,0,1,1,0,1],
    [1,0,1,1,0,0,0,1,1,0,1],
    [1,0,0,0,0,1,0,0,1,0,0],
    [1,1,1,1,1,1,1,1,1,1,1]
])

# initialize qtable
if start_q_table is None:
    q_table = {}
    for x in range(SIZE):
        for y in range(SIZE):
            # there are 4 discrete actions
            q_table[(x,y)] = [np.random.uniform(-5,0) for i in range(4)]
else:
    with open(start_q_table, "rb") as f:
        q_table = pickle.load(f)

episode_rewards = []
for episode in range(HM_EPISODES):
    player = Blob()

    if episode % SHOW_EVERY == 0:
        print(f"on # {episode}")
        print(f"{SHOW_EVERY} ep mean {np.mean(episode_rewards[-SHOW_EVERY:])}")
        show = True
    else:
        show = False
    
    episode_reward = 0
    for i in range(STEPS):
        obs = (player.x, player.y)

        action = np.argmax(q_table[obs])
        player.action(action)

        if maze.hitWall(player) == 1:
            reward = -WALL_PENALTY
        elif player.x == 1 and player.y == 0:
            reward = -WALL_PENALTY
        elif player.x == SIZE-2 and player.y == SIZE-1:
            reward = ESCAPE_REWARD
        else:
            reward = -MOVE_PENALTY

        new_obs = (player.x, player.y)
        max_future_q = np.max(q_table[new_obs])
        current_q = q_table[obs][action]

        # equation for q-learning for back propagation
        if reward == -WALL_PENALTY:
            new_q = -WALL_PENALTY
        elif reward == ESCAPE_REWARD:
            new_q = ESCAPE_REWARD
        else:
            new_q = (1-LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

        # update qtable
        q_table[obs][action] = new_q

        if show:
            img = maze.render((player.x, player.y))
            cv2.imshow("", np.array(img))

            if reward == ESCAPE_REWARD or reward == -WALL_PENALTY:
                if cv2.waitKey(500) & 0xFF == ord("q"):
                    break
            else:
                if cv2.waitKey(10) & 0xFF == ord("q"):
                    break

        episode_reward += reward
        if reward == ESCAPE_REWARD or reward == -WALL_PENALTY:
            break

    episode_rewards.append(episode_reward)

moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,)) / SHOW_EVERY, mode="valid")

plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel(f"Reward {SHOW_EVERY}ma")
plt.xlabel("episode #")
plt.show()

with open(f"qtable-{int(time.time())}.pickle", "wb") as f:
    pickle.dump(q_table, f)
