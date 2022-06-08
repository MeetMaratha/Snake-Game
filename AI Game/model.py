import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        '''
        3 Layered deep learning network
        1. Input Layer (11 Values)
        2. Hidden Layer (hidden_size values)
        3. Output Layer (3 Values)
        '''
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x
    
    def save(self, file_Name = 'model.pth'):
        model_Folder_Path = './model'
        if not os.path.exists(model_Folder_Path) : os.makedirs(model_Folder_Path)

        file_Name = os.path.join(model_Folder_Path, file_Name)
        torch.save(self.state_dict(), file_Name)

class QTrainer:
    def __init__(self, model : Linear_QNet, lr : float, gamma : float):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr = self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state : list, action : int, reward : int, next_state : list, done : int):
        state = torch.tensor(state, dtype = torch.float)
        next_state = torch.tensor(next_state, dtype = torch.float)
        action = torch.tensor(action, dtype = torch.long)
        reward = torch.tensor(reward, dtype = torch.float)

        if len(state.shape) == 1:
            # We need in form (1, x) if multiple it is in form (n, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # 1 : Predicted Q values with current state
        pred = self.model(state)
        
        # 2 : r + gamma * max(next_predicted Q Value)
        # pred.clone()
        # preds[argmax(action)] = Q_new 
        target = pred.clone()

        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))
            target[idx][torch.argmax(action[idx]).item()] = Q_new

        self.optimizer.zero_grad() # Clean gradient
        loss = self.criterion(target, pred) # Calculate loss
        loss.backward() # Backpropogation
        self.optimizer.step() # Step



