import torch
from torch import nn
from torch.nn import functional as F
from torch.autograd import Variable
from torch.utils import data

import argparse

import et_relation_dataloader as mydataloader

import model

import os
import json

parser = argparse.ArgumentParser()

parser.add_argument('-model', help = 'model(.pt) file path')

parser.add_argument('-input', help = 'input(result of maketest py) file path')

parser.add_argument('-output', default = 'filename_result_all.txt', help = 'output(filename,result) file path')

args = parser.parse_args()


# test input 파일경로
#testdl = mydataloader.summ(path='top_test_all_data_emb200.txt',onlytest = True)
testdl = mydataloader.summ(path=args.input,onlytest = True)

testloader = data.DataLoader(dataset=testdl, batch_size=1, collate_fn=mydataloader.collate_fn)

print ('data loaded')

def evaldata(ds):
    correct =0
    for batch in ds:
        out = etmodel(batch[0],batch[1],batch[2],batch[3])
        _,idx = out.max(dim=1)
        if idx.item() == batch[4].item():
            correct+=1
    return correct


hh=256
etmodel = model.et_model(hh).cuda()


#모델(.pt) 경로
#etmodel.load_state_dict(torch.load('emb200_300_adagrad/et.model_20'))
etmodel.load_state_dict(torch.load(args.model))
print('model loaded')


def extract_tlink_filename(filename):
    t=0
    f=''

    link = filename.split('-')[-1].split('.')[0]

    t = int(link)

    f = filename.replace('-{}.'.format(link),'.')
    

    return t,f


# 파일명, 결과 가 저장되는 파일
#ffr = open('filename_result_all.txt','w')
ffr = open(args.output,'w')

for i,batch in enumerate(testloader):
    t,fname = extract_tlink_filename(batch[4][0])
    out = etmodel(batch[0], batch[1],batch[2],batch[3])
    _,idx = out.max(dim=1)


    ffr.write( batch[4][0] + '\t'+ str(idx.item()) + '\n')
