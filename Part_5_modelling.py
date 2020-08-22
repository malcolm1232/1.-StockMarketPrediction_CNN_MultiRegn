import pandas as pd
import time
import numpy as np

import glob
import cv2
import os
import locale

import matplotlib.pyplot as plt
from math import sqrt
import matplotlib.pyplot as pyplot

from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Dropout
from keras.layers.core import Dense
from keras.layers import Flatten
from keras.layers import Input
from keras.models import Model
from keras.layers.core import Dense
from keras.models import Model
from keras.optimizers import Adam
from keras.layers import concatenate

from pandas import set_option

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 1000)

# Change all the 'C:/Users/malco' to your user name
# Image Path
stock_img_path = 'C:/Users/malco/Desktop/Image/Fixed Window Period Image/Combined Data Nasdaq 1min 2020 apr ALL GREEN/Window = ALL'
#  CSV Path
df_main = pd.read_csv('C:/Users/malco/Desktop/Combined Data/Nasdaq 1min/2020 apr ALL GREEN_ENCODED.csv')

# drop values that are float
df = df_main.copy()
categorical_feature_mask_float_float = df.dtypes == float
categorical_feature_mask_float_float = df.columns[categorical_feature_mask_float_float].tolist()
df.drop(categorical_feature_mask_float_float, axis=1, inplace=True)

df_y = df_main['price']
print("df_y:", df_y)
desired_lag = 10

def timeseries_to_supervised(data, lag_duration=desired_lag):
    df = pd.DataFrame(data)
    columns = [df.shift(i) for i in range(1, lag_duration + 1)]
    columns.append(df)

    df = pd.concat(columns, axis=1)
    df.columns = ['price_10_objective', 'price']

    # fill because after shifting u will get 'NaN'
    df.fillna(0, inplace=True)
    return df


df_trainY = timeseries_to_supervised(df_y, lag_duration=1)
df.drop(['Unnamed: 0'], axis=1, inplace = True)
df = pd.concat([df_trainY, df], axis=1)

df = df[:990]  # length to shorten for checking
df = df[desired_lag:]  # drop df by amount of time_lag as they are 0's after df.shift

df = df.reset_index()
print("Commence Loading Stock images......")
tic_imageload = time.time()

images = []
for i in df.index.values:
    print('Loading Image:', i)
    basePath = os.path.sep.join([stock_img_path, "{}_*".format(i + 1)])
    StockPathS = sorted(list(glob.glob(basePath)))
    print('StockPathS:', StockPathS)
    list_input_images = []
    output_Image = np.zeros((64, 64, 3), dtype="uint8")
    for each_window in StockPathS:
        window_image = cv2.imread(each_window)
        window_image = cv2.resize(window_image, (32, 32))
        list_input_images.append(window_image)
    output_Image[0:32, 0:32] = list_input_images[0]
    output_Image[0:32, 32:64] = list_input_images[1]
    output_Image[32:64, 32:64] = list_input_images[2]
    output_Image[32:64, 0:32] = list_input_images[3]
    images.append(output_Image)

images = np.array(images)

# Check how long it takes to load images as in 24 hours, i personally may produce ~600k images
toc_imageload = time.time()
tac_imageload = toc_imageload - tic_imageload
df.drop('index', axis=1, inplace=True)
print('Time taken to load image is {} seconds'.format(tac_imageload))

# note to change your test size according to desired_lag.
X_train_csv, X_test_csv, X_train_IMAGES, X_test_IMAGES = train_test_split(df, images, test_size=0.1, shuffle=False)

# scale your price
scaler_price = X_train_csv['price'].max()
X_train_csv['price'] = X_train_csv['price'] / scaler_price
X_test_csv['price'] = X_test_csv['price'] / scaler_price

trainY = X_train_csv['price_10_objective'] / scaler_price
testY = X_test_csv['price_10_objective'] / scaler_price

# drop target values from
X_train_csv.drop(['price_10_objective'], axis=1, inplace=True)
X_test_csv.drop(['price_10_objective'], axis=1, inplace=True)

def get_MultiLayerPerceptron(dim, regress=False):
    model = Sequential()
    model.add(Dense(50, input_dim=dim, activation='relu'))
    model.add(Dense(30, activation='relu'))
    model.add(Dense(4, activation='relu'))
    if regress:
        model.add(Dense(1, activation='linear'))
    return model

def get_ConvNeuralNet(width, height, depth, filters=(16, 32, 64), regress=False):
    shape_input = (height, width, depth)
    dim_ = -1
    inputs = Input(shape=shape_input)
    for (i, f) in enumerate(filters):

        if i == 0:
            x = inputs
        x = Conv2D(f, (3, 3), padding='same')(x)
        x = Activation('relu')(x)
        x = BatchNormalization(axis=dim_)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)

        x = Flatten()(x)
        x = Dense(16)(x)
        x = BatchNormalization(axis=dim_)(x)
        x = Dropout(0.5)(x)

        x = Dense(4)(x)
        x = Activation('relu')(x)
        if regress:
            x = Dense(1, activation='linear')(x)

        model = Model(inputs, x)
        return model


# create the MLP and CNN models
MultiLPerceptron = get_MultiLayerPerceptron(X_train_csv.shape[1], regress=False)
ConvNN = get_ConvNeuralNet(64, 64, 3, regress=False)

MultiLPerceptron_ConvNN = concatenate([MultiLPerceptron.output, ConvNN.output])

x = Dense(4, activation="relu")(MultiLPerceptron_ConvNN)
x = Dense(1, activation="linear")(x)

model = Model(inputs=[MultiLPerceptron.input, ConvNN.input], outputs=x)
opt = Adam(lr=1e-3, decay=1e-3 / 200)
model.compile(loss="mean_absolute_percentage_error", optimizer=opt)

print("Commence Training")
model.fit(
    [X_train_csv, X_train_IMAGES], trainY,
    validation_data=([X_test_csv, X_test_IMAGES], testY),
    epochs=25, batch_size=8)  # 50#% too little. #20 okay
# make predictions on the testing data
print("Predicting Stock prices...")
yhat = model.predict([X_test_csv, X_test_IMAGES])
print("Prediction  Completed...")
print('___________________________________________________________ Statistics (Basics) ___________________________________________________________')

# Basic Statistics on Stock Price
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
print("Statistics on Actual* Stock Price: \n Average. Stock price: {}, Standard Deviation Stock Price: {}".format(
    locale.currency(df["price"].mean(), grouping=True),
    locale.currency(df["price"].std(), grouping=True)))

# Compute difference between Predicted vs Actual Stock Price.
# Compute the percentage difference and
# Absolute percentage difference
difference = yhat.flatten() - testY
print("preds.flatten():", yhat.flatten())
percent_diff = (difference / testY) * 100
abs_percent_diff = np.abs(percent_diff)

mean = np.mean(abs_percent_diff)
std = np.std(abs_percent_diff)
print("Statistics on Predicted* Stock Price: \nMean: {:.2f}%, Standard Devn: {:.2f}%".format(mean, std))

# Reverse previous scale
reverse_scaled_yhat = scaler_price * yhat
actual_yhat = scaler_price * testY
print("reverse_scaled_yhat:", reverse_scaled_yhat)
print("actual_yhat:", actual_yhat)

# RMSE
rmse_actual = sqrt(mean_squared_error(reverse_scaled_yhat, actual_yhat))
print('Root Mean Squared Error : %.9f' % rmse_actual)

# Visualize Actual vs Prediction
actual_yhat = actual_yhat.tolist()
real = plt.plot(actual_yhat, label='actual')
pred = plt.plot(reverse_scaled_yhat, label='predicted')
plt.legend(['actual', 'predicted'])
plt.show()

# Visualize Learning Rate
training_loss = model.history.history['loss']
test_loss = model.history.history['val_loss']
epoch_count = range(1, len(training_loss) + 1)
plt.plot(epoch_count, training_loss, 'r--')
plt.plot(epoch_count, test_loss, 'b--')
plt.legend(['Training Loss', 'Test Loss'])
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.show()

# To Visually Compare Prediction vs Actual Price
reverse_scaled_yhat_df = pd.DataFrame(reverse_scaled_yhat)
actual_yhat = pd.DataFrame(actual_yhat)
df_compare = pd.concat([actual_yhat, reverse_scaled_yhat_df], axis=1)
df_compare.columns = ['Actual', 'Prediction']
print('___________________________________________________________ Visual Inspection ___________________________________________________________')
print(df_compare)
