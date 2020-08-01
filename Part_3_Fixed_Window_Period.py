#Source code for overlapping image.
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
import time
from matplotlib import *

tic = time.time()
def get_fixed_window_period_image(df_path,window_range):
    df = pd.read_csv(df_path)
    style.use('ggplot')

    df.reset_index()
    range_time = window_range  # window ;100#50#25

    for range_time_each in range_time:

        len_df = len(df)
        count = 0
        splitted = df_path.split('/')
        foldername_but_csv_dropped =  splitted[-1].split('.')[0]
        folder_name_to_add = splitted[-3] +' '+splitted[-2] +' '+splitted[-1] +' '+foldername_but_csv_dropped
        path = 'C:/Users/malco/Desktop/Image/Fixed Window Period Image/{}/Window = {}'.format(folder_name_to_add,range_time_each)

        if os.path.exists(path):
            print('Path exists:',path)
        else:
            os.makedirs(path)
        for i in range(len_df):
            print('printing {} to {} out of {}'.format(count,range_time_each, len_df))
            plt.plot(df['Price'][count:range_time_each])
            plt.xticks(color='w')
            plt.yticks(color='w')

            plt.savefig(path + '/{}_ImageWindow {}.png'.format(count,range_time_each))  # 100#50
            plt.close()
            count += 1
            range_time_each += 1

df_path = 'C:/Users/malco/Desktop/Combined Data/Nasdaq 1min/2020 apr ALL GREEN.csv' #Change
get_fixed_window_period_image(df_path,[50, 100, 150,200])#[50, 100,150,200]
toc = time.time()
tac = toc - tic
print('It took {} Seconds'.format(tac))