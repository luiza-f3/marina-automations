from investiments.src.utils.mappings.rename_data import fund_name_mapping

def replace_column_values(df, column):
    """
    Aplica mapeamento de valores em uma coluna do DataFrame.

    Args:
        df (DataFrame): DataFrame de entrada
        column (str): Nome da coluna

    Returns:
        DataFrame: DataFrame com valores substituídos

    Raises:
        ValueError: Se a coluna não existir
    """

    if column not in df.columns:
        raise ValueError(f"A coluna '{column}' não existe no DataFrame.")

    df = df.copy()
    df[column] = df[column].replace(fund_name_mapping, regex=True)

    return df