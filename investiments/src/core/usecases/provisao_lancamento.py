import pandas as pd

from investiments.src.utils.tools import criar_lancamento_contabil
from investiments.src.utils.consultas.fees_accounts import fees_accounts
from investiments.src.utils.consultas.fees_info import fees_info

def provisao_lancamento(df_provisao):
    finalProtheus = []
    for index, row in df_provisao.iterrows():
        valor = row['Valor']
        plano = row['Plano']
        perfil = row['Perfil']
        despesa = row['Despesa']
        round(valor, 2)
        for taxa in fees_info:
            if taxa in despesa:
                lancamento1 = None
                lancamento2 = None

                if (plano, perfil) != (987, 19) and (plano, perfil) != (952, 20):
                    lancamento1 = criar_lancamento_contabil(fees_accounts[taxa]['Despesa'], abs(valor), 'D',
                                                            taxa,
                                                            plano, perfil)
                    lancamento2 = criar_lancamento_contabil(fees_accounts[taxa]['Plano'], abs(valor), 'C', taxa,
                                                            plano, perfil)

                if (plano, perfil) == (987, 19) or (plano, perfil) == (952, 20):
                    lancamento1 = criar_lancamento_contabil(fees_accounts[taxa]['Despesa'], abs(valor), 'D',
                                                            taxa,
                                                            plano, perfil)
                    lancamento2 = criar_lancamento_contabil(fees_accounts[taxa]['PGA'], abs(valor), 'C', taxa,
                                                            plano, perfil)

                # Adicionar os lançamentos apenas se eles não forem None
                if lancamento1:
                    finalProtheus.append(lancamento1)
                if lancamento2:
                    finalProtheus.append(lancamento2)
                break
    finalProtheus = pd.DataFrame(finalProtheus)
    return finalProtheus