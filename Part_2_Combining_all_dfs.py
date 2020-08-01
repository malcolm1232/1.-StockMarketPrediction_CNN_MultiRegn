import datetime
from time import strptime
import numpy as np
import pandas as pd
import os
starting_number = 16

emdf = pd.DataFrame()
count = 0



def get_GREEONLY_df(what_month_do_you_want_eg_june_in_small_caps, file_path_eg_ServerData1_6NDX_Fut_5min):
    what_month_do_you_want_eg_june_in_small_caps = str.lower(what_month_do_you_want_eg_june_in_small_caps)
    month_upper = str.upper(what_month_do_you_want_eg_june_in_small_caps)

    splitted = list(what_month_do_you_want_eg_june_in_small_caps)
    month_short_alphabet = str(splitted[0] + splitted[1] + splitted[2])
    print('month_short_alphabet:',month_short_alphabet)
    month = strptime(month_short_alphabet, '%b').tm_mon
    print('month:',month)
    month = str(0) + str(month)
    print('month:',month)
    # base_fname = 'C:/Users/malco/Desktop/Server Data 2/13. BTC-USD(OrderBk)/2020-06-29/binance_2020-06-29BTC-USD_(OrderBk).csv'
    # base_fname_tempo = 'C:/Users/malco/Desktop/Server Data 2/13. BTC-USD(OrderBk)(old tempo)/2020-06-{}/binance_2020-06-{}BTC-USD_(OrderBk).csv'

    # base_fname= 'C:/Users/malco/Desktop/Server Data 2/13. BTC-USD(OrderBk)'#actual
    file_path = 'C:/Users/malco/Desktop/Nasdaq 1min'
    file_path1 = file_path.split('/')[-1]
    file_path2 = file_path.split('/')[-2]
    file_path3 = file_path.split(file_path2)[0]
    path_to_csv_nogreen_dir = file_path3 + file_path2 + '/ALL MONTHS/' + file_path1
    if os.path.exists(path_to_csv_nogreen_dir):
        print('path Exists:',path_to_csv_nogreen_dir)
    else:
        os.makedirs(path_to_csv_nogreen_dir)
        print('Path Made:',path_to_csv_nogreen_dir)
    path_to_csv_nogreen = file_path3 + file_path2 + '/ALL MONTHS/' + file_path1+ '/2020 ' + month_short_alphabet + 'ALL (Green and red).csv'
    path_to_csv_GREEN = file_path3 + file_path2 + '/ALL MONTHS/' + file_path1 + '/2020 ' + month_short_alphabet + 'ALL GREEN.csv'
    print('file_path1:',file_path1)
    print('file_path2:', file_path2)
    print('file_path3:', file_path3)
    print('path_to_csv_nogreen_dir:', path_to_csv_nogreen_dir)
    print('path_to_csv_nogreen:',path_to_csv_nogreen)
    print('path_to_csv_GREEN:',path_to_csv_GREEN)

    if os.path.exists(path_to_csv_nogreen):
        print('COMBINED DF EXISTS (ALL Green + No Green)')
    if os.path.exists(path_to_csv_GREEN):
        print('COMBINED DF EXISTS ( GREEN)')
        return None


    # fname_1_dir = base_fname #actual
    fname_1_dir = file_path
    print('fname_1_dir:', fname_1_dir)
    fname_list_all = os.listdir(fname_1_dir)
    print('fname_list_all:',fname_list_all)
    fname_list_all = fname_list_all[1:]
    print('fname_list_all:', fname_list_all)
    #
    dates_all_available_list = []
    desired_month_dates = []
    for i in fname_list_all:
        front = i.split('-')
        date = front[2]
        print(front)
        print('date:', date)
        if front[1] == str(month):
            print('yes month')
            desired_month_dates.append(date)
        dates_all_available_list.append(date)

    print('dates_all_available_list:', dates_all_available_list)
    print('desired_month_dates:', desired_month_dates)

    print('\nprinting dates_all_available_list\n')
    print('dates_all_available_list:',dates_all_available_list)
    emdf = pd.DataFrame()
    count = 0
    for i in dates_all_available_list:
        print('Num {}, date: {}'.format(count, i))
        count+=1

    print('\nprinting desired_month_dates\n')
    count = 0
    print('desired_month_dates:',desired_month_dates)
    for i in desired_month_dates:
        print('Num {}, date: {}'.format(count, i))
        count += 1

    print('_________________________________Section 2_________________________________')
    count_ = 0
    # desired_month_dates = desired_month_dates[:3]#shorten
    comment_ = input(str("Would you like to write file ONCE and for all at end? Type 'yes' or no'"))
    total_supposed_rows = []
    if comment_ == 'yes':
        for i in desired_month_dates:
            df = pd.read_csv('C:/Users/malco/Desktop/Nasdaq 1min/6. NDX Fut 5min/2020-{}-{}/5. Nasdaq Future Tech 1 min 2020-{}-{}.csv'.format(month, i, month, i))
            total_supposed_rows.append(df.shape[0])
            print('df for month :{}, date:{}\n'.format(month,i))
            print(df, '\n')
            print('COUNT_ IS:', count_)

            if count_ == 0:
                concatt = [emdf, df]
                df1 = pd.concat(concatt)
                print('df1:', df1)
            if count > 0:
                concatt = [df1,df]
                df1 = pd.concat(concatt)
            # if count >1:
            #     concatt = [df1, df]
            #     df1 = pd.concat(concatt)

            count_+=1
            print(df1, '\n')
        df = df1
        print('ending df:\n', df)
        #
        # df['200ma'] = df['Price'].rolling(window = 200, min_periods = 0).mean()
        # df['100ma'] = df['Price'].rolling(window = 100, min_periods = 0).mean()
        # df['50ma'] = df['Price'].rolling(window = 50, min_periods = 0).mean()
        # df['30ma'] = df['Price'].rolling(window = 30, min_periods = 0).mean()
        # df['14ma'] = df['Price'].rolling(window = 14, min_periods = 0).mean()

        print('CSV Saving to (no green) :',path_to_csv_nogreen)
        df.to_csv(path_to_csv_nogreen)
        print('concatted df; RED + GREEN\n ', df)

        df_green_only = df[df['Clock'] == 'green']
        df_green_only.to_csv(path_to_csv_GREEN)
        print('CSV Saving to (GREEN ONLY) :', path_to_csv_GREEN)
        print('concatted df GREEN ONLY\n ', df_green_only)
    if comment_ == 'no':
        for i in desired_month_dates:
            df = pd.read_csv('C:/Users/malco/Desktop/Server Data 1/6. NDX Fut 5min/2020-{}-{}/6. Nasdaq Future Tech 5 min 2020-{}-{}.csv'.format(month, i, month, i))
            total_supposed_rows.append(df.shape[0])
            print('df for month :{}, date:{}\n'.format(month, i))
            print(df, '\n')
            print('COUNT_ IS:', count_)
            if count_ == 0:
                concatt = [emdf, df]
                df1 = pd.concat(concatt)
                print('df1:', df1)
            if count > 0:
                concatt = [df1, df]
                df1 = pd.concat(concatt)

                print('CSV Saving to (no green) :', path_to_csv_nogreen)
                df1.to_csv(path_to_csv_nogreen)
                print('concatted df; RED + GREEN\n ', df1)

                df_green_only = df1[df1['Clock'] == 'green']
                df_green_only.to_csv(path_to_csv_GREEN)
                print('CSV Saving to (GREEN ONLY) :', path_to_csv_nogreen)
                print('concatted df GREEN ONLY\n ', df_green_only)
            count_ += 1

    else:
        print('invalid input')
    print('total_supposed_rows:', total_supposed_rows)

    #

file_path = 'C:/Users/malco/Desktop/Nasdaq 1min'
get_GREEONLY_df('June',file_path)
