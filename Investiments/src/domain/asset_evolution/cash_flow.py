import pandas as pd

from investiments.src.use_cases.replace_column import replace_column_values
from investiments.src.utils.data_loader import DataLoader
from investiments.src.utils.mappings.cash_flow_info import cash_flow_info
from investiments.src.utils.mappings.fees_info import fees_info
from investiments.src.utils.tools import filter_statement_by_date, define_profile_plan, normalize_text


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

    @classmethod
    def totalize_cash_flow(cls, statement):
        if statement.empty:
            return pd.DataFrame()

        totals = {}

        for _, row in statement.iterrows():
            history = str(row['Historico'])
            inflow = row['Entrada']
            outflow = row['Saida']
            plan = row['Plano']
            profile = row['Perfil']
            fund_code = row['Cod Fundo']

            movement_type = 'Pos' if inflow > 0 else 'Neg'
            composite_key = f'{fund_code}_{plan}_{profile}_{movement_type}'

            fee_found = False
            for fee in cls.fees_statement:
                if fee in history:
                    fee_key = f'{composite_key}_{fee}'
                    if fee_key not in totals:
                        totals[fee_key] = {
                            'Cod Fundo': fund_code,
                            'Plano': plan,
                            'Perfil': profile,
                            'Tipo': movement_type,
                            'Taxa': fee,
                            'Valor': 0
                        }
                    totals[fee_key]['Valor'] += inflow - outflow
                    fee_found = True
                    break

            if not fee_found:
                if composite_key not in totals:
                    totals[composite_key] = {
                        'Cod Fundo': fund_code,
                        'Plano': plan,
                        'Perfil': profile,
                        'Tipo': movement_type,
                        'Taxa': None,
                        'Valor': 0
                    }
                totals[composite_key]['Valor'] += inflow - outflow

        return pd.DataFrame(totals.values())

    @classmethod
    def generate_inflow_outflow_difference(cls, statement):
        if statement.empty:
            return pd.DataFrame(columns=['Historico', 'Cod Fundo', 'Entrada', 'Saida', 'Plano', 'Perfil'])

        grouped_values = {}

        for _,row in statement.iterrows():
            group_key = (row['Cod Fundo'], row['Plano'], row['Perfil'])

            if group_key not in grouped_values:
                grouped_values[group_key] = {
                    'Historico': row['Historico'],
                    'Cod Fundo': row['Cod Fundo'],
                    'Entrada': 0,
                    'Saida': 0,
                    'Plano': row['Plano'],
                    'Perfil': row['Perfil']
                }

            grouped_values[group_key]['Entrada'] += row['Entrada']
            grouped_values[group_key]['Saida'] += row['Saida']

        result_df = pd.DataFrame(grouped_values.values())

        balance = result_df['Entrada'] - result_df['Saida']
        result_df['Entrada'] = balance.apply(lambda value: value if value > 0 else 0)
        result_df['Saida'] = balance.apply(lambda value: value if value < 0 else 0)

        return result_df[['Historico', 'Cod Fundo', 'Entrada', 'Saida', 'Plano', 'Perfil']]

    @classmethod
    def filter_records(cls, statement_df: pd.DataFrame):
        redemption_acquisition_rows = []
        expense_rows = []
        fund_rows = []

        for _, row in statement_df.iterrows():
            history = str(row['Historico'])
            if any(keyword in history for keyword in cls.fees_statement):
                expense_rows.append(dict(row))
            elif 'RESGATE DE COTAS' in history or 'AQUISICAO DE COTAS' in history:
                redemption_acquisition_rows.append(dict(row))
            else:
                fund_rows.append(dict(row))

        redemption_acquisition_df  = pd.DataFrame(redemption_acquisition_rows)
        updated_statement_df = pd.DataFrame(fund_rows)
        expense_df = pd.DataFrame(expense_rows)

        return updated_statement_df, redemption_acquisition_df, expense_df

