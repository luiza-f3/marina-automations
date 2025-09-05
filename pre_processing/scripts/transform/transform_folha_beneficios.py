import pandas as pd
import re
from unidecode import unidecode

from pre_processing.utils.benefits.portfolio_dictionary import portfolio_dictionary

plano = {
    "TELEFÔNICA BD": 22,
    "MAIS VISAO": 52,
    "PREVISAO": 51,
    "VISAO MULTI": 8,
    "VISAO TELEFÔNICA": 49
}

def transform_folha_beneficios(data):
    # remover espaços extras
    df = data.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))
    df = data.apply(lambda col: col.map(lambda x: re.sub(r'\s+', ' ', x.strip()) if isinstance(x, str) else x))

    df["Tipo de folha"] = df["Tipo de folha"].apply(lambda x: unidecode(x).replace(' ', ''))
    df["Grupo de beneficio"] = df["Grupo de beneficio"].apply(lambda x: unidecode(x).replace(' ', ''))
    df["Tipo de beneficio"] = df["Tipo de beneficio"].apply(lambda x: unidecode(x).replace(' ', ''))
    df["Item folha"] = df["Item folha"].apply(lambda x: unidecode(x).replace(' ', ''))
    df["Empregador"] = df["Empregador"].apply(lambda x: unidecode(x).replace(' ', ''))

    df["Plano"] = df["Plano"].map(lambda x: plano[x] if x in plano else "Sem plano")
    df["Patrocinadora"] = df["Empregador"].map(lambda x: portfolio_dictionary[x] if x in portfolio_dictionary else "Sem portfolio")
    df["Perfil"] = df["Perfil"].map(lambda x: int(re.sub(r"\D", "", x)) if isinstance(x, str) else x)
    return df