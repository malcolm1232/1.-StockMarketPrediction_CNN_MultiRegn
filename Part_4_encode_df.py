import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

def get_label_encoded_cols(file_path_to_df):
    df = pd.read_csv(file_path_to_df)
    categorical_feature_mask = df.dtypes==object
    categorical_cols = df.columns[categorical_feature_mask].tolist()
    col_loc_list =  []
    for i in categorical_cols:
        loc = df.columns.get_loc(i)
        col_loc_list.append(loc)

    comment_ = input(str('Do you want to apply sklearn.MinMax? Type yes or no'))

    #To Apply Minmax to DataFrame of dtype == float
    if comment_ == 'yes':
        categorical_feature_mask_float_float = df.dtypes==float
        categorical_feature_mask_float_float = df.columns[categorical_feature_mask_float_float].tolist()
        categorical_feature_mask_float_float_list =  []
        for i in categorical_feature_mask_float_float:
            loc = df.columns.get_loc(i)
            categorical_feature_mask_float_float_list.append(loc)

        encoder_MinMax = MinMaxScaler()
        df_names_float = []
        count = 0
        for i in df.columns:
            if count in categorical_feature_mask_float_float_list:
                df_names_float.append(i)
            count += 1
        df[df_names_float] = encoder_MinMax.fit_transform(df[df_names_float])

    #Label Encoding of Strong Buy/Neutral/Sell/Strong Sell Signals is a definite Must.
    categorical_feature_mask_float_int = df.dtypes!=object
    categorical_feature_mask_float_int = df.columns[categorical_feature_mask_float_int].tolist()
    categorical_feature_mask_float_int_list =  []
    for i in categorical_feature_mask_float_int:
        loc = df.columns.get_loc(i)
        categorical_feature_mask_float_int_list.append(loc)

    #Commence Label Encode
    encoder_le = LabelEncoder()
    encoder_MinMax = MinMaxScaler()

    df_col_loc_list = df.loc[:,categorical_cols] #obtain categorical columns
    df_col_loc_list.fillna('FillSC', inplace= True)
    le = LabelEncoder()
    df_encoded_SCType0123 = df_col_loc_list.apply(le.fit_transform) #label encode categorical columns
    df.drop(categorical_cols, axis =1 , inplace = True) #drop SCType
    df = pd.concat([df,df_encoded_SCType0123], axis =1)

    df.drop(['Time'], axis=1, inplace=True)
    df.rename(columns={'Price': 'price'}, inplace=True)
    return df

file_path_to_df = 'C:/Users/malco/Desktop/Combined Data/Nasdaq 1min/2020 apr ALL GREEN.csv'
df = get_label_encoded_cols(file_path_to_df)

file_path_to_df = 'C:/Users/malco/Desktop/Combined Data/Nasdaq 1min/2020 apr ALL GREEN.csv'
splitted1 = file_path_to_df.split('/')[-1]
splitted2 = splitted1.split('.csv')[0]
splitted3 = splitted2 + '_ENCODED' + '.csv'
file_path_to_df2 = file_path_to_df.replace(splitted1,splitted3)

df.to_csv(file_path_to_df2)
print('Saved to CSV as:',file_path_to_df2)