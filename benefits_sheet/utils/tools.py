import pandas as pd
from unidecode import unidecode

def normalize_text(df: pd.DataFrame(), colunas_list: list):
    """ Limpa Caracteres especiais, acentos e espaços """
    for coluna in colunas_list:
        df[coluna] = df[coluna].apply(lambda x: unidecode(x).replace(' ', '') if isinstance(x, str) else x)
    return df

def build_benefits_posting_dataframe(data, conta_contabil, valor, tipo_lancamento, descricao, cc, plano, perfil, patrocinadora):
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

def extract_rubric_amount(text):
    """Usado exclusivamente para extrair o valor de 'folha' no preprocessamento da folha de pagamento"""
    if not isinstance(text, str):
        return None

    first_hyphen = text.find('-')
    if first_hyphen == -1:
        return None

    second_hyphen = text.find('-', first_hyphen + 1)
    if second_hyphen == -1:
        return None

    remaining_text = text[second_hyphen + 1:].lstrip()

    space_index = remaining_text.find(' ')

    if space_index == -1:
        return remaining_text

    return remaining_text[:space_index]


def extract_payroll(text):
    # Usado exclusivamente para extrair o valor de 'folha' no preprocessamento da folha de pagamento

    if not isinstance(text, str):
        return None

    after_budget_index = text.lower().find('orç')

    if after_budget_index != -1:
        hyphen_count = 0
        second_hyphen_index = -1

        for i in range(after_budget_index - 1, -1, -1):
            if text[i] == '-':
                hyphen_count += 1
                if hyphen_count == 2:
                    second_hyphen_index = i
                    break

        if second_hyphen_index != -1:
            segment = text[second_hyphen_index + 1 : after_budget_index].strip()
            return segment.replace('-', '')

    last_space_index = text.rfind(' ')
    if last_space_index != -1:
        return ' '.join(text[last_space_index + 1:].strip().split())

    return text.strip()