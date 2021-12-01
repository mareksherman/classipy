from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin


class JSONtoModelTransformer(BaseEstimator, TransformerMixin):
    required_columns = [
        'n_unique_values', 'n_values', 'mean',
        'std', 'median', 'skew', 'kurt', 'shapiro_wilk_test'
    ]

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = X.copy()
        X = self.remove_nans(X)
        X = X[self.required_columns]
        X = MinMaxScaler().fit_transform(X)
        return pd.DataFrame(X, columns=self.required_columns)

    def remove_nans(self, X):
        X = X.fillna(0).replace(np.inf, 0).replace(-np.inf, 0)
        X.loc[X['mean'].astype(str).str.contains(':', na=False), 'mean'] = 0
        return X
