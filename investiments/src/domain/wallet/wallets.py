from dotenv import load_dotenv
from investiments.src.use_cases.replace_column import replace_column_values
from investiments.src.utils.mappings.cash_flow_info import cash_flow_info
from investiments.src.utils.data_loader import DataLoader
from investiments.src.utils.mappings.rename_data import fund_name_mapping
from investiments.src.utils.tools import define_profile_plan, map_fund_classifications, extract_value
from investiments.src.utils.tools import normalize_text
import os
import pandas as pd

load_dotenv()
base_path = os.path.expanduser(os.getenv("BASE_PATH"))
consulta_fundos = os.getenv("CONSULTA_FUNDOS")

#Classe responsável pela leitura e consolidação de carteiras de investimento.
class Wallets:

    # Extrai os códigos das carteiras definidos em cash_flow_info
    wallet_codes = [item[0] for item in cash_flow_info]
    
    # Caminho do arquivo de consulta de fundos (consulta_fundos.xlsx) para mapeamento de classificações e contas contábeis
    fundQueryPath = os.path.normpath(os.path.join(base_path, consulta_fundos))
    
    # Carrega o DataFrame de fundos a partir do arquivo Excel, aba 'para', para uso em mapeamento de fundos
    funds_df = pd.read_excel(fundQueryPath, sheet_name='para')

    # prepare_wallets(): Consolida posições de fundos com plano, perfil e classificação, padronizando nomes e códigos para garantir consistência no cálculo de rendimento.
    @classmethod
    def prepare_wallets(cls, path_file):

        # CARREGAMENTO DE ARQUIVOS DE CARTEIRA (Busca arquivos pelos códigos definidos em wallet_codes.)
        wallets_data = DataLoader.load_file_directory(path_file, cls.wallet_codes)

        # EXTRAÇÃO DOS DADOS DA CARTEIRA (Seleciona as linhas e colunas necessárias de cada arquivo.)
        wallets_data = {
            key: df.iloc[10:, [0, 1, 7]].copy()
            for key, df in wallets_data.items()
        }

        # PADRONIZAÇÃO DE COLUNAS (Renomeia colunas para manter consistência no processamento.)
        wallets_data = {
            key: df.set_axis(["Cod Fundo", "Fundo", "Valor Atual"], axis=1)
            for key, df in wallets_data.items()
        }

        # FILTRAGEM E ADIÇÃO DE PLANO/PERFIL
        for key, df in wallets_data.items():
            df = df.reset_index(drop=True) # Reseta o índice após a filtragem dos dados
            total_index = df[df["Cod Fundo"] == "Total"].index.min() #Localiza a linha "Total" que indica o fim da seção de fundos

            # Remove linhas após "Total" (provisões são processadas separadamente)
            if pd.notna(total_index):
                df = df.iloc[:total_index].copy()

            # Adiciona colunas de Plano e Perfil com base no código da carteira
            df = define_profile_plan(df, key, cash_flow_info)
            wallets_data[key] = df

        # CONSOLIDAÇÃO DAS CARTEIRAS (Concatena os DataFrames em uma única estrutura.)
        combined_wallets = pd.concat(wallets_data, ignore_index=True)

        # NORMALIZAÇÃO DOS DADOS (Padroniza códigos de fundo para 6 dígitos.)
        combined_wallets['Cod Fundo'] = combined_wallets['Cod Fundo'].astype(str).str.zfill(6)

        # Padroniza nomes dos fundos utilizando fund_name_mapping para evitar divergências de nomenclatura entre carteiras e demonstrativos.
        combined_wallets = replace_column_values(combined_wallets, 'Fundo', fund_name_mapping)
        
        # Adiciona a classificação do fundo com base no código informado
        combined_wallets = map_fund_classifications(combined_wallets, cls.funds_df)

        return combined_wallets

    #prepare_provisions(): Extrai movimentações pendentes e provisões das carteiras do rodapé das carteiras, classificando-as em movimentações (resgates/aplicações) e provisões (despesas/taxas) para ajuste de saldo e geração de relatórios.
    @classmethod
    def prepare_provisions(cls, file_path):
        
        # CARREGAMENTO DOS ARQUIVOS DE CARTEIRA
        wallets_data = DataLoader.load_file_directory(file_path, cls.wallet_codes)

        # Encerra o processamento caso nenhum arquivo seja encontrado
        if not wallets_data:
            return pd.DataFrame(), pd.DataFrame()

        # EXTRAÇÃO DO RODAPÉ DA CARTEIRA (Seleciona as linhas e colunas de provisões.)
        wallets_data = {
            key: df.iloc[11:, [0, 1]].copy()
            for key, df in wallets_data.items()
        }

        # PADRONIZAÇÃO DE COLUNAS DAS PROVISÕES (Renomeia colunas para manter consistência no processamento.)
        wallets_data = {
            key: df.set_axis(['Despesa', 'Valor'], axis=1)
            for key, df in wallets_data.items()
        }

        # ISOLAMENTO DA SEÇÃO DE PROVISÕES
        for key, df in wallets_data.items():
            df = df.reset_index(drop=True)

            # Localiza linha com rótulo "Descrição" (marca início da tabela)
            description_row_index = df[df['Despesa'] == 'Descrição'].index.min()
            
            # Localiza linha com "TOTAL" (marca fim de provisões)
            total_row_index = df[df['Despesa'] == 'TOTAL'].index.min()

            # Filtra apenas a seção entre "Descrição" e "TOTAL"
            if pd.notna(total_row_index):
                if pd.notna(description_row_index):
                    # Se "Descrição" existe, começa APÓS ela
                    df = df.iloc[description_row_index + 1:total_row_index].copy()
                else:
                    # Caso contrário, inicia do topo até "TOTAL"
                    df = df.iloc[:total_row_index].copy()

            # Adiciona colunas de Plano e Perfil ao DataFrame
            df = define_profile_plan(df, key, cash_flow_info)
            wallets_data[key] = df

        # CONSOLIDAÇÃO DAS PROVISÕES (Mantém apenas DataFrames com dados.)
        valid_dataframes = [df for df in wallets_data.values() if not df.empty]
        
        # Encerra o processamento caso não existam dados válidos
        if not valid_dataframes:
            return pd.DataFrame(), pd.DataFrame()

        # Consolida os DataFrames válidos em uma única estrutura
        provisions = pd.concat(valid_dataframes, ignore_index=True)

        # SEPARAÇÃO DE MOVIMENTAÇÕES E PROVISÕES (Define os registros de movimentações pendentes.)
        keywords = ['RESGATE', 'APLICACAO']

        # Identifica registros de RESGATE ou APLICACAO na descrição
        redemption_application_filter = provisions['Despesa'].astype(str).str.contains(
            '|'.join(keywords), case=False, regex=True, na=False
        )

        # Separa os registros em movimentações e provisões
        movement_provisions = provisions[redemption_application_filter].copy()
        provisions = provisions[~redemption_application_filter].copy()

        # NORMALIZAÇÃO DAS MOVIMENTAÇÕES (Extrai o nome do fundo e padroniza texto para maiúsculo e sem acentos para garantir associação correta com a carteira.)
        if not movement_provisions.empty:
            movement_provisions['Despesa'] = movement_provisions['Despesa'].apply(extract_value) # Extrai o nome do fundo da descrição da movimentação
            movement_provisions['Despesa'] = movement_provisions['Despesa'].apply(normalize_text) # Padroniza texto para maiúsculo e remove acentos

        # Normaliza o texto das provisões
        provisions['Despesa'] = provisions['Despesa'].apply(normalize_text)
        
        # Aplica mapeamento de renomeação (fund_name_mapping) para padronizar nomes
        provisions = replace_column_values(provisions, 'Despesa', fund_name_mapping)

        return movement_provisions, provisions
