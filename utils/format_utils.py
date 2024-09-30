import pandas as pd


def excel_to_df(excel_file):
    df = pd.read_excel(excel_file)
    return df


def df_to_list(df):
    return df.values.tolist()

# print(excel_to_df("../посилання для скачування 1.xlsx")["Ссылки"])
# print(df_to_list(excel_to_df("../посилання для скачування 1.xlsx")["Ссылки"]))
