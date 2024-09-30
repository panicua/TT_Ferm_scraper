import pandas as pd


def excel_to_df(excel_file):
    df = pd.read_excel(excel_file)
    return df


def df_to_list(df):
    return df.values.tolist()
