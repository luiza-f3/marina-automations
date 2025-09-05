"""
import pandas as pd
import os
from datetime import datetime

def preparar_relatorio_consolidado(cash_flow_balance):
    
    Prepara relatório consolidado com formato específico:
    Data | Plano | Perfil | Histórico | Valores (Entrada/Saída/Saldo)
    
    dados = []
    
    for _, row in current_wallet.iterrows():
        # Obter dados básicos
        data = row['Data']
        plano = row['Plano']
        perfil = row['Perfil']
        cod_fundo = row['Cod Fundo']
        valor_atual = row['Valor Atual']
        
        # Obter saldo anterior
        saldo_anterior = 0
        if not previous_wallet.empty:
            saldo_anterior_row = previous_wallet[
                (previous_wallet['Cod Fundo'] == cod_fundo) &
                (previous_wallet['Plano'] == plano) &
                (previous_wallet['Perfil'] == perfil)
            ]
            if not saldo_anterior_row.empty:
                saldo_anterior = saldo_anterior_row.iloc[0]['Valor Atual']
        
        # Obter fluxos
        entrada = saida = 0
        if not cash_flow_balance.empty:
            fluxo_row = cash_flow_balance[
                (cash_flow_balance['Cod Fundo'] == cod_fundo) &
                (cash_flow_balance['Plano'] == plano) &
                (cash_flow_balance['Perfil'] == perfil)
            ]
            if not fluxo_row.empty:
                entrada = abs(fluxo_row.iloc[0]['Entrada'])
                saida = abs(fluxo_row.iloc[0]['Saida'])
        
        # Determinar tipo de movimento
        if entrada > 0:
            historico = "Aplicação"
            valor_movimento = entrada
        elif saida > 0:
            historico = "Resgate"
            valor_movimento = -saida
        else:
            historico = "Ajuste/Rendimento"
            valor_movimento = valor_atual - saldo_anterior
        
        dados.append({
            'Data': data,
            'Plano': plano,
            'Perfil': perfil,
            'Histórico': historico,
            'Valor': valor_movimento,
            'Saldo Anterior': saldo_anterior,
            'Saldo Atual': valor_atual
        })
    
    return pd.DataFrame(dados)

def gerar_relatorio_autoincrementado(cls, cash_flow):
    Gera relatório que se autoincrementa com novos dados
    # 1. Obter dados
    current_wallet = Carteira.preparar_carteiras(os.path.join(cls.base_path, 'Carteiras', f'{cls.day}_{cls.mon}'))
    previous_wallet = Carteira.preparar_carteiras(os.path.join(cls.base_path, 'Carteiras', 'arquivo_anterior.csv'))
    cash_flow_balance = FluxoDeCaixa.gerar_diferenca_entradas_saidas(cash_flow)
    
    # 2. Gerar novo relatório
    novo_relatorio = preparar_relatorio_consolidado(current_wallet, previous_wallet, cash_flow_balance)
    
    # 3. Caminhos dos arquivos
    PASTA_DESTINO = os.path.expanduser("~/Documents/relatorios_finais/")
    ARQUIVO_CONSOLIDADO = os.path.join(PASTA_DESTINO, "RELATORIO_CONSOLIDADO.csv")
    
    # 4. Verificar e carregar relatório existente
    if os.path.exists(ARQUIVO_CONSOLIDADO):
        relatorio_existente = pd.read_csv(ARQUIVO_CONSOLIDADO, sep=';')
        relatorio_final = pd.concat([relatorio_existente, novo_relatorio])
    else:
        relatorio_final = novo_relatorio
    
    # 5. Exportar
    relatorio_final.to_csv(ARQUIVO_CONSOLIDADO, index=False, sep=';', encoding='utf-8-sig')
    print(f"Relatório atualizado em: {ARQUIVO_CONSOLIDADO}")
    
    return relatorio_final

"""