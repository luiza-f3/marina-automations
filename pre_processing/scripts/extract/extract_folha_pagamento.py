import pandas as pd

from benefits_sheet.utils.tools import extrair_folha, extrair_rubrica

cols = ['DataEmissao', 'DataApropriacao', 'DataVencimento', 'Rubrica', 'Folha', 'ValorLiquido']
schema = {
    "DataEmissao": str,
    "DataApropriacao": str,
    "DataVencimento": str,
    "Rubrica": int,
    "Folha": str,
    "ValorLiquido": float
}

def extract_folha_pagamento(file_path):
    df = pd.read_excel(file_path) #encoding="ISO-8859-1"
    df.columns = df.columns.map(lambda x: x.replace(' ', '')) # retirando espaços vazios

#    df['ValorLiquido'] = df['ValorLiquido'].apply(
#        lambda x: float(str(x).replace(',', '.')) if isinstance(x, str) and x.replace(',', '').replace('.', '').replace(
#            '-', '').isdigit() else None)

    df['Folha'] = df['Historico'].apply(extrair_folha)
    df['Rubrica'] = df['Historico'].apply(extrair_rubrica)

    df = df[cols]
    df = df.astype(schema)
    return df