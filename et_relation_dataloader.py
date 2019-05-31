import torch
import torch.utils.data as data
from torch.autograd import Variable

from collections import Counter

import os

class summ(data.Dataset):
  def __init__(self, path='', onlytest = False, opt=None, vocab = None):
    self.target=[]
    self.et=[]
    self.we=[]
    self.pos=[]
    self.dp=[]
    self.filename=[]

    self.onlytest=onlytest
    
    for i, line in enumerate(open(path,'r')):
      items = line.strip().split('<eow>')
      if not onlytest:
        self.target.append([int(items[-1].strip())])
        self.filename.append('')
      else:
        self.filename.append(items[-1].strip())

      tet = []
      twe = []
      tpos = []
      tdp = []
      for it in items[:-1]:
        it=it.strip().split('\t')
        if len(it) < 2:
          print('except',i,line)
        try:
          tet.append([ int(x) for x in it[0].strip().split(' ')])
          twe.append([ float(x) for x in it[1].strip().split(' ')])
          tpos.append([ int(x) for x in it[2].strip().split(' ')])
          tdp.append([int(x) for x in it[3].strip().split(' ')])
        except:
          #print (line)
          print ((it[0]))
          print ((it[1]))
          print ((it[2]))
          print ((it[3]))
          exit(1)

      #print (tet)
      #print(twe)
      #print(tpos)
      #print(tdp)
      #print(self.target[-1])
      self.et.append(tet)
      self.we.append(twe)
      self.pos.append(tpos)
      self.dp.append(tdp)
      
  def __getitem__(self,idx):
    if self.onlytest:
      return self.et[idx], self.we[idx], self.pos[idx], self.dp[idx], self.filename[idx]
    else:
      return self.et[idx], self.we[idx], self.pos[idx], self.dp[idx], self.target[idx], self.filename[idx]
    #return torch.cuda.FloatTensor(self.et[idx]), torch.cuda.FloatTensor(self.we[idx]), torch.cuda.FloatTensor(self.pos[idx]), torch.cuda.FloatTensor(self.dp[idx]), torch.cuda.LongTensor(self.target[idx]).squeeze()
  def __len__(self):
    return len(self.et)



def collate_fn(batch):
  #print(batch[0])
  #print(batch[1])
  et = []
  we = []
  pos = []
  dp = []
  target = []
  filename = []
  test = False

  if len(batch[0]) < 6:
    test = True

  for b in batch:
    et.append(b[0])
    we.append(b[1])
    pos.append(b[2])
    dp.append(b[3])
    if not test:
      target.append(b[4])
    filename.append(b[-1])
  #print(et)
  if not test:
    return torch.cuda.FloatTensor(et), torch.cuda.FloatTensor(we), torch.cuda.FloatTensor(pos), torch.cuda.FloatTensor(dp), torch.cuda.LongTensor(target).squeeze(), filename
  else:
    return torch.cuda.FloatTensor(et), torch.cuda.FloatTensor(we), torch.cuda.FloatTensor(pos), torch.cuda.FloatTensor(dp), filename

