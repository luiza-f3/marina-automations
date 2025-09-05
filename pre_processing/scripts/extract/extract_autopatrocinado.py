import pandas as pd

cols = 'Participante SA', 'Data vencimento', 'Data credito', 'Data referencia', 'Tipo de contribuicao', 'Plano', 'Empregador', 'Perfil', 'Valor'

schema = {
    'Participante SA': pd.Int64Dtype(),
    'Data vencimento': str,
    'Data credito': str,
    'Data referencia': str,
    'Tipo de contribuicao': str,
    'Plano': str,
    'Empregador': str,
    'Perfil': str,
    'Valor': float
}

def extract_autopatrocinado(file_path):
    df = pd.read_excel(file_path)
    df.columns = cols
    df = df.astype(schema)

    df = df[df['Tipo de contribuicao'].str.contains('auto', regex=True, case=False)]
    df = df[df['Valor'] > 0]
    return df