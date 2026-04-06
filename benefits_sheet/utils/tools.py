import pandas as pd
from unidecode import unidecode

def limparTexto(df: pd.DataFrame(), colunas_list: list):
    """Ferramenta para limpar caracteres especiais, acentos e espaços"""
    for coluna in colunas_list:
        df[coluna] = df[coluna].apply(lambda x: unidecode(x).replace(' ', '') if isinstance(x, str) else x)
    return df

def layoutLancamentoBeneficios(data, conta_contabil, valor, tipo_lancamento, descricao, cc, plano, perfil, patrocinadora):
    """Retorna um DataFrame para o lançamento"""
    return pd.DataFrame({
        'Data': [data],
        'Conta contabil': [conta_contabil],
        'Valor': [valor],
        'D/C': [tipo_lancamento],
        'Descricao': [descricao],
        'CC': [cc],
        'Plano': [plano],
        'Perfil': [perfil],
        'Patrocinadora': [patrocinadora]
    })

def extrair_rubrica(texto):
    """Usado exclusivamente para extrair o valor de 'folha' no preprocessamento da folha de pagamento"""
    if not isinstance(texto, str):
        return None

    primeira = texto.find('-')
    if primeira == -1:
        return None

    segunda = texto.find('-', primeira + 1)
    if segunda == -1:
        return None

    restante = texto[segunda + 1:].lstrip()

    espaco = restante.find(' ')

    if espaco == -1:
        return restante
    return restante[:espaco]


def extrair_folha(texto):
    if not isinstance(texto, str):
        return None

    pos_orc = texto.lower().find('orç')

    if pos_orc != -1:
        contador_hifen = 0
        index_segundo_hifen = -1

        for i in range(pos_orc - 1, -1, -1):
            if texto[i] == '-':
                contador_hifen += 1
                if contador_hifen == 2:
                    index_segundo_hifen = i
                    break

        if index_segundo_hifen != -1:
            trecho = texto[index_segundo_hifen + 1:pos_orc].strip()
            return trecho.replace('-', '')

    ultimo_espaco = texto.rfind(' ')
    if ultimo_espaco != -1:
        return ' '.join(texto[ultimo_espaco + 1:].strip().split())

    return texto.strip()
