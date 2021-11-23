import numpy as np
import pandas as pd
from scipy.stats import shapiro


class Data:
    def __init__(self, df, dataset_name, table_name) -> None:
        self.df = df
        self.dataset_name = dataset_name
        self.table_name = table_name
        print("FROM DATA CLASS:", df, dataset_name, table_name)

    def get_dataframe(self):
        df_rows = [
            self.get_row(self.df[col_name], self.dataset_name) for col_name in self.df
        ]

        print("FROM DATA CLASS ROWS:", df_rows)
        return pd.concat(df_rows, axis=0).reset_index(drop=True)

    def get_rows(self, column):

        try:
            col = column.sample(1000)
        except ValueError:
            col = column

        col_mean = np.nan
        col_median = np.nan
        col_std = np.nan
        wilk_test = np.nan
        col_skew = np.nan
        col_kurt = np.nan

        if col.dtype in [np.dtype("int"), np.dtype("float")]:
            col_mean = col.mean()
            col_std = col.std()
            col_median = col.median()
            # Normality when the p-value is greater than or equal to 0.05
            _, wilk_test = shapiro(col)
            col_skew = col.skew()
            col_kurt = col.kurt()

        rows = {
            "dataset_name": [self.dataset_name],
            "table_name": [self.table_name],
            "column_name": [column.name],
            "column_values": [", ".join(map(str, col.tolist()))],
            "column_values_unique": [col.unique()],
            "nunique_values": [col.nunique()],
            "mean": col_mean,
            "std": col_std,
            "median": col_median,
            "skew": col_skew,
            "kurt": col_kurt,
            "shapiro_wilk_test": [wilk_test],
            "label": [np.nan],
        }

        return pd.DataFrame.from_dict(rows)

    # Kaggle CSV -> DATA CLASS -> DF Containing ROWS
    # GBQ DF -> DATA CLASS -> DF Containing ROWS
