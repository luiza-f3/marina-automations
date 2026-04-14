from Investiments.src.domain.asset_evolution.cashFlow import cashFlow
from Investiments.src.domain.wallet import Wallets

from dotenv import load_dotenv
import os
import pandas as pd

from Investiments.src.utils.tools import map_fund


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
        redemptions_applications_provisions, provisions = Wallets.prepare_provision(
            os.path.join(cls.base_path, 'Wallets', f'{cls.day}_{cls.mon}'))

        # essa saida será usada para somar com o saldo do dia anterior
        redemptions_applications_provisions_pre, aa = Wallets.prepare_provision(
            os.path.join(cls.base_path, 'Wallets', f'{cls.day_pre}_{cls.mon_pre}'))

        # retorna as carteiras todas unidas em um unico df acrescida de plano e perfil
        current_wallet = Wallets.prepare_wallets(os.path.join(cls.base_path, 'Wallets', f'{cls.day}_{cls.mon}'))
        previous_wallet = Wallets.prepare_wallets(os.path.join(cls.base_path, 'Wallets', f'{cls.day_pre}_{cls.mon_pre}'))

        previous_wallet = map_fund(current_wallet, previous_wallet)

        generate_report(redemptions_applications_provisions, current_wallet)

        current_wallet = pd,merge(current_wallet, redemptions_applications_provisions, left_on=['Fundo', 'Plano', 'Perfil'],
                                  right_on=['Despesa', 'Plano', 'Perfil'], how='left')
        current_wallet['Valor Atual'] = current_wallet['Valor Atual'].fillna(0) + current_wallet['Valor'].fillna(0)

        previous_wallet = pd.merge(previous_wallet, redemptions_applications_provisions_pre, left_on=['Fundo', 'Plano', 'Perfil'], right_on=['Despesa', 'Plano', 'Perfil'], how='left')
        previous_wallet['Valor Atual'] = previous_wallet['Valor Atual'].fillna(0) + previous_wallet['Valor'].fillna(0)

        cash_flow = cashFlow.prepare_cash_flow(os.path.join(cls.base_path, 'reports'), cls.dt_cash_flow)