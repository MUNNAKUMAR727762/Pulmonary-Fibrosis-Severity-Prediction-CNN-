# -*- coding: utf-8 -*-
"""Linear Decay (based on ResNet CNN)

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/#fileId=https%3A//storage.googleapis.com/kaggle-colab-exported-notebooks/linear-decay-based-on-resnet-cnn-c72b880a-4906-49c3-8298-babad25c3746.ipynb%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com/20240429/auto/storage/goog4_request%26X-Goog-Date%3D20240429T114837Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D65d45e385f77fccf2481a9132bb68bff2647aca60c33325849950cf9b9e97687bcd3b139990551c8308c5d8f7d0ce9ea046a2fee1a73111766736b89217fadcefbf9f72091f6bc65bc73354a9eabd666574b90ebc324ab2fdf2ecdddc50008dc6f5b6270300c2dcb63120624eba032fb404e4f53b5c79c17d29c468b98235d2a2714ea30abe64f387fb9d82ddf892f450c006b3feccd50bb43d38f78bd1502ee6d1b1fdd402207d09802333b98ac3be5e17ebbfd3fd0efe75c3d4adc0abbb0c4f7cc74699807a1c8b83fcd5143ad2d6a110f6cce660535498e61ed00343cd05f48a9a00e085b25fb6bb04aa5d3c89c32f7df6c1707b4d88d01e22842c738451a
"""

# IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES
# TO THE CORRECT LOCATION (/kaggle/input) IN YOUR NOTEBOOK,
# THEN FEEL FREE TO DELETE THIS CELL.
# NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON
# ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR
# NOTEBOOK.

import os
import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from urllib.error import HTTPError
from zipfile import ZipFile
import tarfile
import shutil

CHUNK_SIZE = 40960
DATA_SOURCE_MAPPING = 'osic-pulmonary-fibrosis-progression:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-competitions-data%2Fkaggle-v2%2F20604%2F1357052%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240429%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240429T114836Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D6e19247837a88b0813b6f70e63d1b9e136dec2c9257284ef9a9e89e9c0ab89f6ad60f951e60c50c959f40507de0a77e6c19ef63feff15042b3cba4a91e4808b9ba0e2191fbd7bc1ef64b640c96d983aa00ea39adec82ad223a292fc19f01b73f8ab765a0258be06164e8765b67c10b37d7f0305c5f9e7260f2a99470ecf1146f0d420ff0ad17afadae53ae42b0eef7bf7220e8e3f64bb7d1e7e21748a3b58f07e426932d9e9276e74ef6130f77891e2e71eb42527172a17135590d448b0979d2dfd31f7e1f1b5411f96f0d7ad6c95af303bf1f034a205a1fae2c914639ad2ed341d1133556c0cbdaf43af91316278be8850167d42dcda8f41cc88e55b0bd00d2'

KAGGLE_INPUT_PATH='/kaggle/input'
KAGGLE_WORKING_PATH='/kaggle/working'
KAGGLE_SYMLINK='kaggle'

import subprocess

# Unmounting directory
subprocess.run(["umount", "/kaggle/input/", "2>", "/dev/null"])

shutil.rmtree('/kaggle/input', ignore_errors=True)
os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)
os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)

try:
  os.symlink(KAGGLE_INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
except FileExistsError:
  pass
try:
  os.symlink(KAGGLE_WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
except FileExistsError:
  pass

for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
    directory, download_url_encoded = data_source_mapping.split(':')
    download_url = unquote(download_url_encoded)
    filename = urlparse(download_url).path
    destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)
    try:
        with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
            total_length = fileres.headers['content-length']
            print(f'Downloading {directory}, {total_length} bytes compressed')
            dl = 0
            data = fileres.read(CHUNK_SIZE)
            while len(data) > 0:
                dl += len(data)
                tfile.write(data)
                done = int(50 * dl / int(total_length))
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
                sys.stdout.flush()
                data = fileres.read(CHUNK_SIZE)
            if filename.endswith('.zip'):
              with ZipFile(tfile) as zfile:
                zfile.extractall(destination_path)
            else:
              with tarfile.open(tfile.name) as tarfile:
                tarfile.extractall(destination_path)
            print(f'\nDownloaded and uncompressed: {directory}')
    except HTTPError as e:
        print(f'Failed to load (likely expired) {download_url} to path {destination_path}')
        continue
    except OSError as e:
        print(f'Failed to load {download_url} to path {destination_path}')
        continue

print('Data source import complete.')

pip install pydicom

import os
import cv2

import pydicom
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from tqdm.notebook import tqdm

"""## Decay theory
Input for test:
   * FVC in n week
   * Percent in n week
   * Age
   * Sex
   * Smoking status
   * CT in n week
   
Result:
   * FVC in any week
   * percent in any week
   
$FVC = a.quantile(0.75) * (week - week_{test}) + FVC_{test}$

$Confidence = Percent + a.quantile(0.75) * abs(week - week_{test}) $

So let's try predict coefficient a.
"""

train = pd.read_csv('../input/osic-pulmonary-fibrosis-progression/train.csv')

train.head()

train.SmokingStatus.unique()

def get_tab(df):
    vector = [(df.Age.values[0] - 30) / 30]

    if df.Sex.values[0] == 'male':
       vector.append(0)
    else:
       vector.append(1)

    if df.SmokingStatus.values[0] == 'Never smoked':
        vector.extend([0,0])
    elif df.SmokingStatus.values[0] == 'Ex-smoker':
        vector.extend([1,1])
    elif df.SmokingStatus.values[0] == 'Currently smokes':
        vector.extend([0,1])
    else:
        vector.extend([1,0])
    return np.array(vector)

A = {}
TAB = {}
P = []
for i, p in tqdm(enumerate(train.Patient.unique())):
    sub = train.loc[train.Patient == p, :]
    fvc = sub.FVC.values
    weeks = sub.Weeks.values
    c = np.vstack([weeks, np.ones(len(weeks))]).T
    a, b = np.linalg.lstsq(c, fvc)[0]

    A[p] = a
    TAB[p] = get_tab(sub)
    P.append(p)

"""## CNN for coeff prediction"""

def get_img(path):
    d = pydicom.dcmread(path)
    return cv2.resize(d.pixel_array / 2**11, (512, 512))

from tensorflow.keras.utils import Sequence

class IGenerator(Sequence):
    BAD_ID = ['ID00011637202177653955184', 'ID00052637202186188008618']
    def __init__(self, keys, a, tab, batch_size=32):
        self.keys = [k for k in keys if k not in self.BAD_ID]
        self.a = a
        self.tab = tab
        self.batch_size = batch_size

        self.train_data = {}
        for p in train.Patient.values:
            self.train_data[p] = os.listdir(f'../input/osic-pulmonary-fibrosis-progression/train/{p}/')

    def __len__(self):
        return 1000

    def __getitem__(self, idx):
        x = []
        a, tab = [], []
        keys = np.random.choice(self.keys, size = self.batch_size)
        for k in keys:
            try:
                i = np.random.choice(self.train_data[k], size=1)[0]
                img = get_img(f'../input/osic-pulmonary-fibrosis-progression/train/{k}/{i}')
                x.append(img)
                a.append(self.a[k])
                tab.append(self.tab[k])
            except:
                print(k, i)

        x,a,tab = np.array(x), np.array(a), np.array(tab)
        x = np.expand_dims(x, axis=-1)
        return [x, tab] , a

from tensorflow.keras.layers import (
    Dense, Dropout, Activation, Flatten, Input, BatchNormalization, GlobalAveragePooling2D, Add, Conv2D, AveragePooling2D,
    LeakyReLU, Concatenate
)

from tensorflow.keras import Model
from tensorflow.keras.optimizers import Nadam

def get_model(shape=(512, 512, 1)):
    def res_block(x, n_features):
        _x = x
        x = BatchNormalization()(x)
        x = LeakyReLU(0.05)(x)

        x = Conv2D(n_features, kernel_size=(3, 3), strides=(1, 1), padding='same')(x)
        x = Add()([_x, x])
        return x

    inp = Input(shape=shape)

    # 512
    x = Conv2D(32, kernel_size=(3, 3), strides=(1, 1), padding='same')(inp)
    x = BatchNormalization()(x)
    x = LeakyReLU(0.05)(x)

    x = Conv2D(32, kernel_size=(3, 3), strides=(1, 1), padding='same')(x)
    x = BatchNormalization()(x)
    x = LeakyReLU(0.05)(x)

    x = AveragePooling2D(pool_size=(2, 2), strides=(2, 2))(x)

    # 256
    x = Conv2D(8, kernel_size=(3, 3), strides=(1, 1), padding='same')(x)
    for _ in range(2):
        x = res_block(x, 8)
    x = AveragePooling2D(pool_size=(2, 2), strides=(2, 2))(x)

    # 128
    x = Conv2D(16, kernel_size=(3, 3), strides=(1, 1), padding='same')(x)
    for _ in range(2):
        x = res_block(x, 16)
    x = AveragePooling2D(pool_size=(2, 2), strides=(2, 2))(x)

    # 64
    x = Conv2D(32, kernel_size=(3, 3), strides=(1, 1), padding='same')(x)
    for _ in range(3):
        x = res_block(x, 32)
    x = AveragePooling2D(pool_size=(2, 2), strides=(2, 2))(x)

    # 32
    x = Conv2D(64, kernel_size=(3, 3), strides=(1, 1), padding='same')(x)
    for _ in range(3):
        x = res_block(x, 64)
    x = AveragePooling2D(pool_size=(2, 2), strides=(2, 2))(x)

    # 16
    x = Conv2D(128, kernel_size=(3, 3), strides=(1, 1), padding='same')(x)
    for _ in range(3):
        x = res_block(x, 128)

    # 16
    x = GlobalAveragePooling2D()(x)

    inp2 = Input(shape=(4,))
    x2 = tf.keras.layers.GaussianNoise(0.2)(inp2)
    x = Concatenate()([x, x2])
    x = Dropout(0.6)(x)
    x = Dense(1)(x)
    #x2 = Dense(1)(x)
    return Model([inp, inp2] , x)

model = get_model()
model.summary()

from tensorflow_addons.optimizers import RectifiedAdam

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mae')

from sklearn.model_selection import train_test_split

tr_p, vl_p = train_test_split(P,
                              shuffle=True,
                              train_size= 0.8)

import seaborn as sns

sns.distplot(list(A.values()));

er = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    min_delta=1e-3,
    patience=5,
    verbose=0,
    mode="auto",
    baseline=None,
    restore_best_weights=True,
)

model.fit_generator(IGenerator(keys=tr_p,
                               a = A,
                               tab = TAB),
                    steps_per_epoch = 200,
                    validation_data=IGenerator(keys=vl_p,
                               a = A,
                               tab = TAB),
                    validation_steps = 20,
                    callbacks = [er],
                    epochs=30)

def score(fvc_true, fvc_pred, sigma):
    sigma_clip = np.maximum(sigma, 70)
    delta = np.abs(fvc_true - fvc_pred)
    delta = np.minimum(delta, 1000)
    sq2 = np.sqrt(2)
    metric = (delta / sigma_clip)*sq2 + np.log(sigma_clip* sq2)
    return np.mean(metric)

from tqdm.notebook import tqdm

metric = []
for q in tqdm(range(1, 10)):
    m = []
    for p in vl_p:
        x = []
        tab = []

        if p in ['ID00011637202177653955184', 'ID00052637202186188008618']:
            continue
        for i in os.listdir(f'../input/osic-pulmonary-fibrosis-progression/train/{p}/'):
            x.append(get_img(f'../input/osic-pulmonary-fibrosis-progression/train/{p}/{i}'))
            tab.append(get_tab(train.loc[train.Patient == p, :]))
        tab = np.array(tab)

        x = np.expand_dims(x, axis=-1)
        _a = model.predict([x, tab])
        a = np.quantile(_a, q / 10)

        percent_true = train.Percent.values[train.Patient == p]
        fvc_true = train.FVC.values[train.Patient == p]
        weeks_true = train.Weeks.values[train.Patient == p]

        fvc = a * (weeks_true - weeks_true[0]) + fvc_true[0]
        percent = percent_true[0] - a * abs(weeks_true - weeks_true[0])
        m.append(score(fvc_true, fvc, percent))
    print(np.mean(m))
    metric.append(np.mean(m))

"""## Predict"""

q = (np.argmin(metric) + 1)/ 10
q

sub = pd.read_csv('../input/osic-pulmonary-fibrosis-progression/sample_submission.csv')
sub.head()

test = pd.read_csv('../input/osic-pulmonary-fibrosis-progression/test.csv')
test.head()

A_test, B_test, P_test,W, FVC= {}, {}, {},{},{}
STD, WEEK = {}, {}
for p in test.Patient.unique():
    x = []
    tab = []
    for i in os.listdir(f'../input/osic-pulmonary-fibrosis-progression/test/{p}/'):
        x.append(get_img(f'../input/osic-pulmonary-fibrosis-progression/test/{p}/{i}'))
        tab.append(get_tab(test.loc[test.Patient == p, :]))
    tab = np.array(tab)

    x = np.expand_dims(x, axis=-1)
    _a = model.predict([x, tab])
    a = np.quantile(_a, q)
    A_test[p] = a
    B_test[p] = test.FVC.values[test.Patient == p] - a*test.Weeks.values[test.Patient == p]
    P_test[p] = test.Percent.values[test.Patient == p]
    WEEK[p] = test.Weeks.values[test.Patient == p]

for k in sub.Patient_Week.values:
    p, w = k.split('_')
    w = int(w)

    fvc = A_test[p] * w + B_test[p]
    sub.loc[sub.Patient_Week == k, 'FVC'] = fvc
    sub.loc[sub.Patient_Week == k, 'Confidence'] = (
        P_test[p] - A_test[p] * abs(WEEK[p] - w)
)

sub.head()

sub[["Patient_Week","FVC","Confidence"]].to_csv("submission.csv", index=False)



