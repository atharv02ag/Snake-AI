from sys import exit
from settings import *
from game import Game
from panel import Panel
from collections import deque
from model import QTrainer, Linear_Qnet

import torch
import random


MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001
EPSILON = 0.4

class Agent():
    def __init__(self):
        self.game = Game()
        self.panel = Panel()
        self.game_over = False
        self.epsilon = EPSILON
        self.gamma = 0.9
        self.lr = 0.001
        self.game_count = 0
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_Qnet(input_size=11,hidden_size=256,output_size=3)
        self.trainer = QTrainer(self.model,self.lr,self.gamma)
    
    def remember(self,curr_state,action,next_state,reward,game_over):
        self.memory.append((curr_state,action,next_state,reward,game_over))

    def update_Qnet(self,curr_state,action,next_state,reward,game_over):
        self.trainer.train_step(curr_state,action,next_state,reward,game_over)
    
    def train_replay_memory(self):
        batch = min(len(self.memory),BATCH_SIZE)
        sample = random.sample(self.memory,batch)

        states, actions, rewards, next_states, game_overs = zip(*sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)
    
    def get_action(self,curr_state):
        action = [0,0,0]
        self.epsilon = EPSILON*(1-(self.game_count/200))
        if(random.random() < self.epsilon):
            action[random.randint(0,2)]=1
        else:
            curr_state = torch.tensor(curr_state,dtype=torch.float)
            Q_pred = self.model(curr_state)
            action[torch.argmax(Q_pred).item()] = 1
        
        return action


def train():

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    agent = Agent()

    running = True
    while(running):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                running = False
                pygame.quit()
                exit()
        
        screen.fill(BACKGROUND_COLOR)

        curr_state = agent.game.get_state()
        action = agent.get_action(curr_state)
        reward,agent.game_over = agent.game.take_step(action)
        next_state = agent.game.get_state()

        agent.update_Qnet(curr_state,action,next_state,reward,agent.game_over)
        agent.remember(curr_state,action,next_state,reward,agent.game_over)

        if(agent.game_over):
            agent.train_replay_memory()
            agent.game_count += 1
            agent.game.reset()

        agent.game.render_ui()
        agent.panel.run()

        pygame.display.update()
        clock.tick(FPS)

if(__name__ == '__main__'):
    train()