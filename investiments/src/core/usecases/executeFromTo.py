'''
from investiments.src.utils.consultas.rename_data import rename_datas

def executeFromTo(df, field_rename):
    """Usada para aplciar um dicionario de depara com propósito de diminuir erros"""
    if field_rename in df.columns:
        df[field_rename] = df[field_rename].replace(rename_datas, regex=True)
        return df
    else:
        print(f"A coluna '{field_rename}' não existe no DataFrame!")
'''

from investiments.src.utils.consultas.rename_data import rename_datas

def executeFromTo(df, field_rename, df_consulta):
    """Usada para aplciar um dicionario de depara com propósito de diminuir erros"""
    if field_rename in df.columns:
        df[field_rename] = df[field_rename].replace(df_consulta, regex=True)
        return df
    else:
        print(f"A coluna '{field_rename}' não existe no DataFrame!")