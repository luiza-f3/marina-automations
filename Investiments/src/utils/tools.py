from unidecode import unidecode
from dotenv import load_dotenv
import os
import pandas as pd
import re

load_dotenv()
base_path = os.path.expanduser(os.getenv("BASE_PATH"))
consulta_fundos = os.getenv('CONSULTA_FUNDOS').replace('/', '\\')
query_path = os.path.join(base_path, consulta_fundos)
query_path = os.path.normpath(query_path)
funds_df = pd.read_excel(query_path, sheet_name='para')


##### 1. CONFIGURATION AND SETUP FUNCTIONS
def define_profile_plan(df, key, query_sheet):
    """
Define plano e perfil com base em uma chave e planilha de consulta.

Args:
    df (DataFrame): Dados a serem atualizados
    key (str): Chave de busca
    query_sheet (list): Fonte com plano e perfil

Returns:
    DataFrame ou None
    """

    index = next((i for i, row in enumerate(query_sheet) if row[0] == key), None)

    if index is not None:
        plan = query_sheet[index][2]
        profile = query_sheet[index][3]

        df.loc[:, 'Plano'] = plan
        df.loc[:, 'Perfil'] = profile
        return df

    else:
        print(f"Key '{key}' not found in 'query_sheet'.")
        return None


##### 2. DATA EXTRACTION FUNCTIONS

def extract_value(text):
    if not isinstance(text, str):
        return text
    match = re.search(r'Fundo\s+(.*?)\s*\[', text)
    return match.group(1).strip() if match else text


def extract_fund_code(text):
    if not isinstance(text, str):
        return None
    match = re.search(r'\[(.*?)\]', text)
    return match.group(1).strip() if match else None


def filter_statement_by_date(df, target_date, default_fund_code='sem id'):
    """
Filtra o fluxo de caixa por uma data específica.

Args:
    df (DataFrame): Dados com colunas ['Data', 'Historico']
    target_date (str): Data de referência (formato: 'dd/mm/yyyy')
    default_fund_code (str): Código padrão caso não encontrado

Returns:
    DataFrame: Dados filtrados com [Cod Fundo, Historico]

Raises:
    ValueError: Se a data não for encontrada
    """

    df = df[df['Historico'] != 'Saldo'].copy()

    if target_date not in df['Data'].values:
        print(f"The date '{target_date}' was not found in the DataFrame.")
        return pd.DataFrame()

    start_index = df[df['Data'] == target_date].index[0]
    filtered_df = df.loc[start_index:].copy()

    next_date_indexes = filtered_df[
        filtered_df['Data'].notna() & (filtered_df['Data'] != target_date)
        ].index

    if len(next_date_indexes) > 0:
        result_df = filtered_df.loc[:next_date_indexes[0] - 1].copy()

        result_df.loc[:, 'Cod Fundo'] = result_df['Historico'].apply(
            lambda text: extract_fund_code(text)
            if isinstance(text, str) and '[' in text
            else default_fund_code
        )

        result_df.loc[:, 'Historico'] = result_df['Historico'].apply(extract_value)
        return result_df

    filtered_df.loc[:, 'Cod Fundo'] = filtered_df['Historico'].apply(
        lambda text: extract_fund_code(text)
        if isinstance(text, str) and '[' in text
        else None
    )

    filtered_df.loc[:, 'Historico'] = filtered_df['Historico'].apply(extract_value)
    return filtered_df


##### 3. MAPPING FUNCTIONS

def map_fund_classifications(df, classification_df):
    """
Mapeia classificações CVM para códigos de fundos.

Args:
    df (DataFrame): Dados com coluna 'Cod Fundo'
    classification_df (DataFrame): Dados com ['Cod Fundo', 'Classificacao CVM']

Returns:
    DataFrame: DataFrame com coluna 'Classificacao' adicionada
    """
    classification_df['Cod Fundo'] = classification_df['Cod Fundo'].astype(str).apply(
        lambda x: x.zfill(6) if x.isdigit() else x
    )
    mapping = classification_df.set_index("Cod Fundo")["Classificacao CVM"].to_dict()
    df["Classificacao"] = df["Cod Fundo"].map(mapping)
    return df


def map_fund(wallet, previous_wallet):
    """
Mapeia nomes de fundos da carteira atual para a carteira anterior.

Args:
    wallet (DataFrame): Carteira atual com nomes dos fundos
    previous_wallet (DataFrame): Carteira anterior a ser enriquecida

Returns:
    DataFrame: Carteira anterior com nomes dos fundos adicionados
    """
    mapping = wallet.set_index("Cod Fundo")["Fundo"].to_dict()
    previous_wallet["Fundo"] = previous_wallet["Cod Fundo"].map(mapping)
    return previous_wallet

##### 4. TEXT MANIPULATION FUNCTIONS

def normalize_text(text):
    """
Normaliza o texto: converte para maiúsculas, remove acentos e espaços.

Args:
    text (str): Texto a normalizar

Returns:
    str: Texto normalizado ou original se NaN
    """
    if pd.isna(text):
        return text
    text = text.upper()
    text = unidecode(text)
    return text.strip()


def edit_value(df, column, old_value, new_value):
    """
Substitui um valor por outro em uma coluna do DataFrame.

Args:
    df (DataFrame): DataFrame a ser modificado
    column (str): Nome da coluna
    old_value (str): Valor a ser substituído
    new_value (str): Novo valor

Returns:
    DataFrame: DataFrame modificado
    """
    df[column] = df[column].str.replace(old_value, new_value)
    return df


def replace_name(df, column, old_name, new_name):
    """
    Substitui um nome por outro em uma coluna do DataFrame.

    Args:
        df (DataFrame): DataFrame a ser modificado
        column (str): Nome da coluna
        old_name (str): Nome a ser substituído
        new_name (str): Novo nome

    Returns:
        DataFrame: DataFrame modificado
    """
    df[column] = df[column].str.replace(old_name, new_name)
    return df


##### 5. FILTERING AND SORTING FUNCTIONS

def sort_columns(df, column1, column2=None):
    """
Ordena o DataFrame por uma ou duas colunas.

Args:
    df (DataFrame): DataFrame a ordenar
    column1 (str): Coluna principal
    column2 (str, opcional): Coluna secundária

Returns:
    DataFrame: DataFrame ordenado
    """
    if column1 and column2:
        return df.sort_values(by=[column1, column2], ascending=[True, True])
    else:
        return df.sort_values(by=column1)


def search_word(df, column, keyword):
    filtro = df[column].str.contains(keyword, case=False, na=False)
    resultado = df[filtro].copy()

    if 'Conta contabil' in resultado.columns:
        resultado['Conta contabil'] = (pd.to_numeric(resultado['Conta contabil'], errors='coerce').astype('Int64').astype(str))

    if 'Conta' in resultado.columns:
        resultado['Conta'] = (pd.to_numeric(resultado['Conta'], errors='coerce').astype('Int64').astype(str))

    resultado = sort_columns(resultado, 'Plano', 'Perfil')
    return resultado


def filter_data(df, keywords_list):
    if isinstance(keywords_list, str):
        keywords_list = [keywords_list]

    history_column = 'Historico de lancamento' if 'Historico de lancamento' in df.columns else 'Historico'

    filtro = df[history_column].str.contains('|'.join(keywords_list), case=False, regex=True, na=False)

    novo_df = df[filtro].copy()

    if 'Conta contabil' in novo_df.columns:
        novo_df['Conta contabil'] = novo_df['Conta contabil'].astype(str)

    if 'Conta' in novo_df.columns:
        novo_df['Conta'] = novo_df['Conta'].astype(str)

    novo_df = sort_columns(novo_df, 'Plano', 'Perfil')
    return novo_df


##### 6. ACCOUNTING FUNCTIONS

def create_accounting_entry(account, value, d_c, history, plan, profile):
    """
Cria um dicionário representando um lançamento contábil.

Args:
    account (str): Conta contábil
    value (float): Valor do lançamento
    d_c (str): Indicador de débito/crédito ('D' ou 'C')
    history (str): Histórico do lançamento
    plan (str): Plano associado
    profile (str): Perfil associado

Returns:
    dict: Dicionário com os dados do lançamento
    """
    return {
        'Conta contabil': account,
        'Valor': value,
        'D/C': d_c,
        'Historico de lancamento': history,
        'CC': 2,
        'Plano': plan,
        'Perfil': profile
    }


##### 7. OUTPUT AND SAVING FUNCTIONS

def save_accounting_outputs(asset_evolution, income_accounting, cash_flow_tax_accounting, provisions_accounting, base_path, day, month):
    if asset_evolution is None:
        raise ValueError("asset_evolution - não pode ser nulo.")
    if income_accounting is None:
        raise ValueError("income_accounting - não pode ser nulo.")
    if cash_flow_tax_accounting is None:
        raise ValueError("cash_flow_tax_accounting - não pode ser nulo.")
    if provisions_accounting is None:
        raise ValueError("provisions_accounting - não pode ser nulo.")
    if not base_path:
        raise ValueError("base_path - não pode estar vazia.")

    try:
        # 1. Filter specific data (mantendo lógica antiga)
        application_df = search_word(income_accounting, 'Historico', 'APLICACAO')
        redemption_df = search_word(income_accounting, 'Historico', 'RESGATE')
        profitability_df = filter_data(income_accounting, 'RENDIMENTO')

        # 2. Create output directory
        investments_path = os.path.join(base_path, 'investimentos')
        os.makedirs(investments_path, exist_ok=True)

        # 3. Format dates (mantendo padrão antigo)
        file_date = f'{day}-{month}'
        sheet_date = f'{day}_{month}'

        # 4. Define file paths (REMOVIDO "_" para manter padrão antigo)
        asset_evolution_file = os.path.join(investments_path, f'evolucao_patrimonial{file_date}.xlsx')
        protheus_file = os.path.join(investments_path, f'lancamentos_protheus{file_date}.csv')
        segregated_file = os.path.join(investments_path, f'lancamentos_segregados{file_date}.xlsx')

        # 5. Save asset evolution
        asset_evolution.to_excel(asset_evolution_file, index=False)

        # 6. Save Protheus file (consolidated)
        protheus_df = pd.concat(
            [income_accounting, cash_flow_tax_accounting, provisions_accounting],
            ignore_index=True
        )
        protheus_df.to_csv(protheus_file, index=False, header=False, sep=';')

        # 7. Save segregated file (mantendo nomes antigos das abas)
        with pd.ExcelWriter(segregated_file) as writer:
            provisions_accounting.to_excel(writer, sheet_name=f'Provisoes{sheet_date}', index=False)
            cash_flow_tax_accounting.to_excel(writer, sheet_name=f'Despesas{sheet_date}', index=False)
            profitability_df.to_excel(writer, sheet_name=f'Rentabilidade_{sheet_date}', index=False)
            application_df.to_excel(writer, sheet_name=f'Aplicacao_{sheet_date}', index=False)
            redemption_df.to_excel(writer, sheet_name=f'Resgate_{sheet_date}', index=False)

        print("\n=== ARQUIVOS SALVOS COM SUCESSO ===")
        print(f"Evolução Patrimonial: {asset_evolution_file}")
        print(f"Lançamentos Protheus: {protheus_file}")
        print(f"Lançamentos Segregados: {segregated_file}")
        print("====================================\n")

        return {
            'asset_evolution': asset_evolution_file,
            'protheus': protheus_file,
            'segregated': segregated_file,
        }

    except PermissionError as error:
        raise PermissionError(
            f"Permissão negada ao salvar arquivos em '{base_path}'. "
            f"Verifique se a pasta existe e se os arquivos não estão abertos."
        ) from error
    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"Caminho de saída não encontrado: '{base_path}'."
        ) from error
    except OSError as error:
        raise OSError(
            f"Erro ao salvar os arquivos de saída: {error}"
        ) from error