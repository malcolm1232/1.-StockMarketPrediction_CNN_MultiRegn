import datetime
from time import strptime
import numpy as np
import pandas as pd
import os

emdf = pd.DataFrame()
count = 0

def get_GREEONLY_df(what_month_do_you_want_eg_june_in_small_caps, file_path_eg_ServerData1_6NDX_Fut_5min):
    what_month_do_you_want_eg_june_in_small_caps = str.lower(what_month_do_you_want_eg_june_in_small_caps)
    month_upper = str.upper(what_month_do_you_want_eg_june_in_small_caps)

    splitted = list(what_month_do_you_want_eg_june_in_small_caps)
    month_short_alphabet = str(splitted[0] + splitted[1] + splitted[2])
    month = strptime(month_short_alphabet, '%b').tm_mon
    month = str(0) + str(month)

    # base_fname= 'C:/Users/malco/Desktop/Server Data 2/13. BTC-USD(OrderBk)'#actual
    file_path = 'C:/Users/malco/Desktop/Nasdaq 1min'
    file_path1 = file_path.split('/')[-1]
    file_path2 = file_path.split('/')[-2]
    file_path3 = file_path.split(file_path2)[0]
    path_to_csv_nogreen_dir = file_path3 + file_path2 + '/Combined Data/' + file_path1
    if os.path.exists(path_to_csv_nogreen_dir):
        print('path Exists:',path_to_csv_nogreen_dir)
    else:
        os.makedirs(path_to_csv_nogreen_dir)
        print('Path Made:',path_to_csv_nogreen_dir)
    path_to_csv_nogreen = file_path3 + file_path2 + '/Combined Data/' + file_path1+ '/2020 ' + month_short_alphabet + ' ALL (Green and red).csv'
    path_to_csv_GREEN = file_path3 + file_path2 + '/Combined Data/' + file_path1 + '/2020 ' + month_short_alphabet + ' ALL GREEN.csv'

    if os.path.exists(path_to_csv_nogreen):
        print('COMBINED DF EXISTS (ALL Green + No Green)')
    if os.path.exists(path_to_csv_GREEN):
        print('COMBINED DF EXISTS ( GREEN)')
        return None

    fname_1_dir = file_path
    fname_list_all = os.listdir(fname_1_dir)
    fname_list_all = fname_list_all[1:]

    dates_all_available_list = []
    desired_month_dates = []
    for i in fname_list_all:
        front = i.split('-')
        date = front[2]
        print(front)
        if front[1] == str(month):
            desired_month_dates.append(date)
        dates_all_available_list.append(date)

    emdf = pd.DataFrame()
    count = 0
    for i in dates_all_available_list:
        count+=1
    count = 0
    for i in desired_month_dates:
        count += 1

    count_ = 0
    comment_ = input(str("Would you like to write file ONCE and for all at end? Type 'yes' or no'"))
    total_supposed_rows = []
    if comment_ == 'yes':
        for i in desired_month_dates:
            df = pd.read_csv('C:/Users/malco/Desktop/Nasdaq 1min/2020-{}-{}/5. Nasdaq Future Tech 1 min 2020-{}-{}.csv'.format(month, i, month, i))
            total_supposed_rows.append(df.shape[0])

            if count_ == 0:
                concatt = [emdf, df]
                df1 = pd.concat(concatt)
                print('df1:', df1)
            if count > 0:
                concatt = [df1,df]
                df1 = pd.concat(concatt)
            count_+=1
            print(df1, '\n')
        df = df1

        # df['200ma'] = df['Price'].rolling(window = 200, min_periods = 0).mean()
        # df['100ma'] = df['Price'].rolling(window = 100, min_periods = 0).mean()
        # df['50ma'] = df['Price'].rolling(window = 50, min_periods = 0).mean()
        # df['30ma'] = df['Price'].rolling(window = 30, min_periods = 0).mean()
        # df['14ma'] = df['Price'].rolling(window = 14, min_periods = 0).mean()

        print('CSV Saving to (no green) :',path_to_csv_nogreen)
        df.to_csv(path_to_csv_nogreen)

        df_green_only = df[df['Clock'] == 'green']
        df_green_only.to_csv(path_to_csv_GREEN)
        print('CSV Saving to (GREEN ONLY) :', path_to_csv_GREEN)
        print('concatted df GREEN ONLY\n ', df_green_only)
    if comment_ == 'no':
        for i in desired_month_dates:
            df = pd.read_csv('C:/Users/malco/Desktop/Nasdaq 1min/2020-{}-{}/5. Nasdaq Future Tech 1 min 2020-{}-{}.csv'.format(month, i, month, i))
            total_supposed_rows.append(df.shape[0])
            if count_ == 0:
                concatt = [emdf, df]
                df1 = pd.concat(concatt)
            if count > 0:
                concatt = [df1, df]
                df1 = pd.concat(concatt)

                df1.to_csv(path_to_csv_nogreen)
                df_green_only = df1[df1['Clock'] == 'green']
                df_green_only.to_csv(path_to_csv_GREEN)
                print('CSV Saving to (GREEN ONLY) :', path_to_csv_nogreen)
            count_ += 1

    else:
        print('invalid input')
    print('total_supposed_rows:', total_supposed_rows)

file_path = 'C:/Users/malco/Desktop/Nasdaq 1min'
get_GREEONLY_df('april',file_path)
