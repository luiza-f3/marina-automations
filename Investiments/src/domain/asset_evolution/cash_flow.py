import pandas as pd

from investiments.src.use_cases.replace_column import replace_column_values
from investiments.src.utils.data_loader import DataLoader
from investiments.src.utils.mappings.cash_flow_info import cash_flow_info
from investiments.src.utils.mappings.fees_info import fees_info
from investiments.src.utils.mappings.rename_data import fund_name_mapping
from investiments.src.utils.tools import filter_statement_by_date, define_profile_plan, normalize_text


class cashFlow:
    wallet_code = [item[0] for item in cash_flow_info]
    fees_statement = fees_info

    @classmethod
    def prepare_cash_flow(cls, file_path, target_date):
        cash_flow_data = DataLoader.load_file_directory(file_path, cls.wallet_code)

        cash_flow_data = {
            key: df.iloc[7:, :4]
            for key, df in cash_flow_data.items()
        }

        cash_flow_data = {
            key: pd.DataFrame(
                df.set_axis(['Data', 'Historico', 'Entrada', 'Saida'], axis='columns')
            )
            for key, df in cash_flow_data.items()
        }

        cash_flow_data = {
            key: filter_statement_by_date(df, target_date)
            for key, df in cash_flow_data.items()
        }

        for key, df in cash_flow_data.items():
            if df is not None and not df.empty:
                cash_flow_data[key] = define_profile_plan(cash_flow_data[key], key, cash_flow_info)

        combined_cash_flow = pd.concat(cash_flow_data).reset_index(drop=True)

        if not combined_cash_flow.empty:
            combined_cash_flow['Historico'] = combined_cash_flow['Historico'].apply(normalize_text)
            combined_cash_flow = replace_column_values(combined_cash_flow, 'Historico', fund_name_mapping)
            combined_cash_flow['Cod Fundo'] = combined_cash_flow['Cod Fundo'].str.zfill(6)
            combined_cash_flow.drop('Data', axis=1, inplace=True)

            return combined_cash_flow

        return pd.DataFrame()

    @classmethod
    def totalize_cash_flow(cls, statement):
        if statement.empty:
            return pd.DataFrame()

        aggregated_values = {}
        fee_counter = 0

        for _, row in statement.iterrows():
            history = row['Historico']
            inflow = row['Entrada']
            outflow = row['Saida']
            plan = row['Plano']
            profile = row['Perfil']
            fund_code = row['Cod Fundo']

            movement_type = "Pos" if inflow > 0 else "Neg"
            composite_key = f"{fund_code}_{plan}_{profile}_{movement_type}"

            fee_found = False

            # Check if the row corresponds to a fee
            for fee in cls.fees_statement:
                if fee in history:
                    fee_key = f"{composite_key}_{fee_counter}"

                    aggregated_values[fee_key] = {
                        'Historico': history,
                        'Entrada': inflow,
                        'Saida': outflow,
                        'Plano': plan,
                        'Perfil': profile,
                        'Cod Fundo': fund_code
                    }

                    fee_counter += 1
                    fee_found = True
                    break

            if fee_found:
                continue

            # Aggregate non-fee entries
            if composite_key in aggregated_values:
                existing_entry = aggregated_values[composite_key]

                if existing_entry['Entrada'] > 0 and inflow > 0:
                    existing_entry['Entrada'] += inflow

                elif existing_entry['Saida'] > 0 and outflow > 0:
                    existing_entry['Saida'] += outflow

                else:
                    existing_entry['Entrada'] += inflow
                    existing_entry['Saida'] += outflow

            else:
                aggregated_values[composite_key] = {
                    'Historico': history,
                    'Entrada': inflow,
                    'Saida': outflow,
                    'Plano': plan,
                    'Perfil': profile,
                    'Cod Fundo': fund_code
                }

        result_df = pd.DataFrame.from_dict(aggregated_values, orient='index').reset_index(drop=True)

        result_df = result_df[
            ['Historico', 'Entrada', 'Saida', 'Plano', 'Perfil', 'Cod Fundo']
        ]

        return result_df

    @classmethod
    def generate_inflow_outflow_difference(cls, statement):
        if statement.empty:
            return pd.DataFrame()

        aggregated_values = {}

        for _, row in statement.iterrows():
            history = row['Historico']
            fund_code = row['Cod Fundo']
            inflow = row['Entrada']
            outflow = row['Saida']
            plan = row['Plano']
            profile = row['Perfil']

            composite_key = f"{fund_code}_{plan}_{profile}"

            if composite_key in aggregated_values:
                aggregated_values[composite_key]['Entrada'] += inflow
                aggregated_values[composite_key]['Saida'] += outflow

                current_entry = aggregated_values[composite_key]

                # Apply legacy balance rule only if both are non-zero
                if current_entry['Entrada'] != 0 and current_entry['Saida'] != 0:
                    balance = current_entry['Entrada'] + current_entry['Saida']

                    if balance < 0:
                        current_entry['Entrada'] = 0
                        current_entry['Saida'] = balance
                    else:
                        current_entry['Saida'] = 0
                        current_entry['Entrada'] = balance

            else:
                aggregated_values[composite_key] = {
                    'Historico': history,
                    'Cod Fundo': fund_code,
                    'Entrada': inflow,
                    'Saida': outflow,
                    'Plano': plan,
                    'Perfil': profile
                }

        result_df = pd.DataFrame.from_dict(aggregated_values, orient='index').reset_index(drop=True)

        result_df = result_df[
            ['Historico', 'Cod Fundo', 'Entrada', 'Saida', 'Plano', 'Perfil']
        ]

        return result_df

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

        return redemption_acquisition_df, updated_statement_df, expense_df

