#-*- coding: utf-8 -*-

import torch
from torch import nn
from torch.nn import functional as F
from torch.autograd import Variable
from torch.utils import data

import etlink.mydataloader as mydataloader
import etlink.model.etmodel.model as model

import os, json


class etlink(nn.Module) :
	def __init__(self, model_path) :
		super(etlink, self).__init__()
		# Model
		self.etmodel = model.et_model(300).cuda()
		self.etmodel.load_state_dict(torch.load(model_path))


	def predict(self, input_path, input_json, output_path, output_json) :
		testdl = mydataloader.summ(path = input_path, onlytest = True)
		testloader = data.DataLoader(dataset = testdl, batch_size = 1, collate_fn = mydataloader.collate_fn)

		filelist = self.search(input_json)

		#### Event - time link predict ####
		# Write result
		ffr = open(output_path, 'w')

		for i,batch in enumerate(testloader):
			t,fname = self.extract_tlink_filename(batch[4][0])
			out = self.etmodel(batch[0], batch[1],batch[2],batch[3])
			_,idx = out.max(dim=1)

			# 결과 json 파일이 저정될 디렉토리 경로
			savename = os.path.join(output_json + fname)

			nofile = False
			if os.path.isfile(savename):
				full_filename = savename
			else:
				if len([x for x in filelist if fname in x]) ==0:
					nofile = True
				else:
					full_filename = [x for x in filelist if fname in x][0]

			ffr.write(batch[4][0] + '\t'+ str(idx.item()) + '\n')

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

		return


	def search(self,dirname) :
		filelist = []

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

		return filelist


	def extract_tlink_filename(self,filename):
		t, f=0, ''

		link = filename.split('-')[-1].split('.')[0]

		t = int(link)

		f = filename.replace('-{}.'.format(link),'.')


		return t,f


