import numpy as np
import pandas as pd
from scipy.stats import shapiro


class Data:
    def __init__(self, df, dataset_name, table_name) -> None:
        self.df = df
        self.dataset_name = dataset_name
        self.table_name = table_name

    def get_dataframe(self):
        df_rows = [
            self.get_row(self.df[col_name]) for col_name in self.df
        ]
        return pd.concat(df_rows, axis=0).reset_index(drop=True)

    def get_row(self, column):
        try:
            col = column.sample(1000)
        except ValueError:
            col = column

        features = {
            "dataset_name": [self.dataset_name],
            "table_name": [self.table_name],
            "column_name": [column.name],
            "label": [np.nan],
        }

        feature_functions = {
            "column_values": lambda x: [", ".join(map(str, col.tolist()))],
            "column_values_unique": lambda x: x.unique(),
            "nunique_values": lambda x: x.nunique(),
            "mean": lambda x: x.mean(),
            "std": lambda x: x.std(),
            "median": lambda x: x.median(),
            "skew": lambda x: x.skew(),
            "kurt": lambda x: x.kurt(),
            "shapiro_wilk_test": lambda x: shapiro(x)[1],
        }

        for col_name, fn in feature_functions.items():
            try:
                val = fn(col)
            except (ValueError, TypeError):
                val = np.nan
            except Exception as e:  # DEBUGGING TYPES OF ERRORS
                val = np.nan
                print(features['column_name'], col_name, 'Exception:', type(e))

            features[col_name] = [val]

        return pd.DataFrame.from_dict(features)
