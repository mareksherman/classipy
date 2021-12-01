import pandas as pd
import re
import math
import ast
import numpy as np


class Heuristic ():

    def __init__(self) -> None:
        pass

    def fill_nan_none(self,df):
        for index,row in df.iterrows():
            for col in ['mean','std','median','skew','kurt','shapiro_wilk_test']:
                if row[col] == None:
                    df.loc[index, col] = np.nan
        return df

    def check_cat_binary(self,df):
        df['heuristic_label'] = np.nan
        for index,row in df.iterrows():
            if row['n_unique_values'] == 2:
                list_n_uniques = ast.literal_eval(row.column_values_unique)
                if all(isinstance(item, int) for item in list_n_uniques):
                    test_bin_num = set(list_n_uniques)
                    if set([0, 1]).issubset(test_bin_num):
                        df.loc[index,'heuristic_label'] = 6
                else:
                    df.loc[index,'heuristic_label'] = 6
        return df

    def check_date(self,df):
        pattern = r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))|((0?[13578]|10|12)(-|\/)(([1-9])|(0[1-9])|([12])([0-9]?)|(3[01]?))(-|\/)((19)([2-9])(\d{1})|(20)([01])(\d{1})|([8901])(\d{1}))|(0?[2469]|11)(-|\/)(([1-9])|(0[1-9])|([12])([0-9]?)|(3[0]?))(-|\/)((19)([2-9])(\d{1})|(20)([01])(\d{1})|([8901])(\d{1})))'
        for index,row in df.loc[df.heuristic_label.isnull()].iterrows():
            if 'date' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 5
            elif 'period' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 5
            elif 'year' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 5
            elif re.search(pattern,str(row.column_values_unique)):
                df.loc[index,'heuristic_label'] = 5
        return df


    def check_cat_multi(self,df):
        for index,row in df.loc[df.heuristic_label.isnull()].iterrows():
            if 'province' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 2
            elif 'region' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 2
            elif 'country' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 2
            elif 'category' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 2
            elif 'state' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 2
            elif 'city' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 2
            elif 'day' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 2
            elif 'week' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 2
            elif 'location' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 2
            elif (row.n_unique_values/row.n_values) < 0.05 and row.n_unique_values < 10:
                df.loc[index,'heuristic_label'] = 2
        return df


    def check_text(self,df):
        for col in df.columns:
            print(col)
        for index,row in df.loc[df.heuristic_label.isnull()].iterrows():
            if math.isnan(row['mean']) and math.isnan(row['std']) and math.isnan(row['median']) and math.isnan(row['skew']) and math.isnan(row['kurt']) and (row.n_unique_values/row.n_values) > 0.8 :
                df.loc[index,'heuristic_label'] = 4
        return df


    def check_int_float(self,df):
        for col in df.columns:
            print(col)
        for index,row in df.loc[df.heuristic_label.isnull()].iterrows():
            if math.isnan(row['mean'])==False and math.isnan(row['std'])==False and math.isnan(row['median'])==False and math.isnan(row['skew'])==False and math.isnan(row['kurt'])==False and (row.n_unique_values/row.n_values) > 0.8:
                list_n_uniques = ast.literal_eval(row.column_values_unique)
                if all(isinstance(item, int) for item in list_n_uniques):
                    df.loc[index,'heuristic_label'] = 0
                elif all(isinstance(item, float) for item in list_n_uniques):
                    df.loc[index,'heuristic_label'] = 1
        return df


    def test_dataset_heuristic(self,df):
        df = self.fill_nan_none(df)
        df = self.check_cat_binary(df)
        df = self.check_date(df)
        df = self.check_cat_multi(df)
        df= self.check_text(df)
        df= self.check_int_float(df)
        df.loc[df.heuristic_label.isnull()] = 3
        #df = df_bin.append([df_cat_multi,df_text,df_int_float,df],ignore_index=True)
        return df.heuristic_label

if __name__ == '__main__':
    df = pd.read_csv('../../raw_data/kaggle_data_merged_with_labels.csv')
    print(df.shape)
    heuristic = Heuristic()
    df = heuristic.test_dataset_heuristic(df)
    print(df.shape)
    print(df)
