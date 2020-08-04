#Source code for overlapping image.
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
import time
from matplotlib import *
#(foldername: 2020 April, IMAGE 2020 APRIL_timestep = 1min, IMAGE 2020 APRIL_timestep_MovingAverage = 1min
#initial df = pd.read_csv('C:/Users/malco/Desktop/5. AWS NDX Fut 1min/2020 April.csv', header=0,index_col=0)

tic = time.time()
def get_fixed_window_period_image(df_path,window_range):
    df = pd.read_csv(df_path)
    style.use('ggplot')
    df.reset_index()
    range_time = window_range  # window ;100#50#25
    window_range_num = window_range[0]

    for range_time_each in range_time:
        len_df = len(df)
        count = 0
        splitted = df_path.split('/')
        foldername_but_csv_dropped =  splitted[-1].split('.')[0]
        folder_name_to_add = splitted[-3] +' '+splitted[-2] +' '+foldername_but_csv_dropped#Change Folder Name here
        # path = 'C:/Users/malco/Desktop/NN Data/Fixed Window Period Image/{}/Window = {}'.format(folder_name_to_add,range_time_each)#Type1 Actual
        path = 'C:/Users/malco/Desktop/Image/Fixed Window Period Image/{}/Window = ALL'.format(folder_name_to_add,range_time_each)

        if os.path.exists(path):
            print('Path exists:',path)
        else:
            print('Path does not exist, commence creating file')
            os.makedirs(path)
            print('Path created:', path)
        for i in range(len_df):
            print('printing {} to {} out of {}'.format(count,range_time_each, len_df))
            plt.plot(df['Price'][count:range_time_each])
            plt.xticks(color='w')
            plt.yticks(color='w')
            plt.savefig(path + '/{}_ImageWindow {}.png'.format(count,window_range_num))  # 100#50
            plt.close()
            count += 1
            range_time_each += 1

df_path = 'C:/Users/malco/Desktop/Combined Data/Nasdaq 1min/2020 apr ALL GREEN.csv'
get_fixed_window_period_image(df_path,[50])#NOTE DONT LOOP, USE ONE AT A TIME
toc = time.time()
tac = toc - tic
print('It took {} Seconds'.format(tac))