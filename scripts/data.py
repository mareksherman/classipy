from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
from pandas.core.base import DataError
import glob
import chardet
import os

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
    data = data.head(50)
    df_all_data = pd.DataFrame()
    for dataset_name in data:
        print('Downloading')
        api.dataset_download_files(dataset_name,'../raw_data/temp_datasets/',unzip=True)
        print('Downlaoding done')
        file_names = read_filenames()
        print('Create Data Frame')
        df = read_data_frame(file_names,dataset_name)
        print(df.head())
        df_all_data =  pd.concat([df_all_data,df])
        print(df_all_data.shape)
        for file in glob.glob('../raw_data/temp_datasets/*'):
            print(file)
            os.remove(file)
    df_all_data.to_csv('../raw_data/data.csv')


def read_filenames():
    file_names = []
    for name in glob.glob('../raw_data/temp_datasets/*.csv'):
        file_names.append(name)
        #encoding_det(name)
    return file_names

def read_data_frame(file_names,dataset_name):
    count_passes = 0
    for file in file_names:
        try:
            df = pd.read_csv(file)
            df_calc = calulate(df,file,dataset_name)
        except:
            count_passes += 1
            df_calc = pd.DataFrame()
            pass
    print(f'Passes count:{count_passes}')
    return df_calc


def calulate(data_frame,file,dataset_name):
    column_names = data_frame.columns
    df_all_rows = pd.DataFrame()
    df = pd.DataFrame()
    for column in column_names:
        df['dataset_name'] = dataset_name
        df['csv_file_name'] = file[26:]
        df['column_name'] = column
        df['column_values'] = [data_frame[column].unique()]
        df['n_unique_values'] = data_frame[column].nunique()
        try:
            df['mean'] = data_frame[column].mean()
            df['std'] = data_frame[column].std()
            df['median'] = data_frame[column].median()
            df['skew'] = data_frame[column].skew()
            df['kurt'] = data_frame[column].kurt()
        except:
            df['mean'] = None
            df['std'] = None
            df['median'] = None
            df['skew'] = None
            df['kurt'] = None
        df_all_rows =  pd.concat([df_all_rows,df])
    return df_all_rows

def encoding_det(file):
    rawdata = open(file, "r").read()
    result = chardet.detect(rawdata)
    charenc = result['encoding']
    print(charenc)

#file_names = read_filenames()
#read_data_frame(file_names,'this_is_a_test')
download_data_sets()
