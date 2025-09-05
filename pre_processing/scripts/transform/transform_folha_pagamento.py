import pandas as pd
import re
from unidecode import unidecode


def transform_folha_pagamento(df):
    df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))
    df = df.apply(lambda col: col.map(lambda x: re.sub(r'\s+', ' ', x.strip()) if isinstance(x, str) else x))
    df = df.applymap(lambda x: unidecode(x) if isinstance(x, str) else x)

    return df