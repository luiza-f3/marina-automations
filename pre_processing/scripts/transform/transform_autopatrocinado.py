import pandas as pd

patroc_code = {
    "001": "Patrocinadoras", # código universal
    "002": "FIBRASIL",
    "003": "FUNDACAO TELEFONICA",
    "004": "SP TELECOMUNICACOES",
    "005": "TELEFONICA BRASIL",
    "006": "CIBER",
    "007": "CLOUD",
    "008": "TCS",
    "009": "TGS",
    "010": "TIS",
    "011": "IOT",
    "012": "TELEF ON THE SPOT SOL DIGIT BR LTDA",
    "013": "TELEF SERV EMPR DO BR LTDA",
    "014": "TLOG",
    "015": "TELXIUS CABLE",
    "016": "TERRA NETWORKS",
    "017": "VISAO PREV",
    "018": "VITA IT",
    "019": "MAIS VISAO"
}

plano_perfil = [{
    "Mais Visao": {"Agressivo": 36, "Agressivo RF LP": 35, "Conservador": 33, "Moderado": 34,  "Super Conser": 36},
    "Telefônica BD":{ "Telefônica BD": 3},
    "Visao Multi": {"Agressivo": 26, "Agressivo RF LP": 25, "Conservador": 23, "Moderado": 24,  "Super Conser": 22},
    "Visao Telefônica": {"Agressivo": 31, "Agressivo RF LP": 30, "Conservador": 28, "Moderado": 29,  "Super Conser": 27}
}]
planos = {
    'Mais Visao': 52,
    'Telefônica BD': 3,
    'Visao Multi': 8,
    'Visao Telefônica': 49
}

def transform_autopatrocinado(df):
    df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))
    df['Tipo de contribuicao'] = df['Tipo de contribuicao'].apply(lambda x: x.replace(':', '') if ':' in x else x)

    for row_index, row in df.iterrows():
        for plano_dict in plano_perfil:
            if row['Plano'] in plano_dict:
                df.at[row_index, 'Perfil'] = plano_dict[row['Plano']][row['Perfil']]
                break

    for index, row in df.iterrows():
        df.at[index, 'Plano'] = planos[row['Plano']]

    df['Patroc Cred'] = df["Empregador"].map(lambda x: next((key for key, value in patroc_code.items() if x in value), "001") if isinstance(x, str) else "001")
    df = df.drop_duplicates(keep="first")
    return df