import os
SR = 48000
FRAME_LEN = int(SR / 10)
HOP = int(FRAME_LEN / 2)
MFCC_dim = 13

fold_num = 5
seed = 2022

DIR_DATA = "./sounddr_data/"
OUTPUT_DIR = DIR_DATA + 'output/'

os.makedirs(OUTPUT_DIR, exist_ok = True)