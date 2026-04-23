import os
import pandas as pd
from investiments.src.utils.mappings.fees_accounts import fees_accounts
from investiments.src.utils.tools import create_accounting_entry
from dotenv import load_dotenv

load_dotenv()
base_path = os.path.expanduser(os.getenv("BASE_PATH"))
consulta_fundos = os.getenv("CONSULTA_FUNDOS")
funds_file_path = os.path.normpath(os.path.join(base_path, consulta_fundos))
df_funds = pd.read_excel(funds_file_path, sheet_name='para')

# Constantes
standard_fees = ('DESPESA - CUSTO CETIP', 'TAXA CETIP')
special_plans = {(987, 19), (952, 20)}
iof_account = 50298999900000

def statement_fee_expenses(df_despesas):
    """Processa despesas e taxas, gerando lançamentos contábeis."""

    accounting_entries = []

    for _, row in df_despesas.iterrows():
        fund = row['Historico']
        plan = row['Plano']
        profile = row['Perfil']
        inflow = row['Entrada']
        outflow = row['Saida']

        # Busca conta da carteira
        current_wallet = df_funds.loc[
            (df_funds['Plano'] == plan) &
            (df_funds['Perfil'] == profile)
            ]['Investimentos'].values[0]

        # Define tipo de conta (PGA ou Plano)
        tipo_conta = 'PGA' if (plan, profile) in special_plans else 'Plano'

        value = abs(inflow) if inflow != 0 else abs(outflow)

        # ========== IOF ==========
        if fund == 'IOF':
            if inflow != 0:
                accounting_entries.append(create_accounting_entry(current_wallet, value, 'D', fund, plan, profile))
                accounting_entries.append(create_accounting_entry(iof_account, value, 'C', fund, plan, profile))
            elif outflow != 0:
                accounting_entries.append(create_accounting_entry(iof_account, value, 'D', fund, plan, profile))
                accounting_entries.append(create_accounting_entry(current_wallet, value, 'C', fund, plan, profile))

        # ========== ESTORNO DE TAXA CETIP ==========
        elif fund in ['ESTORNO DE TAXA CETIP', 'ESTORNO TAXA CETIP']:
            accounting_entries.append(create_accounting_entry(fees_accounts['ESTORNO DE TAXA CETIP']['PGA'], value, 'D',
                                                         'ESTORNO DE TAXA CETIP', plan, profile))
            accounting_entries.append(
                create_accounting_entry(current_wallet, value, 'C', 'ESTORNO DE TAXA CETIP', plan, profile))

        # ========== TAXAS PADRÃO (CETIP) ==========
        elif fund in standard_fees:
            if inflow != 0:
                accounting_entries.append(create_accounting_entry(current_wallet, value, 'D', fund, plan, profile))
                accounting_entries.append(create_accounting_entry(fees_accounts['Taxa CETIP'][tipo_conta], value, 'C', fund, plan, profile))
            elif outflow != 0:
                accounting_entries.append(create_accounting_entry(fees_accounts['Taxa CETIP'][tipo_conta], value, 'D', fund, plan, profile))
                accounting_entries.append(create_accounting_entry(current_wallet, value, 'C', fund, plan, profile))

        # ========== TAXA DE CONTROLADORIA ==========
        elif fund == 'TAXA DE CONTROLADORIA':
            if inflow != 0:
                accounting_entries.append(create_accounting_entry(current_wallet, value, 'D', fund, plan, profile))
                accounting_entries.append(create_accounting_entry(fees_accounts['TAXA DE CONTROLADORIA'][tipo_conta], value, 'C', fund, plan, profile))
            elif outflow != 0:
                accounting_entries.append(create_accounting_entry(fees_accounts['TAXA DE CONTROLADORIA'][tipo_conta], value, 'D', fund, plan, profile))
                accounting_entries.append(create_accounting_entry(current_wallet, value, 'C', fund, plan, profile))

        # ========== TAXA DE CUSTÓDIA ==========
        elif fund == 'TAXA DE CUSTODIA':
            if inflow != 0:
                accounting_entries.append(create_accounting_entry(current_wallet, value, 'D', fund, plan, profile))
                accounting_entries.append(create_accounting_entry(fees_accounts['TAXA DE CUSTODIA'][tipo_conta], value, 'C', fund, plan, profile))
            elif outflow != 0:
                accounting_entries.append(create_accounting_entry(fees_accounts['TAXA DE CUSTODIA'][tipo_conta], value, 'D', fund, plan, profile))
                accounting_entries.append(create_accounting_entry(current_wallet, value, 'C', fund, plan, profile))

        # ========== AJUSTES DE TAXA CETIP E SELIC ==========
        elif fund in ['(AJUSTE) TAXA CETIP', 'AJUSTE DE TAXA SELIC']:
            if inflow != 0:
                accounting_entries.append(create_accounting_entry(current_wallet, value, 'D', fund, plan, profile))
                accounting_entries.append(
                    create_accounting_entry(fees_accounts['Taxa CETIP']['Despesa'], value, 'C', fund, plan, profile))
            elif outflow != 0:
                accounting_entries.append(
                    create_accounting_entry(fees_accounts['Taxa CETIP']['Despesa'], value, 'D', fund, plan, profile))
                accounting_entries.append(create_accounting_entry(current_wallet, value, 'C', fund, plan, profile))

        # ========== TARIFAS DE LIQUIDAÇÃO ==========
        elif fund in ['DESPESA B 10 - TARIFA DE LIQUIDACAO FINANCEIRA', '(AJUSTE) TARIFA DE LIQUIDACAO FINANCEIRA']:
            chave_tipo = 'Despesa' if '(AJUSTE)' in fund else tipo_conta

            if inflow != 0:
                accounting_entries.append(create_accounting_entry(current_wallet, value, 'D', fund, plan, profile))
                accounting_entries.append(
                    create_accounting_entry(fees_accounts[fund][chave_tipo], value, 'C', fund, plan, profile))
            elif outflow != 0:
                accounting_entries.append(
                    create_accounting_entry(fees_accounts[fund][chave_tipo], value, 'D', fund, plan, profile))
                accounting_entries.append(create_accounting_entry(current_wallet, value, 'C', fund, plan, profile))

        # ========== TAXA DE ADMINISTRAÇÃO ==========
        elif fund == 'TAXA ADMINISTRACAO':
            if inflow != 0:
                accounting_entries.append(create_accounting_entry(current_wallet, value, 'D', fund, plan, profile))
                accounting_entries.append(
                    create_accounting_entry(fees_accounts['Taxa CETIP'][tipo_conta], value, 'C', fund, plan, profile))
            elif outflow != 0:
                accounting_entries.append(
                    create_accounting_entry(fees_accounts['Taxa CETIP'][tipo_conta], value, 'D', fund, plan, profile))
                accounting_entries.append(create_accounting_entry(current_wallet, value, 'C', fund, plan, profile))

        # ========== DESPESA DE CUSTO SELIC ==========
        elif fund == 'DESPESA DE CUSTO SELIC':
            if inflow != 0:
                accounting_entries.append(create_accounting_entry(current_wallet, value, 'D', fund, plan, profile))
                accounting_entries.append(
                    create_accounting_entry(fees_accounts['Despesa de CUSTO SELIC'][tipo_conta], value, 'C', fund, plan, profile))
            elif outflow != 0:
                accounting_entries.append(
                    create_accounting_entry(fees_accounts['Despesa de CUSTO SELIC'][tipo_conta], value, 'D', fund, plan, profile))
                accounting_entries.append(create_accounting_entry(current_wallet, value, 'C', fund, plan, profile))
    return pd.DataFrame(accounting_entries)
