from dotenv import load_dotenv
import pandas as pd
import os

from investiments.src.core.carteira.carteira import Carteira
from investiments.src.core.demonstrativo.fluxo_caixa import FluxoDeCaixa
from investiments.src.core.usecases.despesasTaxasDemonstrativo import despesas_taxas_demonstrativo
from investiments.src.core.usecases.prepararLancamentoContabil import processarLancamentoContabil
from investiments.src.core.usecases.provisao_lancamento import provisao_lancamento
from investiments.src.core.usecases.prepararEvolucaoPatrimonial import prepararEvolucaoPatrimonial
from investiments.src.core.usecases.reports.gerarRelatorio import gerarRelatorio
from investiments.src.core.usecases.reports.gerarRelatorioDemonstrativo import gerarRelatorioDemonstrativo, processarDemonstrativos
from investiments.src.utils.tools import save_data, mapear_fundo


class InvestimentosService:
    load_dotenv()
    base_path = os.path.expanduser(os.getenv("BASE_PATH"))
    year, mon, day = os.getenv('DATA_ATUAL').split('-')
    year_pre, mon_pre, day_pre = os.getenv('DATA_ANTERIOR').split('-')
    dt_cash_flow = f'{day}/{mon}/{year}'
    execute_provision = os.getenv('PROVISAO')

    @classmethod
    def prepararInvestimentos(cls):
        """Prepara planilha de contabilização de investimentos e planilha d e evolução patrimonial"""

        # separa provisões e entradas presente no rodapé das carteiras
        redemptions_applications_provisions, provisions = Carteira.preparar_provisao(
            os.path.join(cls.base_path, 'Carteiras', f'{cls.day}_{cls.mon}'))

        # essa saida será usada para somar com o saldo do dia anterior
        redemptions_applications_provisions_pre, aa = Carteira.preparar_provisao(
            os.path.join(cls.base_path, 'Carteiras', f'{cls.day_pre}_{cls.mon_pre}'))

        # retorna as carteiras todas unidas em um unico df acrescida de plano e perfil
        current_wallet = Carteira.preparar_carteiras(os.path.join(cls.base_path, 'Carteiras', f'{cls.day}_{cls.mon}'))
        previous_wallet = Carteira.preparar_carteiras(os.path.join(cls.base_path, 'Carteiras', f'{cls.day_pre}_{cls.mon_pre}'))

        previous_wallet = mapear_fundo(current_wallet, previous_wallet)

        # gerar um relatorio
        gerarRelatorio(redemptions_applications_provisions, current_wallet)

        # junta os valores de entrada presente no rodapé dá carteira com o valor atual do respectivo fundo
        current_wallet = pd.merge(current_wallet, redemptions_applications_provisions, left_on=['Fundo', 'Plano', 'Perfil'],
                                  right_on=['Despesa', 'Plano', 'Perfil'], how='left')
        current_wallet['Valor Atual'] = current_wallet['Valor Atual'].fillna(0) + current_wallet['Valor'].fillna(0)

        previous_wallet = pd.merge(previous_wallet, redemptions_applications_provisions_pre, left_on=['Fundo', 'Plano', 'Perfil'],
                                  right_on=['Despesa', 'Plano', 'Perfil'], how='left')
        previous_wallet['Valor Atual'] = previous_wallet['Valor Atual'].fillna(0) + previous_wallet['Valor'].fillna(0)

        # retorna todos demontrativos separados pela data passada no .env em um unico DF acrescido de plano e perfil
        cash_flow = FluxoDeCaixa.preparar_fluxo_caixa(os.path.join(cls.base_path, 'demonstrativos'), cls.dt_cash_flow)

        resultado = processarDemonstrativos(
            cash_flow=cash_flow,
            dt_referencia=cls.dt_cash_flow,
            base_path=cls.base_path  # Passar base_path da classe
        )

        # 3. Verificar resultado
        if resultado:
            print("✅ Processamento concluído com sucesso!")
        else:
            print("❌ Ocorreram erros durante o processamento")

        # Demonstração Financeira de Entradas e Saídas, Agrupadas por Fundos/Taxas Iguais
        cash_flow = FluxoDeCaixa.totalizar_entrada_saida(cash_flow)

        # diferença entre entradas e saidas do fluxo de caixa. Obs: será usado para registro no balanço patrimonial
        cash_flow_balance = FluxoDeCaixa.gerar_diferenca_entradas_saidas(cash_flow)

        # dataframes com registro de resgates e aquisições, demontrativo(fundos) e despesas
        acquisition_redemption, cash_flow, expenses = FluxoDeCaixa.filtrar_registros(cash_flow)

        assetEvolution = prepararEvolucaoPatrimonial(current_wallet, previous_wallet, cash_flow_balance)


        ### contabilização ###
        # contabilização balanço patrimonial (rentabilidade) #
        income_accounting = processarLancamentoContabil(assetEvolution, cash_flow)

        cash_flow_tax_accounting = despesas_taxas_demonstrativo(expenses)

        provisions_accouting = pd.DataFrame()
        if (cls.execute_provision == 'True'):
            provisions_accouting = provisao_lancamento(provisions)

        save_data(assetEvolution, income_accounting, cash_flow_tax_accounting, provisions_accouting, cls.base_path, cls.day, cls.mon)

    def prepararContabilizacaoInvestimentos(self):
        """Prepara o relatorio de partida dobrada para rendimento, despesas, provisao, entrada e saida de fundos,
        e resgates e aplicações"""

        ...
