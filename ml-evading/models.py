import torch
import torch.nn.functional as F
from MalConv import MalConv
from ember import predict_sample
import lightgbm as lgb
import numpy as np
from os import listdir
from os.path import isfile, join

MALCONV_MODEL_PATH = 'src/models/malconv/malconv.checkpoint'
EMBER_MODEL_PATH = 'src/models/ember/ember_model.txt'

class MalConvModel(object):
    def __init__(self, model_path, thresh=0.5, name='malconv'): 
        self.model = MalConv(channels=256, window_size=512, embd_size=8).train()
        weights = torch.load(model_path,map_location='cpu')
        self.model.load_state_dict( weights['model_state_dict'])
        self.thresh = thresh
        self.__name__ = name

    def predict(self, bytez):
        _inp = torch.from_numpy( np.frombuffer(bytez,dtype=np.uint8)[np.newaxis,:] )
        with torch.no_grad():
            outputs = F.softmax( self.model(_inp), dim=-1)

        return outputs.detach().numpy()[0,1] > self.thresh


class EmberModel(object):
    # ember_threshold = 0.8336 # resulting in 1% FPR
    def __init__(self, model_path=EMBER_MODEL_PATH, thresh=0.8336, name='ember'):
        # load lightgbm model
        self.model = lgb.Booster(model_file=model_path)
        self.thresh = thresh
        self.__name__ = 'ember'

    def predict(self,bytez):
        return predict_sample(self.model, bytez)

if __name__ == '__main__':
    #malconv = MalConvModel(MALCONV_MODEL_PATH, thresh=0.5 )
    ember = EmberModel(EMBER_MODEL_PATH, thresh=0.8336 )
    #models = [malconv,ember]
    models = [ember]

    import sys
    only_files = [f for f in listdir("src/in") if isfile(join("src/in", f))]
    print(only_files)
    for sample in only_files:
        file_path = join("src/in", sample)
        with open(file_path,'rb') as infile:
            bytez = infile.read()
            for m in models:
                print( f'{m.__name__}: {m.predict(bytez)}')

    
