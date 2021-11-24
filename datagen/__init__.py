from datagen.kaggle_data import KaggleDataset
from datagen.gbq_data import GBQDataset
import pandas as pd
import os


def create_dataset(n_kaggle_datasets=100, n_gbq_datasets=20, output_name='combined_data.csv'):
    k = KaggleDataset(n_datasets=n_kaggle_datasets)
    g = GBQDataset(n_datasets=n_gbq_datasets)

    data_loc = k.loc_data

    df_gbq = k.download_datasets()
    df_kaggle = g.download_datasets()

    # df_gbq = pd.read_csv(os.path.join(data_loc, 'gbq_data.csv'))
    # df_kaggle = pd.read_csv(os.path.join(data_loc, 'kaggle_data.csv'))

    df = pd.concat([df_gbq, df_kaggle], axis=0).reset_index(drop=True)
    file_path = os.path.join(data_loc, output_name)
    df.to_csv(file_path, index=False)
    print(
        f'Completed Creating Dataset | Saved @ {file_path}')


if __name__ == '__main__':
    print('Hello World')
