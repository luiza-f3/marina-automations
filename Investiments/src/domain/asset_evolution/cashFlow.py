import pandas as pd

from Investiments.src.use_cases.replace_column import replace_column_values
from Investiments.src.utils.data_loader import DataLoader
from Investiments.src.utils.mappings.cash_flow_info import cash_flow_info
from Investiments.src.utils.mappings.fees_info import fees_info
from Investiments.src.utils.tools import filter_statement_by_date, define_profile_plan, normalize_text


class cashFlow:
    wallet_code = [item[0] for item in cash_flow_info]
    fees_statement = fees_info

    @classmethod
    def prepare_cash_flow(cls, file_path, target_date):
        cash_flow_data = DataLoader.load_file_directory(file_path, cls.wallet_code)

        cash_flow_data = {
            key: df.iloc[7:, :4].copy()
            for key, df in cash_flow_data.items()
        }

        cash_flow_data = {
            key: df.set_axis(['Data', 'Historico', 'Entrada', 'Saida'], axis='columns')
            for key, df in cash_flow_data.items()
        }

        cash_flow_data = {
            key: filter_statement_by_date(df, target_date)
            for key, df in cash_flow_data.items()
        }

        for key, df in cash_flow_data.items():
            if not df.empty:
                cash_flow_data[key] = define_profile_plan(df, key, cash_flow_info)

        cash_flow_data = {
            key: df for key, df in cash_flow_data.items()
            if not df.empty
        }

        if not cash_flow_data:
            print("Nenhum fluxo de caixa válido encontrado.")
            return pd.DataFrame()

        combined_cash_flow = pd.concat(cash_flow_data).reset_index(drop=True)

        combined_cash_flow['Historico'] = combined_cash_flow['Historico'].apply(normalize_text)
        combined_cash_flow = replace_column_values(combined_cash_flow, 'Historico')
        combined_cash_flow['Cod Fundo'] = combined_cash_flow['Cod Fundo'].astype(str).str.zfill(6)

        combined_cash_flow = combined_cash_flow.drop(columns='Data')

        return combined_cash_flow