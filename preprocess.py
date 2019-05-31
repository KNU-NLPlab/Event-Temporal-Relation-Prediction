# -*- coding:utf-8 -*-
import json
import os
import sys
import random

#fout = open('top_test_all_data_emb200.txt','w')
fout = open(sys.argv[3],'w')
ignore_cnt = 0
all_cnt = 0

def search(dirname):
    global all_cnt
    global ignore_cnt
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search(full_filename)
            else:
                all_cnt += 1
                writer = ''
                flag=False
                #writer += filename + '\t'
                for i,line in enumerate(open(full_filename,'r')):
                    #datas = json.loads(line)
                    if line.find('[[')>=0:
                        flag = True
                        ignore_cnt += 1
                        break
                        #datas = json.loads(line)
                    #print (full_filename,target)
                    it = line.strip().split(' ')
                    if len(it) < 200:
                        flag=True
                        ignore_cnt += 1
                        print(len(it))
                        break
                    etsz = 3
                    wesz = 200
                    possz = 45
                    
                    et = it[:etsz]
                    we = it[etsz:etsz+wesz]
                    pos = it[etsz+wesz:etsz+wesz+possz]
                    dp = it[etsz+wesz+possz:]

                    #print(et)
                    #print(we)
                    #print(pos)
                    #print(dp)
                    #print(len(dp))
                    #print ()
                    writer += ' '.join(et)+'\t' + ' '.join(we) + '\t'+' '.join(pos)+'\t'+' '.join(dp)+'\t<eow>\t'
                if not flag:
                    if len(writer) <10:
                        print (full_filename)
                    writer += filename
                    writer = writer.strip()
                    fout.write(writer + '\n')


    except PermissionError:
        print ('permissionerror')
        pass
    
def main(inPath, outPath) :
        for path, dic, files in os.walk(inPath) :
                for file in files :
                        tmpdic = []

                        with open(path + file, 'r', encoding='utf-8') as f :
                                tmpdic = json.loads(f.read())

                        sentList = []
                        for tlink in tmpdic['tlink'] :
                                tset = []
                                for ele in tlink:
                                        word = []
                                        word+=ele['entity']
                                        word+=ele['wordembedding']
                                        word+=ele['POS']
                                        word+=ele['dp']

                                        tset.append(word)
                                sentList.append(tset)

                        for idx, tset in enumerate(sentList) :
                                _file = file.split('.txt')[0] + '-' + str(idx) + '.txt'
                                with open(outPath + _file, 'w', encoding = 'utf-8') as f:
                                        for word in tset :
                                                for ele in word:
                                                        f.write(str(ele)+' ')
                                                f.write('\n')
#search("/shared/emb200_full/etTestData/")
main(sys.argv[1], sys.argv[2])
search(sys.argv[2])
print ('all',all_cnt)
print ('ignore', ignore_cnt)
