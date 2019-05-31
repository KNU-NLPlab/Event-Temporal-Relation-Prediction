import torch
from torch import nn
from torch.nn import functional as F
from torch.autograd import Variable
import random



class et_model(nn.Module):
  def __init__(self,hidden_size):
    super(et_model,self).__init__()
    self.hidden_size = hidden_size
    

    self.e_rnn = nn.GRU(3, self.hidden_size, bidirectional=True)
    self.w_rnn = nn.GRU(200, self.hidden_size, bidirectional=True)
    self.p_rnn = nn.GRU(45,  self.hidden_size, bidirectional=True)
    self.d_rnn = nn.GRU(20,  self.hidden_size, bidirectional=True)

    self.concat_linear = nn.Linear(self.hidden_size * 8, self.hidden_size *2)
    self.out = nn.Linear (self.hidden_size *2, 2)
    
  def forward(self, ee, we, pos, dp):
    ee =  ee.transpose(1,0)
    we =  we.transpose(1,0)
    pos =pos.transpose(1,0)
    dp =  dp.transpose(1,0)


    eout,_ = self.e_rnn(ee)
    wout,_ = self.w_rnn(we)
    pout,_ = self.p_rnn(pos)
    dout,_ = self.d_rnn(dp)
    
    catin = torch.cat( (eout[-1], wout[-1], pout[-1], dout[-1]), dim=1)
    #print (catin.size())

    out = self.concat_linear(catin)
    out = self.out(out)

    return out


