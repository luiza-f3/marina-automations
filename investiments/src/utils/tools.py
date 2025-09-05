import re

from dotenv import load_dotenv
import os
import pandas as pd

from investiments.src.utils.consultas.fees_info import fees_info
from pandas import concat
from unidecode import unidecode

load_dotenv()
path_consulta_fundos = os.getenv('CONSULTA_FUNDOS')
df_fundos = pd.read_excel(path_consulta_fundos, sheet_name='para')

def define_profile_plan(df, key, querySheet):
    """Define plano e perfil para qulaquer necessidade mas precisa de uma planilha de consulta"""
    index = next((i for i, row in enumerate(querySheet) if row[0] == key), None)

    # Verifica se o `key` foi encontrado
    if index is not None:
        plan = querySheet[index][2]
        profile = querySheet[index][3]

        # Retorna as colunas "Plano" e "Perfil" com base nos valores encontrados
        df['Plano'] = plan
        df['Perfil'] = profile
        return df
    else:
        print(f"Chave '{key}' não encontrada em 'querySheet'.")
        return None

def filtrar_data_demonstrativo(df, date):
    """Função que filtra movimentações do fluxo de caixa seguindo um padrão especifico"""
    df = df[df['Historico'] != 'Saldo']

    if date not in df['Data'].values:
        print(f"A data '{date}' não foi encontrada no DataFrame.")
        return pd.DataFrame()
    else:
        indice_inicio = df[df['Data'] == date].index[0]

        df_filtrado = df.loc[indice_inicio:]

        proxima_data = df_filtrado[df_filtrado['Data'].notna() & (df_filtrado['Data'] != date)].index

        inexistente = 'sem id'

        if len(proxima_data) > 0:
            # Filtra o DataFrame até a próxima data encontrada
            df = df_filtrado.loc[:proxima_data[0] - 1]

            # Extrai cod_fundo antes de limpar o histórico (enquanto ainda tem os colchetes)
            df['Cod Fundo'] = df['Historico'].apply(
                lambda texto: extrair_cod_fundo(texto) if '[' in texto else inexistente
            )

            # Agora sim, extrai valor do histórico (limpa o restante)
            df['Historico'] = df.apply(lambda x: extrair_valor(x['Historico']), axis=1)

            return df
        else:
            # Mesmo processo no else
            df_filtrado['Cod Fundo'] = df_filtrado['Historico'].apply(
                lambda texto: extrair_cod_fundo(texto) if '[' in texto else None
            )
            df_filtrado['Historico'] = df_filtrado.apply(lambda x: extrair_valor(x['Historico']), axis=1)

            return df_filtrado

def extrair_valor(texto):
    inicio = texto.find('Fundo')
    fim = texto.find('[')
    if inicio > 0 and fim > 0:
        valor = texto[inicio+5:fim].strip()
        return valor
    return texto

def extrair_cod_fundo(texto):
    if not isinstance(texto, str):
        return None

    inicio = texto.find('[')
    fim = texto.find(']')

    if inicio != -1 and fim != -1 and inicio < fim:
        return texto[inicio + 1:fim].strip()

    return None


def mapear_classificacoes(df, consulta_classificao):
    consulta_classificao['Cod Fundo'] = consulta_classificao['Cod Fundo'].astype(str).apply(
        lambda x: x.zfill(6) if x.isdigit() else x)
    mapeamento = consulta_classificao.set_index("Cod Fundo")["Classificacao CVM"].to_dict()
    df["Classificacao"] = df["Cod Fundo"].map(mapeamento)
    return df

def editar_valor(df, coluna, nome_antigo, nome_novo):
    df[coluna] = df[coluna].str.replace(nome_antigo, nome_novo)
    return df

def criar_lancamento_contabil(conta, valor, d_c, historico, plano, perfil):
    return {
        'Conta contabil': conta,
        'Valor': valor,
        'D/C': d_c,
        'Historico de lancamento': historico,
        'CC': 2,
        'Plano': plano,
        'Perfil': perfil
    }

def substituir_nome(df, coluna, nome_antigo, nome_novo):
    df[coluna] = df[coluna].str.replace(nome_antigo, nome_novo)
    return df

def normalize_text(text):
    if pd.isna(text):
        return text
    text = text.upper()
    text = unidecode(text)
    return text.strip()

def save_data(assetEvolution, income_accounting, cash_flow_tax_accounting, provisions_accouting, base_path, day, month):
    df_aplic = procurar_palavra(income_accounting, 'Historico de lancamento', 'APLICACAO')
    df_resg = procurar_palavra(income_accounting, 'Historico de lancamento', 'RESGATE')

    lista_rentabilidade = 'RENDIMENTO'
    filtro_rent = filtrar_dados(income_accounting, lista_rentabilidade)

    investiments_path = os.path.join(base_path, 'investimentos')
    os.makedirs(investiments_path, exist_ok=True)

    assetEvolution.to_excel(os.path.join(investiments_path, f'evolucao_patrimonial{day}-{month}.xlsx'), index=False)

    df_protheus = concat([income_accounting, cash_flow_tax_accounting, provisions_accouting], ignore_index=True)
    df_protheus.to_csv(os.path.join(investiments_path, f'lancamentos_protheus{day}-{month}.csv'), index=False,
                       header=False, sep=';')

    with pd.ExcelWriter(os.path.join(investiments_path, f'lancamentos_segregados{day}-{month}.xlsx')) as writer:
        provisions_accouting.to_excel(writer, sheet_name=f'Provisoes{day}_{month}', index=False)
        cash_flow_tax_accounting.to_excel(writer, sheet_name=f'Despesas{day}_{month}', index=False)
        filtro_rent.to_excel(writer, sheet_name=f'Rentabilidade_{day}_{month}', index=False)
        df_aplic.to_excel(writer, sheet_name=f'Aplicacao_{day}_{month}', index=False)
        df_resg.to_excel(writer, sheet_name=f'Resgate_{day}_{month}', index=False)

    print('Arquivos salvos com sucesso')


def filtrar_dados(df, lista_palavras):
    # Cria um filtro booleano para as linhas que contêm parcialmente alguma palavra da lista
    filtro = df['Historico de lancamento'].str.contains('|'.join(lista_palavras), case=False, regex=True)

    # Aplica o filtro ao DataFrame original para obter um novo DataFrame
    novo_df = df[filtro]
    novo_df['Conta contabil'] = novo_df['Conta contabil'].astype(str)
    novo_df = ordenar_coluna(novo_df, 'Plano', 'Perfil')
    return novo_df

def ordenar_coluna(df, coluna1, coluna2=None):
    if coluna1 and coluna2:
        return df.sort_values(by=[coluna1, coluna2], ascending=[True, True])
    else:
        return df.sort_values(by=coluna1)

def procurar_palavra(df, coluna, palavra_chave):
    filtro = df[coluna].str.contains(palavra_chave, case=False)
    resultado = df[filtro]

    resultado['Conta contabil'] = resultado['Conta contabil'].astype(str)
    resultado = ordenar_coluna(resultado, 'Plano', 'Perfil')
    return resultado

def mapear_fundo(wallet, previous_wallet):
    mapeamento = wallet.set_index("Cod Fundo")["Fundo"].to_dict()
    previous_wallet["Fundo"] = previous_wallet["Cod Fundo"].map(mapeamento)
    return previous_wallet
