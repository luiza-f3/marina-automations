from investiments.src.domain.asset_evolution.cash_flow import cashFlow
from investiments.src.domain.wallet.wallets import Wallets
from investiments.src.use_cases.accounting.prepare_accounting_entries import prepare_accounting_entries
from investiments.src.use_cases.accounting.provision_entries import provision_entries
from investiments.src.use_cases.asset_evolution.prepare_equity_changes import prepare_equity_changes
from investiments.src.use_cases.expanses.statement_fee_expenses import statement_fee_expenses
from investiments.src.use_cases.reports.generate_statement import process_statements
from investiments.src.utils.tools import map_fund, save_accounting_outputs
from investiments.src.use_cases.reports.generate_report import generate_report

from dotenv import load_dotenv
import os
import pandas as pd

class InvestimentService:
    load_dotenv()
    base_path = os.path.expanduser(os.getenv("BASE_PATH"))
    year, mon, day = os.getenv('CURRENT_DATE').split('-')
    year_pre, mon_pre, day_pre = os.getenv('PREVIOUS_DATE').split('-')
    dt_cash_flow = f'{day}/{mon}/{year}'
    execute_provision = os.getenv('PROVISION')

    @classmethod
    def prepareInvestments(cls):
        """Prepara a planilha de contabilização de investimentos e planilha de evolução patrimonial"""

        # separa provisões e entradas presente no rodapé das carteiras
        redemptions_applications_provisions, provisions = Wallets.prepare_provisions(
            os.path.join(cls.base_path, 'Carteiras', f'{cls.day}_{cls.mon}'))

        # essa saida será usada para somar com o saldo do dia anterior
        redemptions_applications_provisions_pre, aa = Wallets.prepare_provisions(
            os.path.join(cls.base_path, 'Carteiras', f'{cls.day_pre}_{cls.mon_pre}'))

        # retorna as carteiras todas unidas em um unico df acrescida de plano e perfil
        current_wallet = Wallets.prepare_wallets(os.path.join(cls.base_path, 'Carteiras', f'{cls.day}_{cls.mon}'))
        previous_wallet = Wallets.prepare_wallets(os.path.join(cls.base_path, 'Carteiras', f'{cls.day_pre}_{cls.mon_pre}'))

        previous_wallet = map_fund(current_wallet, previous_wallet)

        generate_report(redemptions_applications_provisions, current_wallet)

        current_wallet = pd.merge(current_wallet, redemptions_applications_provisions, left_on=['Fundo', 'Plano', 'Perfil'], right_on=['Despesa', 'Plano', 'Perfil'], how='left')

        current_wallet['Valor Atual'] = (
                pd.to_numeric(current_wallet['Valor Atual'], errors='coerce').fillna(0) +
                pd.to_numeric(current_wallet['Valor'], errors='coerce').fillna(0)
        )

        previous_wallet = pd.merge( previous_wallet, redemptions_applications_provisions_pre, left_on=['Fundo', 'Plano', 'Perfil'], right_on=['Despesa', 'Plano', 'Perfil'], how='left')

        previous_wallet['Valor Atual'] = (
                pd.to_numeric(previous_wallet['Valor Atual'], errors='coerce').fillna(0) +
                pd.to_numeric(previous_wallet['Valor'], errors='coerce').fillna(0)
        )

        cash_flow = cashFlow.prepare_cash_flow(os.path.join(cls.base_path, 'Demonstrativos'), cls.dt_cash_flow)

        result = process_statements(
            cash_flow=cash_flow,
            reference_date=cls.dt_cash_flow,
            base_path=cls.base_path
        )

        if result:
            print("[OK] Processamento dos demonstrativos concluido com sucesso.")
        else:
            print("[ERRO] Ocorreu um erro durante o processamento dos demonstrativos.")

        # Totaliza o fluxo de caixa
        cash_flow = cashFlow.totalize_cash_flow(cash_flow)

        # Filtra registros (separa RESGATE/AQUISICAO DE COTAS e despesas)
        acquisition_redemption, cash_flow, expenses = cashFlow.filter_records(cash_flow)

        # Gera a diferença entre entrada e saída para evolução patrimonial (após filtro)
        cash_flow_balance = cashFlow.generate_inflow_outflow_difference(cash_flow)

        assetEvolutuion = prepare_equity_changes(current_wallet, previous_wallet, cash_flow_balance)

        income_accouting = prepare_accounting_entries(assetEvolutuion, cash_flow)

        cash_flow_tax_accounting = statement_fee_expenses(expenses)

        provisions_accounting = pd.DataFrame()
        if (cls.execute_provision == 'True') and not provisions.empty:
            provisions_accounting = provision_entries(provisions)

        save_accounting_outputs(assetEvolutuion, income_accouting, cash_flow_tax_accounting, provisions_accounting, cls.base_path, cls.day, cls.mon)