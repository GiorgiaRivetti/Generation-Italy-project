import pandas as pd
import numpy as np


class LocationStandardizer:
    def __init__(self, reference_df: pd.DataFrame):
        self.reference_df = reference_df

    def list_from_dataframe(self, original_column: pd.Series, column_1: str,
                            column_2: str) -> list:
        """
        Starting from the reference_df and its columns (column_1 and column_2) it creates a dict with column_1 as key and column_2 as value.
        Then compare the original_column with the keys of the dict and returns a list of the respective values

        :param original_column: column of the original dataframe used to map the final list
        :param reference_df: reference dataframe
        :param column_1: column name of the reference dataframe that gets compared with the original column
        :param column_2: column name of the reference dataframe whose values are used to get the result_column
        :return: a list of the resulting column
        """
        mapping_dict = self.reference_df.set_index(column_1)[column_2].to_dict()
        result_column = original_column.map(mapping_dict)
        result_column = result_column.where(original_column.notna(), np.nan)

        return result_column.to_list()
