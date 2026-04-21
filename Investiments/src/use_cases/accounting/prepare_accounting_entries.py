import pandas as pd
import os
from investiments.src.utils.tools import create_accounting_entry
from dotenv import load_dotenv

load_dotenv()
base_path = os.path.expanduser(os.getenv("BASE_PATH"))
consulta_fundos = os.getenv("CONSULTA_FUNDOS").replace('/', '\\')
path_file = os.path.normpath(os.path.join(base_path, consulta_fundos))
funds_df = pd.read_excel(path_file, sheet_name='para')

funds_df['Cod Fundo'] = funds_df['Cod Fundo'].astype(str).str.zfill(6)
funds_df['Plano'] = funds_df['Plano'].astype(int)
funds_df['Perfil'] = funds_df['Perfil'].astype(int)

def prepare_accounting_entries(income_df: pd.DataFrame, statements_df: pd.DataFrame) -> pd.DataFrame:
    protheus_entries = []

    # --- Process income entries ---
    for _, row in income_df.iterrows():
        plan = int(row['Plano'])
        profile = int(row['Perfil'])
        fund_name = row['Fundo']
        fund_code = str(row['Cod Fundo']).zfill(6)
        income_amount = round(row['Rendimento'], 2)

        fund_match = funds_df[funds_df['Cod Fundo'] == fund_code]

        if fund_match.empty:
            print(f"⚠️ Fundo não encontrado no funds_df: {fund_code}")
            continue

        positive_profit_account = fund_match['Rentabilidade Positiva'].values[0]
        negative_profit_account = fund_match['Rentabilidade Negativa'].values[0]
        updated_cost_account = fund_match['Custo Atualizado'].values[0]

        if income_amount < 0:
            protheus_entries.append(
                create_accounting_entry(
                    negative_profit_account,
                    abs(income_amount),
                    'D',
                    f'RENDIMENTO - {fund_name}',
                    plan,
                    profile
                )
            )
            protheus_entries.append(
                create_accounting_entry(
                    updated_cost_account,
                    abs(income_amount),
                    'C',
                    f'RENDIMENTO - {fund_name}',
                    plan,
                    profile
                )
            )

        elif income_amount > 0:
            protheus_entries.append(
                create_accounting_entry(
                    updated_cost_account,
                    income_amount,
                    'D',
                    f'RENDIMENTO - {fund_name}',
                    plan,
                    profile
                )
            )
            protheus_entries.append(
                create_accounting_entry(
                    positive_profit_account,
                    income_amount,
                    'C',
                    f'RENDIMENTO - {fund_name}',
                    plan,
                    profile
                )
            )

    # --- Process statement entries ---
    if not statements_df.empty:
        for _, row in statements_df.iterrows():
            fund_name = row['Historico']
            fund_code = str(row['Cod Fundo']).zfill(6)
            entry_amount = row['Entrada']
            exit_amount = row['Saida']
            plan = int(row['Plano'])
            profile = int(row['Perfil'])

            wallet_match = funds_df[
                (funds_df['Plano'] == plan) &
                (funds_df['Perfil'] == profile)
            ]

            fund_match = funds_df[
                (funds_df['Plano'] == plan) &
                (funds_df['Perfil'] == profile) &
                (funds_df['Cod Fundo'] == fund_code)
            ]

            wallet_account = None
            application_account = None
            redemption_account = None

            if wallet_match.empty:
                print(f"⚠️ Conta carteira não encontrada para Plano {plan}, Perfil {profile}")
            else:
                wallet_account = wallet_match['Investimentos'].values[0]

            if fund_match.empty:
                print(f"⚠️ Conta do fundo não encontrada para Plano {plan}, Perfil {profile}, Fundo {fund_code}")
            else:
                application_account = fund_match['Aplicacao'].values[0]
                redemption_account = fund_match['Resgate'].values[0]

            if entry_amount:
                entry_amount = round(entry_amount, 2)
                protheus_entries.append(
                    create_accounting_entry(
                        wallet_account,
                        abs(entry_amount),
                        'D',
                        f'RESGATE - {fund_name}',
                        plan,
                        profile
                    )
                )
                protheus_entries.append(
                    create_accounting_entry(
                        application_account,
                        abs(entry_amount),
                        'C',
                        f'RESGATE - {fund_name}',
                        plan,
                        profile
                    )
                )

            if exit_amount:
                exit_amount = round(exit_amount, 2)
                protheus_entries.append(
                    create_accounting_entry(
                        redemption_account,
                        abs(exit_amount),
                        'D',
                        f'APLICACAO - {fund_name}',
                        plan,
                        profile
                    )
                )
                protheus_entries.append(
                    create_accounting_entry(
                        wallet_account,
                        abs(exit_amount),
                        'C',
                        f'APLICACAO - {fund_name}',
                        plan,
                        profile
                    )
                )

    final_df = pd.DataFrame(protheus_entries)

    fixed_columns = ['Conta', 'Valor', 'Tipo', 'Historico', 'Plano', 'Perfil']
    for column in fixed_columns:
        if column not in final_df.columns:
            final_df[column] = None

    return final_df[fixed_columns]