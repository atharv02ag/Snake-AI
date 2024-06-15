import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

#Using a linear neural network with single hidden layer
class Linear_Qnet(nn.Module):
    def __init__(self,input_size,hidden_size,output_size,device):
        super().__init__()
        self.linear1 = nn.Linear(input_size,hidden_size)
        self.linear2 = nn.Linear(hidden_size,output_size)
        self.to(device)

    def forward(self, state):
        x = F.relu(self.linear1(state))
        x = self.linear2(x)
        return x

#Trainer class used to train model
class QTrainer():
    def __init__(self,model,lr,gamma,device):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(),lr=lr)
        self.criterion = nn.MSELoss()
        self.device = device
    
    #used to update network based on consecutive moves of agent
    #also used to train replay memory, by considering mini batch (solution to breaking correlation between sequential states)
    def train_step(self,curr_state,action,next_state,reward,game_over):

        #consider list of states, actions, next_states, rewards if training mini-batch
        curr_state = torch.tensor(curr_state,dtype=torch.float).to(self.device)
        action = torch.tensor(action,dtype=torch.long).to(self.device)
        next_state = torch.tensor(next_state,dtype=torch.float).to(self.device)
        reward = torch.tensor(reward,dtype=torch.float).to(self.device)

        #but if updating Q values based on each action taken by agent, only single state, action, next_state and reward considered
        if(len(curr_state.shape) == 1):
            curr_state = torch.unsqueeze(curr_state,dim=0)
            action = torch.unsqueeze(action,dim=0)
            next_state = torch.unsqueeze(next_state,dim=0)
            reward = torch.unsqueeze(reward,dim=0)
            game_over = [game_over]

        #implementing bellman's equation
        old_Q = self.model.forward(curr_state)

        Q_target = old_Q.clone()
        for i in range(0,len(curr_state)):
            new_Q = 0
            if(game_over[i]):
                new_Q = reward[i]
            else:
                #bellman eqn -> new Q(s,a) = R(s) + y*max(Q(s',a'))
                new_Q = reward[i] + self.gamma*(max(self.model.forward(next_state[i])))

            #can assume output of nn is encoded as (Q1,[1,0,0]), (Q2,[0,1,0]), (Q3,[0,0,1])
            #from curr_state to next_state say we took action [0,1,0], then Q2 must have been the maximum Q value among Q1,Q2,Q3
            Q_target[i][torch.argmax(action[i]).item()] = new_Q

        #calling backpropogation to update neural network's weights and biases
        self.optimizer.zero_grad()

        #loss is measured as mean square error between predicted Q (old_Q) and target Q (as found by bellman's eqn)
        loss = self.criterion(Q_target,old_Q).to(self.device)
        loss.backward()
        self.optimizer.step()

