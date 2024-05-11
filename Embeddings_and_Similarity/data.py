import csv

import pandas as pd


class Data:
    @staticmethod
    def load_dataframe(path):
        df = pd.read_csv(path)
        return df

    @staticmethod
    def save_dataframe(dataframe, path_output):
        dataframe.to_csv(path_output, index=False, quoting=csv.QUOTE_ALL, errors='ignore')

    @staticmethod
    def create_dataframe(data):
        dataframe = pd.DataFrame(data)
        return dataframe

    @staticmethod
    def get_dict_list(dataframe):
        dict_list = []
        columns = dataframe.columns.tolist()
        for i in range(len(dataframe)):
            cur_dict = {}
            for j in range(len(columns)):
                cur_dict[columns[j]] = str(dataframe.iloc[i][columns[j]])
            dict_list.append(cur_dict)
        return dict_list
