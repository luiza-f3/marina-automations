from investiments.src.core.usecases.executeFromTo import executeFromTo
from investiments.src.utils.consultas.cash_flow_info import cash_flow_info
from investiments.src.utils.data_loader import DataLoader
from investiments.src.utils.tools import define_profile_plan, normalize_text, extrair_valor
from investiments.src.utils.tools import mapear_classificacoes

from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import os

class Carteira:
    """Métodos para manipular as carteiras"""
    cod_carteira = [item[0] for item in cash_flow_info]
    path_consulta_fundos = os.path.expanduser(os.getenv("CONSULTA_FUNDOS"))
    df_fundos = pd.read_excel(path_consulta_fundos, sheet_name='para')

    @classmethod
    def preparar_carteiras(cls, path_file):
        """Junta todas as carteiras"""
        df_wallets = DataLoader.load_file_directory(path_file, cls.cod_carteira)
        df_wallets = {key: df.iloc[10:, [0, 1, 7]] for key, df in df_wallets.items()}
        df_wallets = {key: df.set_axis(
            ['Cod Fundo', 'Fundo', 'Valor Atual'], axis=1
        ) for key, df in df_wallets.items()}

        for key, df in df_wallets.items():
            df.reset_index(drop=True, inplace=True)
            total_index = df[df['Cod Fundo'] == 'Total'].index.min()
            if total_index is not None and not pd.isna(total_index):
                df_wallets[key] = df.iloc[:total_index]

            df_wallets[key] = define_profile_plan(df_wallets[key], key, cash_flow_info)
        wallets = pd.concat(df_wallets).reset_index(drop=True)

        # ======= formatação de campos =======
        # garantir 6 caracteres para os código do fundo
        wallets['Cod Fundo'] = wallets['Cod Fundo'].str.zfill(6)

        wallets = executeFromTo(wallets, 'Fundo')

        wallets = mapear_classificacoes(wallets, cls.df_fundos)

        return wallets

    @classmethod
    def preparar_provisao(cls, path_file):
        df_wallets = DataLoader.load_file_directory(path_file, cls.cod_carteira)
        df_wallets = {key: df.iloc[11:, [0, 1]] for key, df in df_wallets.items()}

        df_wallets = {key: df.set_axis(
            ['Despesa', 'Valor'], axis=1
        ) for key, df in df_wallets.items()}

        for key, df in df_wallets.items():
            df.reset_index(drop=True, inplace=True)

            descricao_index = df[df['Despesa'] == 'Descrição'].index.min()
            total_index = df[df['Despesa'] == 'TOTAL'].index.min()

            if total_index is not None and not pd.isna(total_index):
                df_wallets[key] = df.iloc[descricao_index + 1:total_index]

            df_wallets[key] = define_profile_plan(df_wallets[key], key, cash_flow_info)

        provisions = pd.concat(df_wallets).reset_index(drop=True)

        redemptions_applications_provisions_filter = provisions['Despesa'].str.contains(
            '|'.join(['RESGATE', 'APLICACAO']), case=False, regex=True)

## Adicionar aqui a preparação caso não haja provisões de resgate/aplicação

        redemptions_applications_provisions = provisions[redemptions_applications_provisions_filter]
        if redemptions_applications_provisions is not None and not redemptions_applications_provisions.empty:
            redemptions_applications_provisions['Despesa'] = redemptions_applications_provisions.apply(
                lambda x: extrair_valor(x['Despesa']), axis=1)

        provisions = provisions[~redemptions_applications_provisions_filter]

        redemptions_applications_provisions['Despesa'] = redemptions_applications_provisions['Despesa'].apply(normalize_text)
        provisions['Despesa'] = provisions['Despesa'].apply(normalize_text)
        provisions = executeFromTo(provisions, 'Despesa')

        return redemptions_applications_provisions, provisions