import torch 
import torch.nn as nn 
import torch.nn.functional as F 

class SelfAttention(nn.Module):
    def __init__(self,d_model):
        super().__init__()
        #d_model = dimensions ex. 512   
        self.Wq = nn.Linear(d_model,d_model )
        self.Wk = nn.Linear(d_model,d_model)
        self.Wv = nn.Linear(d_model , d_model)

    def forward(self,x):
        Q = self.Wq(x) 
        K = self.Wk(x)
        V = self.Wv(x)

        scores = torch.matmul(Q,K.transpose(-2,-1))
        
        scores = scores/ (K.shape[-1]**0.5) # root dk
        attention_weights = F.softmax(scores,dim=-1 )
        output = torch.matmul(attention_weights,V)

        return output 
    
