import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class Linear_Qnet(nn.Module):
    def __init__(self,input_size,hidden_size,output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size,hidden_size)
        self.linear2 = nn.Linear(hidden_size,output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

class QTrainer():
    def __init__(self,model,lr,gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(),lr=lr)
        self.criterion = nn.MSELoss()
        self.device = torch.device("cuda") if (torch.cuda.is_available()) else torch.device("cpu")
    
    def train_step(self,curr_state,action,next_state,reward,game_over):
        curr_state = torch.tensor(curr_state,dtype=torch.float)
        action = torch.tensor(action,dtype=torch.long)
        next_state = torch.tensor(next_state,dtype=torch.float)
        reward = torch.tensor(reward,dtype=torch.float)

        if(len(curr_state.shape) == 1):
            curr_state = torch.unsqueeze(curr_state,dim=0)
            action = torch.unsqueeze(action,dim=0)
            next_state = torch.unsqueeze(next_state,dim=0)
            reward = torch.unsqueeze(reward,dim=0)
            game_over = (game_over,)

        old_Q = self.model(curr_state)

        target = old_Q.clone()
        for i in range(0,len(curr_state)):
            new_Q = 0
            if(game_over[i]):
                new_Q = reward[i]
            else:
                #bellman eqn - new Q(s,a) = R(s) + y*max(Q(s',a'))
                new_Q = reward[i] + self.gamma*(max(self.model(next_state[i])))
            #can assume output of nn is encoded as (Q1,[1,0,0]), (Q2,[0,1,0]), (Q3,[0,0,1])
            #from curr_state to next_state say we took action [0,1,0], then Q2 must have been the maximum Q value among Q1,Q2,Q3
            target[i][torch.argmax(action).item()] = new_Q

        self.optimizer.zero_grad()
        loss = self.criterion(target,old_Q)
        loss.backward()
        self.optimizer.step()

