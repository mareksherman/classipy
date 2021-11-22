import re
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
from pandas.core.base import DataError
import glob

from pandas.io.parsers import read_csv
api = KaggleApi()
api.authenticate()

def get_data_set_names():
    data_set_names = []
    run = True
    page = 4
    while run == True:
        try:
            resp = api.datasets_list(page=page,filetype='csv',)
            print(page)
            for i in range(20):
                data_set_names.append((resp[i]['id'],resp[i]['ref'],resp[i]['totalBytes']))
            page += 1
        except IndexError as e:
            print('Index Error')
            run = False
    data_set_names = pd.DataFrame(
                                data_set_names,
                                index=range(len(data_set_names)),
                                columns=['id', 'ref', 'size'])
    data_set_names.to_csv('../raw_data/name_data_sets.csv')

def download_data_sets():
    data = pd.read_csv('../raw_data/name_data_sets.csv')
    data = data["ref"]
    data = data.head(5)
    #print(data)

    for i in data:
        print(i)
        api.dataset_download_files(i,'../raw_data/temp_datasets/',unzip=True)

def read_fileames():
    file_names = []
    for name in glob.glob('../raw_data/temp_datasets/*.csv'):
       file_names.append(name)

    return file_names

def read_data_frame(file_names):
    count_passes = 0
    for file in file_names:
        print(file)
        try:
            df = pd.read_csv(file)
            calulate(df)
        except:
            count_passes += 1
            pass
    print(count_passes)

def calulate(data_frame):
    column_names = data_frame.columns
    for column in column_names:
        #if column to datetime
        #if column or int
        #else pass
        print(data_frame[column])

#get_data_set_names()
#download_data_sets()

file_names = read_fileames()
#print(file_names)
read_data_frame(file_names)

#pd.read_csv('../raw_data/temp_datasets/cwurData.csv')
