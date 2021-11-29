import pandas as pd
import numpy as np
from scipy.stats import shapiro
from os.path import normpath, join, abspath, dirname

from datagen.data import Data


class GBQDataset(Data):
    def __init__(self, n_datasets=None, n_samples=1000, max_rows=None, output_name="gbq_data.json", project_id=None) -> None:
        super().__init__(n_samples, max_rows, output_name)
        self.n_datasets = n_datasets
        self.end_points = []
        self.project_id = project_id
        pass

    def get_queryendpoints(self):
        self.end_points = []
        with open(join(dirname(__file__), 'gbq_endpoints.txt'), 'r', encoding='utf-8') as file:
            for line in file:
                endpoint = line.strip('\n')
                dataset_name, _, table_name = endpoint.partition(':')

                self.end_points.append(
                    {
                        'api': endpoint,
                        'dataset_name': dataset_name,
                        'table_name': table_name
                    }
                )
        pass

    def download_datasets(self):
        if not self.end_points:
            self.get_queryendpoints()

        data_frames = []
        # TODO: REMOVE LIMIT AFTER TESTING
        for endpoint in self.end_points[:self.n_datasets]:

            api, dataset_name, table_name = endpoint.values()
            print(f'Fetching :', {dataset_name}, {table_name})

            try:
                # query = f"SELECT * FROM {dataset_name}.{table_name}"
                query = f"""
                SELECT * FROM {dataset_name}.{table_name}
                ORDER BY RAND()
                LIMIT {self.n_samples}
                """
                df = pd.read_gbq(query, project_id=self.project_id)
                df_calc = self.get_dataframe(
                    df, dataset_name, table_name)
            except Exception as e:
                print(
                    f'ERROR: {dataset_name}, {table_name}, {type(e)} \n SKIPPING')
                df_calc = pd.DataFrame()
            else:
                print(f'Completed :', {dataset_name}, {table_name})
            finally:
                data_frames.append(df_calc)

            df_all = pd.concat(data_frames, axis=0).reset_index(
                drop=True)[:self.max_rows]
            df_all.to_json(
                join(self.loc_data, self.output_name))

        print(
            f'Completed Creating Dataset | Saved @ {join(self.loc_data,self.output_name)}')

        return df_all


if __name__ == '__main__':
    d = GBQDataset(1)
    d.download_datasets()