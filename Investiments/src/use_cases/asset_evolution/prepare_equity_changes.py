import pandas as pd

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

    for _, row in current_wallet.iterrows():
        fund = row['Fundo']
        plan = row['Plano']
        profile = row['Perfil']
        current_value = row['Valor Atual']
        classification = row['Classificacao']
        fund_code = row['Cod Fundo']

        previous_balance_row = previous_wallet[
            (previous_wallet['Cod Fundo'] == fund_code) &
            (previous_wallet['Plano'] == plan) &
            (previous_wallet['Perfil'] == profile)
        ]

        if not previous_balance_row.empty:
            previous_balance = previous_balance_row.iloc[0]["Valor Atual"]
        else:
            previous_balance = 0

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

        if inflow != 0 or outflow != 0:
            inflow *= -1
            outflow *= -1

        income = current_value - previous_balance - inflow - outflow

        fund_list.append(fund)
        plan_list.append(plan)
        profile_list.append(profile)
        classification_list.append(classification)
        current_value_list.append(current_value)
        previous_balance_list.append(previous_balance)
        inflow_list.append(inflow)
        outflow_list.append(outflow)
        income_list.append(income)
        fund_code_list.append(fund_code)

        final_df = pd.DataFrame({
            'Fundo': fund_list,
            'Cod Fundo': fund_code_list,
            'Plano': plan_list,
            'Perfil': profile_list,
            'Classificacao': classification_list,
            'Saldo Anterior': previous_balance_list,
            'Entrada': inflow_list,
            'Saida': outflow_list,
            'Valor Atual': current_value_list,
            'Rendimento': income_list
        })

        return final_df