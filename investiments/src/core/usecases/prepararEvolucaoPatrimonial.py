import pandas as pd

def prepararEvolucaoPatrimonial(current_wallet, previous_wallet, cash_flow_balance):
    """Prepara o relatorio diário de evolucao patrimonial"""
    # Crie listas para armazenar os dados
    fundo_lista = []
    plano_lista = []
    perfil_lista = []
    classificacao_lista = []
    valor_atual_lista = []
    saldo_anterior_lista = []
    entrada_lista = []
    saida_lista = []
    rendimento_lista = []  # Lista para armazenar o rendimento
    codigo_fundo_lista = []

    # Itera pelas linhas do DataFrame de carteira
    for index, row in current_wallet.iterrows():
        fundo = row['Fundo']
        plano = row['Plano']
        perfil = row['Perfil']
        valor_atual = row['Valor Atual']
        classe = row['Classificacao']
        codigo_fundo = row['Cod Fundo']

        # Verifica se há uma correspondência no DataFrame de saldo anterior
        saldo_anterior_row = previous_wallet[
            (previous_wallet['Cod Fundo'] == codigo_fundo) & (previous_wallet['Plano'] == plano)
            & (previous_wallet['Perfil'] == perfil)
            ]

        if not saldo_anterior_row.empty:
            saldo_anterior = saldo_anterior_row.iloc[0]["Valor Atual"]
        else:
            saldo_anterior = 0

        if not cash_flow_balance.empty:
            # Verifica se há uma correspondência no DataFrame de resultados
            resultados_row = cash_flow_balance[(cash_flow_balance['Cod Fundo'] == codigo_fundo) &
                                               (cash_flow_balance['Plano'] == plano) &
                                               (cash_flow_balance['Perfil'] == perfil)]
        else:
            resultados_row = pd.DataFrame()
        if not resultados_row.empty:
            entrada = resultados_row.iloc[0]['Saida']
            saida = resultados_row.iloc[0]['Entrada']
        else:
            entrada = 0
            saida = 0

        if entrada != 0 or saida != 0:
            entrada = entrada * -1
            saida = saida * -1

        rendimento = valor_atual - saldo_anterior - entrada - saida  # Calcula o rendimento

        # Adicione os dados às listas
        fundo_lista.append(fundo)
        plano_lista.append(plano)
        perfil_lista.append(perfil)
        classificacao_lista.append(classe)
        valor_atual_lista.append(valor_atual)
        saldo_anterior_lista.append(saldo_anterior)
        entrada_lista.append(entrada)
        saida_lista.append(saida)
        codigo_fundo_lista.append(codigo_fundo)
        rendimento_lista.append(rendimento)


    # Crie um DataFrame final a partir das listas, incluindo a coluna 'Rendimento'
    df_final = pd.DataFrame({
        'Fundo': fundo_lista,
        'Cod Fundo': codigo_fundo_lista,
        'Plano': plano_lista,
        'Perfil': perfil_lista,
        'Classificacao': classificacao_lista,
        'Saldo Anterior': saldo_anterior_lista,
        'Entrada': entrada_lista,
        'Saida': saida_lista,
        'Saldo Atual': valor_atual_lista,
        'Rendimento': rendimento_lista
    })
    return df_final