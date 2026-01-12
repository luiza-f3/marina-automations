import sys

import pandas as pd
import os

# filtro de data para rendimentos yyyy-mm-dd
data = "2025-11-30"
ano, mes, dia = data.split('-')
file_name = 'Rendimentos_11.2025.xlsx'

documentos_path = os.path.join("Documents", "Rendimentos")

# definindo o caminho para os rendimentos de emprestimos
file_path = os.path.join('~','Documents', file_name)
path_rendimentos_emprestimos = os.path.expanduser(file_path)
base_path = os.path.expanduser(documentos_path)
path_save = os.path.join(base_path, f"rendimentoEmprestimos_protheus{dia}-{mes}.csv")

# contas contabeis, os valores sempre será positivo portando a ordem é sempre debito e credito
conta_debito = 10203080101010
conta_credito = 50108010100000

# !! Inverter valores do "Rendimento" quando o resultado for negativo e transformá-los em positivo
conta_debito_neg = 50108010100000
conta_credito_neg = 10203080101010

# armazenar debitos e creditos para depois transformar em um dataframe
lista_d_c = []

# de-para de planos
planos = {
    "PREVISÃO": 51,
    "VISÃO MULTI": 8,
    "VISÃO TELEFÔNICA": 49,
    "TELEFÔNICA BD": 22
}
# de-para de perfis
plano_perfil = [{
    "PREVISÃO": {"PREVISÃO": 21},
    "TELEFÔNICA BD": {"TELEFÔNICA BD": 3},
    "VISÃO MULTI": {"AGRESSIVO": 26, "AGRESSIVO RF LP": 25, "CONSERVADOR": 23, "MODERADO": 24, "SUPER CONSER": 22},
    "VISÃO TELEFÔNICA": {"AGRESSIVO": 31, "AGRESSIVO RF LP": 30, "CONSERVADOR": 28, "MODERADO": 29, "SUPER CONSER": 27}
}]

df_rendimentos = pd.read_excel(path_rendimentos_emprestimos)

# tratamento de tipos
df_rendimentos.columns = df_rendimentos.columns.str.strip()
df_rendimentos['Data'] = df_rendimentos["Data"].astype(str)
df_rendimentos['Perfil'] = df_rendimentos['Perfil'].str.strip()

# filtrando somente os dados necessários
if data not in df_rendimentos['Data'].values:
    print("A Data não foi encontrada, seu arquivo não será gerado!")
    sys.exit()
else:
    df_rendimentos = df_rendimentos[df_rendimentos["Data"] == data]
    df_rendimentos = df_rendimentos[["Data", "Plano", "Perfil", "Rendimento"]]

# inserindo campos
df_rendimentos['CC'] = 9
df_rendimentos['Patroc'] = '001'
df_rendimentos['Historico do lancamento'] = 'APROP DE JUROS DO PROGRAMA DE EMPRESTIMO'
df_rendimentos['Valor'] = df_rendimentos['Rendimento']

# excluindo campos
df_rendimentos.drop(["Rendimento", 'Data'], inplace=True, axis=1)

# de-para de perfil
for row_index, row in df_rendimentos.iterrows():
    for plano_dict in plano_perfil:
        if row['Plano'] in plano_dict:
            df_rendimentos.at[row_index, 'Perfil'] = plano_dict[row['Plano']][row['Perfil']]
            break

# de-para de planos
for index, row in df_rendimentos.iterrows():
    df_rendimentos.at[index, 'Plano'] = planos[row['Plano']]

lista_d_c = []  # Inicialize a lista para armazenar as novas linhas

# atribuindo contas contabies para debitos e creditos
for index, row in df_rendimentos.iterrows():
    # Crie uma cópia da linha original para débito

    if row['Valor'] >= 0 :
        debito = row.copy()
        debito['Conta contabil'] = conta_debito  # Adicione a conta de débito
        debito['D/C'] = 'D'  # Indique que é um débito

    # Crie uma cópia da linha original para crédito
        credito = row.copy()
        credito['Conta contabil'] = conta_credito  # Adicione a conta de crédito
        credito['D/C'] = 'C'  # Indique que é um crédito
    else:
        debito = row.copy()
        debito['Conta contabil'] = conta_debito_neg
        debito['D/C'] = 'D'

        credito = row.copy()
        credito['Conta contabil'] = conta_credito_neg
        credito['D/C'] = 'C'

#Garantindo que os valores sejam sempre positivos
    debito['Valor'] = abs(row['Valor'])
    credito['Valor'] = abs(row['Valor'])

    # Adicione as linhas de débito e crédito à lista
    lista_d_c.append(debito)
    lista_d_c.append(credito)

# Converta a lista de linhas em um DataFrame
df_final = pd.DataFrame(lista_d_c)

#Lançamentos adicionais na conta = 10203080101020
conta_adicional = "10203080101020"
conta_adicional_debito = "10203080101020"
conta_adicional_credito = "10203080101010"

novos_lancamentos = []

for index, row in df_final.iterrows():
    if row['Conta contabil'] == conta_adicional:
        # Cria o lançamento adicional de débito
        lancamento_debito = row.copy()
        lancamento_debito['Conta contabil'] = conta_adicional_debito
        lancamento_debito['D/C'] = 'D'
        lancamento_debito['Valor'] = abs(row['Valor'])  # Garantindo que o valor seja positivo

        # Cria o lançamento adicional de crédito
        lancamento_credito = row.copy()
        lancamento_credito['Conta contabil'] = conta_adicional_credito
        lancamento_credito['D/C'] = 'C'
        lancamento_credito['Valor'] = abs(row['Valor'])  # Garantindo que o valor seja positivo

        # Adiciona os lançamentos adicionais à lista
        novos_lancamentos.append(lancamento_debito)
        novos_lancamentos.append(lancamento_credito)

        df_final = pd.concat([df_final, pd.DataFrame(novos_lancamentos)], ignore_index=True)

# colocando dados em ordem
df_final = df_final[['Conta contabil', 'Valor', 'D/C', 'Historico do lancamento', 'CC', 'Plano', 'Perfil', 'Patroc'
]]

os.makedirs(base_path, exist_ok=True)
df_final.to_csv(path_save, header=False, index=False, sep=';')

print('Arquivos gerados com sucesso!')