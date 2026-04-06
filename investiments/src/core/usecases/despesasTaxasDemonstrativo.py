import os
import pandas as pd

from investiments.src.utils.consultas.fees_accounts import fees_accounts
from investiments.src.utils.tools import criar_lancamento_contabil

path_consulta_fundos = os.path.expanduser(os.getenv("CONSULTA_FUNDOS"))
df_fundos = pd.read_excel(path_consulta_fundos, sheet_name='para')


def despesas_taxas_demonstrativo(df_despesas):
    finalProtheus = []
    for index, row in df_despesas.iterrows():
        taxas = 'DESPESA - CUSTO CETIP', 'TAXA DE CONTROLADORIA', 'TAXA DE CUSTODIA', 'TAXA CETIP'
        fundo = row['Historico']
        plano = row['Plano']
        perfil = row['Perfil']
        saida = row['Saida']
        entrada = row['Entrada']
        contaContabil_carteira = df_fundos.loc[
            (df_fundos['Plano'] == plano) &
            (df_fundos['Perfil'] == perfil)
            ]['Investimentos'].values[0]

        # --- NOVA REGRA: ESTORNO DE TAXA CETIP ---

        if fundo in ['ESTORNO DE TAXA CETIP', 'ESTORNO TAXA CETIP']:
            valor = abs(entrada) if entrada != 0 else abs(saida)
            finalProtheus.append(criar_lancamento_contabil(fees_accounts['ESTORNO DE TAXA CETIP']['PGA'], valor, 'D',
                                                           'ESTORNO DE TAXA CETIP', plano, perfil))
            finalProtheus.append(
                criar_lancamento_contabil(contaContabil_carteira, valor, 'C', 'ESTORNO DE TAXA CETIP', plano, perfil))
            continue

        # -----------------------------------------


        if fundo == 'IOF':
            if entrada != 0:
                valor = abs(entrada)
                finalProtheus.append(criar_lancamento_contabil(
                    contaContabil_carteira, valor, 'D', fundo, plano, perfil))
                finalProtheus.append(criar_lancamento_contabil(
                    50204039800000, valor, 'C', fundo, plano,
                    perfil))
                continue
            if saida != 0:
                valor = abs(saida)
                finalProtheus.append(criar_lancamento_contabil(
                    50204039800000, valor, 'D', fundo, plano, perfil))
                finalProtheus.append(criar_lancamento_contabil(
                    contaContabil_carteira, valor, 'C', fundo, plano,
                    perfil))
                continue

        if (plano == 987 and perfil == 19) or (plano == 952 and perfil == 20):
            if entrada != 0:
                valor = abs(entrada)
                if fundo in taxas:
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        fees_accounts['DESPESA - CUSTO CETIP']['PGA'], valor, 'C', fundo, plano,
                        perfil))
                    continue
                if fundo == '(AJUSTE) TAXA CETIP' or fundo == 'Ajuste de Taxa SELIC':
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        fees_accounts['Taxa CETIP']['Despesa'], valor, 'C', fundo, plano, perfil))
                    continue
                if fundo == 'DESPESA B 10 - TARIFA DE LIQUIDACAO FINANCEIRA':
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        fees_accounts[fundo]['PGA'], valor, 'C', fundo, plano, perfil))
                    continue
                if fundo == '(AJUSTE) TARIFA DE LIQUIDACAO FINANCEIRA':
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        fees_accounts[fundo]['Despesa'], valor, 'C', fundo, plano, perfil))
                    continue
            if saida != 0:
                valor = abs(saida)
                if fundo in taxas:
                    finalProtheus.append(criar_lancamento_contabil(
                        fees_accounts['Taxa CETIP']['PGA'], valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'C', fundo, plano, perfil))
                    continue
                if fundo == '(AJUSTE) TAXA CETIP' or fundo == 'Ajuste de Taxa SELIC':
                    finalProtheus.append(criar_lancamento_contabil(
                        fees_accounts['Taxa CETIP']['Despesa'], valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'C', fundo, plano, perfil))
                    continue
                if fundo == 'DESPESA B 10 - TARIFA DE LIQUIDACAO FINANCEIRA':
                    finalProtheus.append(criar_lancamento_contabil(
                        fees_accounts[fundo]['PGA'], valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'C', fundo, plano, perfil))
                    continue
                if fundo == '(AJUSTE) TARIFA DE LIQUIDACAO FINANCEIRA':
                    finalProtheus.append(criar_lancamento_contabil(
                        fees_accounts[fundo]['Despesa'], valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'C', fundo, plano, perfil))
                    continue
        else:
            if entrada != 0:
                valor = abs(entrada)
                if fundo in taxas:
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        fees_accounts['Taxa CETIP']['Plano'], valor, 'C', fundo, plano, perfil))
                    continue
                if fundo == '(AJUSTE) TAXA CETIP' or fundo == 'Ajuste de Taxa SELIC':
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        fees_accounts['Taxa CETIP']['Despesa'], valor, 'C', fundo, plano, perfil))
                    continue
                if fundo == 'DESPESA B 10 - TARIFA DE LIQUIDACAO FINANCEIRA':
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        fees_accounts[fundo]['Plano'], valor, 'C', fundo, plano,
                        perfil))
                    continue
                if fundo == '(AJUSTE) TARIFA DE LIQUIDACAO FINANCEIRA':
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        fees_accounts[fundo]['Despesa'], valor, 'C', fundo, plano,
                        perfil))
                    continue
            if saida != 0:
                valor = abs(saida)
                if fundo in taxas:
                    finalProtheus.append(criar_lancamento_contabil(
                        fees_accounts['Taxa CETIP']['Plano'], valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'C', fundo, plano, perfil))
                    continue
                if fundo == '(AJUSTE) TAXA CETIP' or fundo == 'Ajuste de Taxa SELIC':
                    finalProtheus.append(criar_lancamento_contabil(
                        fees_accounts['Taxa CETIP']['Despesa'], valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'C', fundo, plano, perfil))
                    continue
                if fundo == 'DESPESA B 10 - TARIFA DE LIQUIDACAO FINANCEIRA':
                    finalProtheus.append(criar_lancamento_contabil(
                        fees_accounts[fundo]['Plano'], valor, 'D', fundo, plano,
                        perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'C', fundo, plano, perfil))
                    continue
                if fundo == '(AJUSTE) TARIFA DE LIQUIDACAO FINANCEIRA':
                    finalProtheus.append(criar_lancamento_contabil(
                        fees_accounts[fundo]['Despesa'], valor, 'D', fundo, plano,
                        perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'C', fundo, plano, perfil))
                    continue
    finalProtheus = pd.DataFrame(finalProtheus)
    return finalProtheus
