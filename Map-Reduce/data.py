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
