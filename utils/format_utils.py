import pandas as pd


def excel_to_df(excel_file_name: str) -> pd.DataFrame:
    """
    Reads an Excel file into a pandas DataFrame

    Args: excel_file (str): The path to the Excel file

    Returns: pandas.DataFrame
    """
    df = pd.read_excel(excel_file_name)
    return df


def df_to_list(df: pd.DataFrame) -> list[str]:
    """
    Converts a pandas DataFrame into a list of lists

    Args: df (pandas.DataFrame): The DataFrame to convert

    Returns: list[str]
    """
    return df.values.tolist()
