import argparse
import pickle
from tqdm import tqdm
from utils import ls, preprocess_wav, melspectrogram
import os
import glob

parser = argparse.ArgumentParser()
parser.add_argument("--model_name", type=str, help="name of the model")
parser.add_argument("--dataset", type=str, help="path to dataset")
parser.add_argument("--n_spkrs", type=int, default=2, help="size of the batches")

opt = parser.parse_args()
print(opt)
feats = {}

for spkr in range(opt.n_spkrs):
    wavs = glob.glob('%s/spkr_%s/*.wav'%(opt.dataset, spkr+1))
    wavs = [w.replace('\\', '/') for w in wavs]
    feats[spkr] = [None]*len(wavs)
    for i, wav in tqdm(enumerate(wavs), total=len(wavs), desc="spkr_%d"%(spkr+1)):
        sample = preprocess_wav(wav)
        feats[spkr][i] = melspectrogram(sample)

pickle.dump(feats,open('%s/%s.pickle'%(opt.dataset, opt.model_name),'wb'))
