import pandas as pd

cols = "Tipo de folha", "Data de pagamento","Plano","Empregador","Perfil","Grupo de beneficio","Tipo de beneficio","Item folha","Valor"
schema = {
    "Tipo de folha": str,
    "Data de pagamento": 'datetime64[ns]',
    "Plano": str,
    "Empregador": str,
    "Perfil": pd.StringDtype(),
    "Grupo de beneficio": str,
    "Tipo de beneficio": str,
    "Item folha": str,
    "Valor": float
}

def extract_folha_beneficios(file_path):
    df = pd.read_excel(file_path, skiprows=5)
    df.columns = cols

    colunas = ['Empregador', 'Perfil', 'Plano']

    # Remove linhas onde alguma dessas colunas seja NaN ou string vazia
    df = df.dropna(subset=colunas)  # Remove NaN
    df = df[~df[colunas].apply(lambda row: row.astype(str).str.strip().eq('').any(), axis=1)]

    df["Data de pagamento"] = df["Data de pagamento"].apply(ajustar_datas)
    df = df.astype(schema)

    return df

def ajustar_datas(data):
    try:
        return pd.to_datetime(data, dayfirst=True)
    except:
        return pd.NaT