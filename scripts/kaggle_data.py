from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import glob
import os
from data import Data


class KaggleDataset(Data):
    def __init__(self, n_datasets) -> None:
        self.n_datasets = n_datasets
        self.api = KaggleApi()
        self.api.authenticate()
        pass

    def get_data_set_names(self):
        data_set_names = []
        page = 4
        dataset_num = 0
        while True:
            if dataset_num >= self.n_datasets:
                break

            try:
                resp = self.api.datasets_list(
                    page=page, filetype="csv", max_size=25_000_000
                )
                for i in range(20):  # TODO FIX THIS
                    data_set_names.append(
                        (resp[i]["id"], resp[i]["ref"], resp[i]["totalBytes"])
                    )
                    dataset_num +=1
                page += 1

            except IndexError as e:
                break

        self.data_set_names = pd.DataFrame(
            data_set_names,
            index=range(len(data_set_names)),
            columns=["id", "ref", "size"],
        )

        self.data_set_names.to_csv("../raw_data/name_data_sets.csv")

    def download_data_sets(self):
        data = self.data_set_names["ref"]
        df_all_data = pd.DataFrame()

        for dataset_name in data:
            self.api.dataset_download_files(
                dataset_name, "../raw_data/temp_datasets/", unzip=True
            )

            file_names = self.read_filenames()  # CUSTOM FUNCTION

            df = self.read_data_frame(file_names, dataset_name)  # CUSTOM FUNCTION

            df_all_data = pd.concat([df_all_data, df])

            #for file in glob.glob("../raw_data/temp_datasets/*"):
            #    os.remove(file)

        df_all_data.to_csv("../raw_data/data.csv")


    def read_filenames(self):
        file_names = []
        for name in glob.glob("../raw_data/temp_datasets/*.csv"):
            file_names.append(name)
        return file_names


    def read_data_frame(self, file_names, dataset_name):
        count_passes = 0
        for file in file_names:
            try:
                df = pd.read_csv(file)               
                d = Data(df, dataset_name, file)
                df_calc = d.get_dataframe()
                print(df_calc)

            except:
                count_passes += 1
                df_calc = pd.DataFrame()
                pass
        return df_calc


# def encoding_det(file):
#     rawdata = open(file, "r").read()
#     result = chardet.detect(rawdata)
#     charenc = result["encoding"]
#     print(charenc)


if __name__ == "__main__":
    # file_names = read_filenames()
    # read_data_frame(file_names,'this_is_a_test')
    # download_data_sets()
    k = KaggleDataset(40)
    k.get_data_set_names()
    k.download_data_sets()
    pass
