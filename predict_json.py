import torch
from torch import nn
from torch.nn import functional as F
from torch.autograd import Variable
from torch.utils import data

import argparse

import mydataloader
import model

import os
import json

parser = argparse.ArgumentParser()

parser.add_argument('-model', help = 'model(.pt) file path')

parser.add_argument('-input', help = 'input(result of maketest py) file path')
parser.add_argument('-input_json', help = 'input json directory path')

parser.add_argument('-out_name', default = 'filename_result_all.txt', help = 'output(filename,result) file path')
parser.add_argument('-out_json', help = 'directory of result json file path')

args = parser.parse_args()


# test input 파일경로
#testdl = mydataloader.summ(path='top_test_all_data_emb200.txt',onlytest = True)
testdl = mydataloader.summ(path=args.input,onlytest = True)

testloader = data.DataLoader(dataset=testdl, batch_size=1, collate_fn=mydataloader.collate_fn)

#print ('data loaded')

def evaldata(ds):
    correct =0
    for batch in ds:
        out = etmodel(batch[0],batch[1],batch[2],batch[3])
        _,idx = out.max(dim=1)
        if idx.item() == batch[4].item():
            correct+=1
    return correct


hh=300
etmodel = model.et_model(hh).cuda()


#모델(.pt) 경로
#etmodel.load_state_dict(torch.load('emb200_300_adagrad/et.model_20'))
etmodel.load_state_dict(torch.load(args.model))
#print('model loaded')


filelist = []

def search(dirname):
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search(full_filename)
            else:
                filelist.append(full_filename)
    except PermissionError:
        pass


# 원본 json 파일이 있는 경로
#search("/shared/emb200_full/etlink/")
search(args.input_json)

def extract_tlink_filename(filename):
    t=0
    f=''

    link = filename.split('-')[-1].split('.')[0]

    t = int(link)

    f = filename.replace('-{}.'.format(link),'.')
    

    return t,f


# 파일명, 결과 가 저장되는 파일
#ffr = open('filename_result_all.txt','w')
ffr = open(args.out_name,'w')

for i,batch in enumerate(testloader):
    t,fname = extract_tlink_filename(batch[4][0])
    out = etmodel(batch[0], batch[1],batch[2],batch[3])
    _,idx = out.max(dim=1)

    # 결과 json 파일이 저정될 디렉토리 경로
    # savename = os.path.join('link_result_all/' + fname)
    savename = os.path.join(args.out_json + fname)

    nofile = False
    if os.path.isfile(savename):
        full_filename = savename
    else:
        if len([x for x in filelist if fname in x]) ==0:
            nofile = True
        else:
            full_filename = [x for x in filelist if fname in x][0]

    ffr.write( batch[4][0] + '\t'+ str(idx.item()) + '\n')

    if nofile:
        continue

    lines = ''
    for line in open(full_filename,'r'):
        lines+=line

    try:
        js = json.loads(lines)
    except:
        print ('error in',full_filename)
        print ('program exit')
        exit(1)

    fjsonout = open(savename,'w',encoding='utf-8')
    if 'etlink' not in js:
        js['etlink'] = []
    if idx.item() == 1:
        js['etlink'].append(t)

    json.dump(js, fjsonout, sort_keys=True, ensure_ascii = False)
    fjsonout.close()
