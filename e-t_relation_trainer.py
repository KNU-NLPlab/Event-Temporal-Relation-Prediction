import torch
from torch import nn
from torch.nn import functional as F
from torch.autograd import Variable
from torch.utils import data

import argparse

import et_relation_dataloader as mydataloader
import model

import argparse

import os
import json

parser = argparse.ArgumentParser()

parser.add_argument('-input', help = 'training files directory')

args = parser.parse_args()


dl = mydataloader.summ(path=os.path.join(args.input,'et_train_emb200.txt'))
dataloader = data.DataLoader(dataset=dl, batch_size=1, collate_fn=mydataloader.collate_fn)

criterion = nn.CrossEntropyLoss()

devdl = mydataloader.summ(path=os.path.join(args.input,'et_dev_emb200.txt'))
devloader = data.DataLoader(dataset=devdl, batch_size=1, collate_fn=mydataloader.collate_fn)
testdl = mydataloader.summ(path=os.path.join(args.input,'et_test_emb200.txt'))
testloader = data.DataLoader(dataset=testdl, batch_size=1, collate_fn=mydataloader.collate_fn)


def evaldata(ds):
  correct =0
  for batch in ds:
    out = etmodel(batch[0],batch[1],batch[2],batch[3])
    _,idx = out.max(dim=1)
    if idx.item() == batch[4].item():
      correct+=1
  return correct


hidden_size = 256
optimizer = torch.optim.Adam

etmodel = model.et_model(hidden_size).cuda()
optim = optimizer(etmodel.parameters())
for epoch in range(30):
  totalloss = 0

  for batch in dataloader:
        
    optim.zero_grad()
    out = etmodel(batch[0], batch[1],batch[2],batch[3])
    target = batch[4].unsqueeze(0)
    loss = criterion(out,target)
    totalloss += loss.item()
    loss.backward()
    optim.step()
      
  c = evaldata(devloader)
  print ('dev : ',c)
  torch.save(etmodel.state_dict(), 'mymodel.pt')
print ('model1 finished')

