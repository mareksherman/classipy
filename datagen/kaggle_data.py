from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import glob
import os
import shutil
from os.path import normpath, join, abspath, dirname

from datagen.data import Data


class KaggleDataset(Data):
    def __init__(self, n_datasets=100, max_size=25_000_000, max_rows=None, n_samples=1000, output_name="kaggle_data.csv") -> None:
        super().__init__(n_samples, max_rows, output_name)
        self.n_datasets = n_datasets
        self.dataset_names = []
        self.max_size = max_size
        self.max_rows = max_rows

        self.api = KaggleApi()
        self.api.authenticate()

        self.loc_temp_data = join(self.loc_data, 'temp_datasets')

    def get_dataset_names(self):
        dataset_names = []
        page = 4
        dataset_num = 0
        while dataset_num < self.n_datasets:
            try:
                resp = self.api.datasets_list(
                    page=page,
                    filetype="csv",
                    max_size=self.max_size
                )

                for i in range(20):  # TODO FIX THIS
                    dataset_names.append(
                        (resp[i]["id"], resp[i]["ref"], resp[i]["totalBytes"])
                    )
                    dataset_num += 1
                    if dataset_num >= self.n_datasets:
                        break
                page += 1

            except IndexError as e:
                break

        self.dataset_names = pd.DataFrame(
            dataset_names,
            columns=["id", "ref", "size"],
        )
        self.dataset_names.to_csv(join(self.loc_data, "name_data_sets.csv"))

    def download_datasets(self):
        if not self.dataset_names:
            self.get_dataset_names()

        all_dataframes = []

        for dataset_name in self.dataset_names["ref"]:
            self.api.dataset_download_files(
                dataset_name, self.loc_temp_data, unzip=True
            )

            dataset_file_names = self.read_filenames()
            dataset_dataframes = self.read_data_frame(
                dataset_file_names, dataset_name)
            all_dataframes += dataset_dataframes

            # print('Clean-up | ', dataset_name)
            self.clean_tempfolder()

        df_all = pd.concat(all_dataframes, axis=0).reset_index(
            drop=True)[:self.max_rows]
        df_all.to_csv(
            join(self.loc_data, self.output_name), index=False)

        print(
            f'Completed Creating Dataset | Saved @ {join(self.loc_data,self.output_name)}')

        return df_all

    def read_filenames(self):
        return [
            name
            for name in
            glob.glob(self.loc_temp_data + "/**/*.csv", recursive=True)]

    def clean_tempfolder(self):
        for file in glob.glob(self.loc_temp_data+"/*"):
            try:
                os.remove(file)
            except OSError:
                shutil.rmtree(file, ignore_errors=True)

    def read_data_frame(self, file_names, dataset_name):
        count_passes = 0
        data_frames = []
        for file_name in file_names:
            *_, table_name = file_name.rpartition('/')

            try:
                df = pd.read_csv(file_name)
                df_calc = self.get_dataframe(
                    df, dataset_name, table_name)
            except Exception as e:
                count_passes += 1
                print('ERROR: SKIPPING CSV:', dataset_name, table_name, type(e))
                df_calc = pd.DataFrame()
            finally:
                data_frames.append(df_calc)

            print(f'Completed :', {dataset_name}, {table_name})

        return data_frames


if __name__ == "__main__":
    k = KaggleDataset(4)
    k.download_datasets()
    print('DONE!!')
    pass
