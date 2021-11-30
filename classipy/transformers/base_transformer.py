import numpy as np
import pandas as pd
from scipy.stats import shapiro
from sklearn.base import TransformerMixin, BaseEstimator


class DataFrameTransformer(TransformerMixin, BaseEstimator):
    def __init__(self, dataset_name, table_name, n_samples=1000):
        self.n_samples = n_samples
        self.dataset_name = dataset_name
        self.table_name = table_name

    def fit(self, x, y=None):
        print('fit called')
        return self

    def transform(self, x, y=None):
        print('transform called')
        return self.get_dataframe(x, self.dataset_name, self.table_name)

    def get_dataframe(self, df, dataset_name, table_name):

        print(f'Processing DataFrame: {dataset_name} {table_name}')
        df_rows = [
            self.get_row(df[col_name]) for col_name in df
        ]
        return pd.concat(df_rows, axis=0).reset_index(drop=True)

    def get_row(self, column):
        try:
            col = column.sample(self.n_samples)
        except ValueError:
            col = column

        features = {
            "dataset_name": [self.dataset_name],
            "table_name": [self.table_name],
            "column_name": [column.name],
            # "label": [np.nan],
        }

        feature_functions = {
            "column_values": lambda x: ", ".join(map(str, x.tolist())),
            "column_values_unique": lambda x: x.unique(),
            "n_unique_values": lambda x: x.nunique(),
            "unique_value_counts": lambda x: {val: freq for val, freq in x.value_counts().items()},
            'n_values': lambda x: x.shape[0],
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

            # THIS PUTS ZEROS INSTEAD OF NANS
            finally:
                if val is None or val is np.nan or val is np.inf:
                    val = 0
            features[col_name] = [val]

        return pd.DataFrame.from_dict(features)
