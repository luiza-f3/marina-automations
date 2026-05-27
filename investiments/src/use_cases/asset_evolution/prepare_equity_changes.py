import pandas as pd

# Calcula a evolução patrimonial de cada fundo, gerando relatório de rendimentos, Compara carteira atual, carteira anterior e fluxo de caixa para gerar saldos, movimentações e rendimento do período.
def prepare_equity_changes(current_wallet, previous_wallet, cash_flow_balance):
    fund_list = []
    plan_list = []
    profile_list = []
    classification_list = []
    current_value_list = []
    previous_balance_list = []
    inflow_list = []
    outflow_list = []
    income_list = []
    fund_code_list = []

    # PROCESSAMENTO DOS FUNDOS DA CARTEIRA ATUAL (Itera sobre cada fundo da carteira atual, buscando saldo anterior e movimentações para calcular rendimento.)
    for _, row in current_wallet.iterrows():
        fund = row['Fundo']
        plan = row['Plano']
        profile = row['Perfil']
        current_value = row['Valor Atual']
        classification = row['Classificacao']
        fund_code = row['Cod Fundo']

        # BUSCA DO SALDO ANTERIOR (Localiza o mesmo fundo na carteira anterior por código, plano e perfil.)
        previous_balance_row = previous_wallet[
            (previous_wallet['Cod Fundo'] == fund_code) &
            (previous_wallet['Plano'] == plan) &
            (previous_wallet['Perfil'] == profile)
        ]

        if not previous_balance_row.empty:
            previous_balance = previous_balance_row.iloc[0]["Valor Atual"]
        else:
            previous_balance = 0

        # BUSCA DO FLUXO DE CAIXA (Localiza movimentações do mesmo fundo por código, plano e perfil.)
        if not cash_flow_balance.empty:
            cash_flow_row = cash_flow_balance[
                (cash_flow_balance['Cod Fundo'] == fund_code) &
                (cash_flow_balance['Plano'] == plan) &
                (cash_flow_balance['Perfil'] == profile)
            ]
        else:
            cash_flow_row = pd.DataFrame()

        if not cash_flow_row.empty:
            inflow = cash_flow_row.iloc[0]['Entrada']
            outflow = cash_flow_row.iloc[0]['Saida']
        else:
            inflow = 0
            outflow = 0

        # CÁLCULO DO RENDIMENTO (Calcula rendimento considerando saldo anterior, movimentações e saldo atual.)
        income = current_value - previous_balance + inflow + outflow

        # ACUMULAÇÃO DOS DADOS (Adiciona os dados processados às listas para montagem do DataFrame final.)
        fund_list.append(fund)
        plan_list.append(plan)
        profile_list.append(profile)
        classification_list.append(classification)
        current_value_list.append(current_value)
        previous_balance_list.append(previous_balance)
        inflow_list.append(-outflow)
        outflow_list.append(-inflow)
        income_list.append(income)
        fund_code_list.append(fund_code)

    # MONTAGEM DO DATAFRAME FINAL (Cria um DataFrame consolidado com os dados processados para geração de relatórios e análises.)
    final_df = pd.DataFrame({
        'Fundo': fund_list,
        'Cod Fundo': fund_code_list,
        'Plano': plan_list,
        'Perfil': profile_list,
        'Classificacao': classification_list,
        'Saldo Anterior': previous_balance_list,
        'Entrada': inflow_list,
        'Saida': outflow_list,
        'Saldo Atual': current_value_list,
        'Rendimento': income_list
    })

    return final_df
