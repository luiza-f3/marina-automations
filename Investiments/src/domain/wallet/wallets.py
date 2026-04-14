from dotenv import load_dotenv

from Investiments.src.use_cases.replace_column import replace_column_values
from Investiments.src.utils.mappings.cash_flow_info import cash_flow_info
from Investiments.src.utils.data_loader import DataLoader
from Investiments.src.utils.tools import define_profile_plan, map_fund_classifications

load_dotenv()

import pandas as pd
import os

class Wallets:
    wallet_codes = [item[0] for item in cash_flow_info] #cod_carteira
    fundQueryPath = os.path.expanduser(os.getenv("CONSULTA_FUNDOS")) #path_consulta_fundos
    funds_df = pd.read_excel(fundQueryPath, sheet_name='para') #df_fundos

    @classmethod
    def prepare_wallets(cls, path_file):
        wallets_data = DataLoader.load_file_directory(path_file, cls.wallet_codes)
        wallets_data = {key: df.iloc[10:, [0, 1, 7]] for key, df in wallets_data.items()}

        wallets_data = {key: df.set_axis(
            ['Cod Fundo', 'Fundo', 'Valor Atual'], axis=1
        ) for key, df in wallets_data.items()}

        for key, df in wallets_data.items():
            df.reset_index(drop=True, inplace=True)
            total_index = df[df['Cod Fundo'] == 'Total'].index.min()
            if total_index is not None and not pd.isna(total_index):
                wallets_data[key] = df.iloc[:total_index]

            wallets_data[key] = define_profile_plan(wallets_data[key], key, cash_flow_info)
        combined_wallets = pd.concat(wallets_data).reset_index(drop=True)

        # Format fields
        combined_wallets['Cod Fundo'] = combined_wallets['Cod Fundo'].str.zfill(6)
        combined_wallets = replace_column_values(combined_wallets, 'Fund Name')
        combined_wallets = map_fund_classifications(combined_wallets, cls.funds_df)

        return combined_wallets

    @classmethod
    def prepare_provisions(cls, file_path):
        wallets_data = DataLoader.load_file_directory(file_path, cls.cod_carteira)

        if not wallets_data:
            return pd.DataFrame(), pd.DataFrame()

        wallets_data = {
            key: df.iloc[11:, [0, 1]].copy()
            for key, df in wallets_data.items()
        }

        wallets_data = {
            key: df.set_axis(['Despesa', 'Valor'], axis=1)
            for key, df in wallets_data.items()
        }

        for key, df in wallets_data.items():
            df = df.reset_index(drop=True)

            description_row_index = df[df['Despesa'] == 'Descrição'].index.min()
            total_row_index = df[df['Despesa'] == 'TOTAL'].index.min()

            if pd.notna(description_row_index) and pd.notna(total_row_index):
                df = df.iloc[description_row_index + 1:total_row_index].copy()

            df = define_profile_plan(df, key, cash_flow_info)
            wallets_data[key] = df

        provisions = pd.concat(wallets_data).reset_index(drop=True)

        keywords = ['RESGATE', 'APLICACAO']
        redemption_application_filter = provisions['Despesa'].str.contains(
            '|'.join(keywords), case=False, regex=True, na=False
        )

        movement_provisions = provisions[redemption_application_filter].copy()
        provisions = provisions[~redemption_application_filter].copy()

        if not movement_provisions.empty:
            movement_provisions['Despesa'] = movement_provisions['Despesa'].apply(extract_value)
            movement_provisions['Despesa'] = movement_provisions['Despesa'].apply(normalize_text)

        provisions['Despesa'] = provisions['Despesa'].apply(normalize_text)
        provisions = replace_column_values(provisions, 'Despesa')

        return movement_provisions, provisions
