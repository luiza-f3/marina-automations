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


class Wallets:
    wallet_codes = [item[0] for item in cash_flow_info]
    fundQueryPath = os.path.normpath(os.path.join(base_path, consulta_fundos))
    funds_df = pd.read_excel(fundQueryPath, sheet_name='para')

    @classmethod
    def prepare_wallets(cls, path_file):
        wallets_data = DataLoader.load_file_directory(path_file, cls.wallet_codes)

        wallets_data = {
            key: df.iloc[10:, [0, 1, 7]].copy()
            for key, df in wallets_data.items()
        }

        wallets_data = {
            key: df.set_axis(["Cod Fundo", "Fundo", "Valor Atual"], axis=1)
            for key, df in wallets_data.items()
        }

        for key, df in wallets_data.items():
            df = df.reset_index(drop=True)

            total_index = df[df["Cod Fundo"] == "Total"].index.min()
            if pd.notna(total_index):
                df = df.iloc[:total_index].copy()

            df = define_profile_plan(df, key, cash_flow_info)
            wallets_data[key] = df

        combined_wallets = pd.concat(wallets_data, ignore_index=True)

        combined_wallets['Cod Fundo'] = combined_wallets['Cod Fundo'].astype(str).str.zfill(6)
        combined_wallets = replace_column_values(combined_wallets, 'Fundo', fund_name_mapping)
        combined_wallets = map_fund_classifications(combined_wallets, cls.funds_df)

        return combined_wallets

    @classmethod
    def prepare_provisions(cls, file_path):
        wallets_data = DataLoader.load_file_directory(file_path, cls.wallet_codes)

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

            if pd.notna(total_row_index):
                if pd.notna(description_row_index):
                    df = df.iloc[description_row_index + 1:total_row_index].copy()
                else:
                    df = df.iloc[:total_row_index].copy()

            df = define_profile_plan(df, key, cash_flow_info)
            wallets_data[key] = df

        valid_dataframes = [df for df in wallets_data.values() if not df.empty]
        if not valid_dataframes:
            return pd.DataFrame(), pd.DataFrame()

        provisions = pd.concat(valid_dataframes, ignore_index=True)

        keywords = ['RESGATE', 'APLICACAO']
        redemption_application_filter = provisions['Despesa'].astype(str).str.contains(
            '|'.join(keywords), case=False, regex=True, na=False
        )

        movement_provisions = provisions[redemption_application_filter].copy()
        provisions = provisions[~redemption_application_filter].copy()

        if not movement_provisions.empty:
            movement_provisions['Despesa'] = movement_provisions['Despesa'].apply(extract_value)
            movement_provisions['Despesa'] = movement_provisions['Despesa'].apply(normalize_text)

        provisions['Despesa'] = provisions['Despesa'].apply(normalize_text)
        provisions = replace_column_values(provisions, 'Despesa', fund_name_mapping)

        return movement_provisions, provisions

