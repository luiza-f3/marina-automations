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

        # EXTRAÇÃO DE PROVISÕES E MOVIMENTAÇÕES DO DIA ATUAL E ANTERIOR (Lê todos os arquivos de carteira e separa rodapé em duas planilhas: redemptions_applications_provisions (resgates/aplicações) e provisions (taxas/custódia).)
        redemptions_applications_provisions, provisions = Wallets.prepare_provisions(
            os.path.join(cls.base_path, 'Carteiras', f'{cls.day}_{cls.mon}'))

        # EXTRAÇÃO DE PROVISÕES DA CARTEIRA ANTERIOR (Mantém consistência no cálculo de rendimento.)
        redemptions_applications_provisions_pre, aa = Wallets.prepare_provisions(
            os.path.join(cls.base_path, 'Carteiras', f'{cls.day_pre}_{cls.mon_pre}'))

        #CONSOLIDAÇÃO DAS CARTEIRAS (Lê os arquivos .xls, consolida posições e padroniza nomes dos fundos para evitar divergências de cálculo.)
        current_wallet = Wallets.prepare_wallets(os.path.join(cls.base_path, 'Carteiras', f'{cls.day}_{cls.mon}'))

        #EXTRAÇÃO DA CARTEIRA DO DIA ANTERIOR (Utilizada como saldo anterior no cálculo de rendimento.)
        previous_wallet = Wallets.prepare_wallets(os.path.join(cls.base_path, 'Carteiras', f'{cls.day_pre}_{cls.mon_pre}'))

        # SINCRONIZAÇÃO DE NOMES ENTRE CARTEIRAS (Padroniza nomes dos fundos entre current_wallet e previous_wallet para garantir associação correta dos dados e evitar divergências de cálculo.)
        previous_wallet = map_fund(current_wallet, previous_wallet)

        # GERAÇÃO DE RELATÓRIO DE PROVISÕES (Consolida provisões e movimentações em relatório Excel para conferência e suporte de auditoria.)
        generate_report(redemptions_applications_provisions, current_wallet)

        # AJUSTE DE SALDO DA CARTEIRA ATUAL (Relaciona provisões e movimentações à carteira atual para refletir a posição real investida.)
        current_wallet = pd.merge(current_wallet, redemptions_applications_provisions, left_on=['Fundo', 'Plano', 'Perfil'], right_on=['Despesa', 'Plano', 'Perfil'], how='left')

        # ATUALIZAÇÃO DO SALDO DA CARTEIRA (Soma movimentações pendentes ao valor atual da carteira com tratamento de valores inválidos.)
        current_wallet['Valor Atual'] = (
                pd.to_numeric(current_wallet['Valor Atual'], errors='coerce').fillna(0) +
                pd.to_numeric(current_wallet['Valor'], errors='coerce').fillna(0)
        )

        # AJUSTE DE SALDO DA CARTEIRA ANTERIOR (Aplica a mesma regra da carteira atual para garantir consistência no cálculo de rendimento.)
        previous_wallet = pd.merge( previous_wallet, redemptions_applications_provisions_pre, left_on=['Fundo', 'Plano', 'Perfil'], right_on=['Despesa', 'Plano', 'Perfil'], how='left')

        previous_wallet['Valor Atual'] = (
                pd.to_numeric(previous_wallet['Valor Atual'], errors='coerce').fillna(0) +
                pd.to_numeric(previous_wallet['Valor'], errors='coerce').fillna(0)
        )

        # PROCESSAMENTO DO FLUXO DE CAIXA (Lê demonstrativos, filtra registros da data atual, identifica fundos e consolida movimentações em um único DataFrame.)
        cash_flow = cashFlow.prepare_cash_flow(os.path.join(cls.base_path, 'Demonstrativos'), cls.dt_cash_flow)

        # GERAÇÃO DO RELATÓRIO DE DEMONSTRATIVOS (Formata, consolida e salva histórico dos demonstrativos processados para conferência e auditoria.)
        result = process_statements(
            cash_flow=cash_flow,
            reference_date=cls.dt_cash_flow,
            base_path=cls.base_path
        )

        if result:
            print("[OK] Processamento dos demonstrativos concluido com sucesso.")
        else:
            print("[ERRO] Ocorreu um erro durante o processamento dos demonstrativos.")

        # TOTALIZAÇÃO DO FLUXO DE CAIXA (Agrupa movimentações por fundo, plano e perfil, mantendo taxas e despesas separadas para rastreabilidade.)
        cash_flow = cashFlow.totalize_cash_flow(cash_flow)

        # FILTRAGEM DO FLUXO DE CAIXA (Separa movimentações de cotas, despesas e demais registros para aplicação das regras contábeis específicas.)
        acquisition_redemption, cash_flow, expenses = cashFlow.filter_records(cash_flow)

        # CÁLCULO DO BALANÇO LÍQUIDO (Consolida entradas e saídas por fundo, mantendo apenas o valor líquido da movimentação.) # Output: DataFrame [Historico, Cod Fundo, Entrada, Saida, Plano, Perfil]
        cash_flow_balance = cashFlow.generate_inflow_outflow_difference(cash_flow)

        # CÁLCULO DA EVOLUÇÃO PATRIMONIAL (Calcula saldo anterior, movimentações, saldo atual e rendimento por fundo para base de contabilização.) # Output: DataFrame [Fundo, Cod Fundo, Plano, Perfil, Classificacao, Saldo Anterior, Entrada, Saida, Saldo Atual, Rendimento]
        assetEvolutuion = prepare_equity_changes(current_wallet, previous_wallet, cash_flow_balance)

        # GERAÇÃO DE LANÇAMENTOS CONTÁBEIS (Converte rendimentos e movimentações em débitos e créditos para importação no Protheus.) # Output: DataFrame [Conta Contabil, Valor, D/C, Historico, CC, Plano, Perfil]
        income_accouting = prepare_accounting_entries(assetEvolutuion, cash_flow)

        # GERAÇÃO DE LANÇAMENTOS DE DESPESAS E TAXAS (Classifica despesas, busca contas contábeis e gera débitos/créditos para contabilização.)
        cash_flow_tax_accounting = statement_fee_expenses(expenses)

        # INICIALIZAÇÃO DOS LANÇAMENTOS DE PROVISÕES (Garante a existência do DataFrame mesmo sem processamento.)
        provisions_accounting = pd.DataFrame()
        
        # PROCESSAMENTO DAS PROVISÕES (Gera lançamentos apenas quando habilitado e houver provisões válidas.)
        if (cls.execute_provision == 'True') and not provisions.empty:
            provisions_accounting = provision_entries(provisions)

        # GRAVAÇÃO DOS ARQUIVOS DE SAÍDA Consolida todos os lançamentos contábeis e dados processados e gera os arquivos finais.
        save_accounting_outputs(assetEvolutuion, income_accouting, cash_flow_tax_accounting, provisions_accounting, cls.base_path, cls.day, cls.mon)
