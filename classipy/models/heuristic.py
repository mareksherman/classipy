import pandas as pd
import re
import math
import ast

class Heuristic ():

    def __init__(self) -> None:
        pass

    
    def check_cat_binary(self,df):
        for index,row in df.iterrows():
            if row['n_unique_values'] == 2:
                list_n_uniques = ast.literal_eval(row.column_values_unique)
                if all(isinstance(item, int) for item in list_n_uniques):
                    test_bin_num = set(list_n_uniques)
                    if set([0, 1]).issubset(test_bin_num):
                        df.loc[index,'heuristic_label'] = 'cat-binary'
                else:
                    df.loc[index,'heuristic_label'] = 'cat-binary'
        df_bin = df.loc[df.heuristic_label == 'cat-binary']
        df = df.loc[df.heuristic_label.isnull()]
        return df,df_bin

    def check_date(self,df):
        pattern = r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))|((0?[13578]|10|12)(-|\/)(([1-9])|(0[1-9])|([12])([0-9]?)|(3[01]?))(-|\/)((19)([2-9])(\d{1})|(20)([01])(\d{1})|([8901])(\d{1}))|(0?[2469]|11)(-|\/)(([1-9])|(0[1-9])|([12])([0-9]?)|(3[0]?))(-|\/)((19)([2-9])(\d{1})|(20)([01])(\d{1})|([8901])(\d{1})))'
        for index,row in df.iterrows():
            if 'date' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 'date'
            elif 'period' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 'date'
            elif 'year' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 'date'
            elif re.search(pattern,str(row.column_values_unique)):
                df.loc[index,'heuristic_label'] = 'date'
        df_date = df.loc[df.heuristic_label == 'date']
        df = df.loc[df.heuristic_label.isnull()]
        return df,df_date


    def check_cat_multi(self,df):
        for index,row in df.iterrows():
            if 'province' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 'cat-multi'
            elif 'region' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 'cat-multi'  
            elif 'country' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 'cat-multi'
            elif 'category' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 'cat-multi'
            elif 'state' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 'cat-multi'
            elif 'city' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 'cat-multi'
            elif 'day' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 'cat-multi'
            elif 'week' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 'cat-multi'
            elif 'location' in row['column_name'].lower():
                df.loc[index,'heuristic_label'] = 'cat-multi'
            elif (row.n_unique_values/row.n_values) < 0.05 and row.n_unique_values < 10:
                df.loc[index,'heuristic_label'] = 'cat-multi'
        df_cat_multi = df.loc[df.heuristic_label == 'cat-multi']
        df = df.loc[df.heuristic_label.isnull()]
        return df,df_cat_multi

    
    def check_text(self,df):
        for index,row in df.iterrows():
            if math.isnan(row['mean']) and math.isnan(row['std']) and math.isnan(row['median']) and math.isnan(row['skew']) and math.isnan(row['kurt']) and (row.n_unique_values/row.n_values) > 0.8 :
                df.loc[index,'heuristic_label'] = 'text'
        df_text = df.loc[df.heuristic_label == 'text']
        df = df.loc[df.heuristic_label.isnull()]
        return df,df_text


    def check_int_float(self,df):
        for index,row in df.iterrows():
            if math.isnan(row['mean'])==False and math.isnan(row['std'])==False and math.isnan(row['median'])==False and math.isnan(row['skew'])==False and math.isnan(row['kurt'])==False and (row.n_unique_values/row.n_values) > 0.8:
                list_n_uniques = ast.literal_eval(row.column_values_unique)
                if all(isinstance(item, int) for item in list_n_uniques):
                    df.loc[index,'heuristic_label'] = 'int'
                elif all(isinstance(item, float) for item in list_n_uniques):
                    df.loc[index,'heuristic_label'] = 'float'
        df_int_float = df.loc[(df.heuristic_label == 'int')|(df.heuristic_label == 'float')]
        df = df.loc[df.heuristic_label.isnull()]
        return df,df_int_float

    
    def test_dataset_heuristic(self,df):
            df, df_bin = self.check_cat_binary(df)
            df, df_date = self.check_date(df)
            df, df_cat_multi = self.check_cat_multi(df)
            df,df_text = self.check_text(df)
            df,df_int_float = self.check_int_float(df)
            df.heuristic_label = 'other'
            df = df_bin.append([df_date,df_cat_multi,df_text,df_int_float,df],ignore_index=True)
            return df.heuristic_label

if __name__ == '__main__':
    df = pd.read_csv('../raw_data/kaggle_data_merged_with_labels.csv')
    print(df.shape)
    heuristic = Heuristic()
    df = heuristic.test_dataset_heuristic(df)
    print(df.shape)
    print(df)

    

