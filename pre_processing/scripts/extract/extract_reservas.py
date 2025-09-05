import pandas as pd
from unidecode import unidecode

cols = 'Data', 'Empregador','Razao social', 'Cod cont', 'Nome do plano', 'Perfil', 'Nome do perfil', 'Conta contabil', 'Nome da conta', 'Tipo da conta', 'Tipo da operacao', 'Data da Cota', 'Valor da moeda', 'Valor da cota', 'Ordem'

def extract_reservas(file_path):
    df = pd.read_excel(file_path)
    df.columns = cols

    df = df.loc[~df["Tipo da conta"].isin(["SALDO DO MÊS ANTERIOR", "SALDO DO MÊS ATUAL"])]
    df["Nome da conta"] = df["Nome da conta"].apply(unidecode)
    df['Tipo da conta'] = df['Tipo da conta'].apply(unidecode)
    df['Tipo da operacao'] = df['Tipo da operacao'].apply(unidecode)
    df["Nome do plano"] = df["Nome do plano"].apply(unidecode)

    df.drop('Conta contabil', axis=1, inplace=True)
    return df