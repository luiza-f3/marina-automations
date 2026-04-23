import sys
import pandas as pd
import os

class LoanInterestPosting:
    # Função para gerar o arquivo de lançamentos contábeis de rendimentos de empréstimos

    #Filtro de data para rendimentos yyyy-mm-dd
    date = "2026-01-01"
    year, month, day = date.split('-')
    file_name = f'Rendimentos_01.2026.xlsx'

    # Definindo o caminho absoluto do diretório do projeto
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_root, 'Documents', 'Consultas', file_name)
    path_loan_interest = file_path
    base_path = os.path.join(project_root, 'Documents', 'Rendimentos')
    path_save = os.path.join(base_path, f"rendimentoEmprestimos_protheus{day}-{month}.csv")

    # Contas contábeis, os valores sempre serão positivos, portanto a ordem é sempre débito e crédito
    debit_account = 10203080101010
    credit_account = 50108010100000

    # Inverter valores do "Rendimento" quando o resultado for negativo e transformá-los em positivo
    negative_debit_account = 50108010100000
    negative_credit_account = 10203080101010

    debit_credit_entries = []

    # De-para de planos
    plan = {
        "PREVISÃO": 51,
        "VISÃO MULTI": 8,
        "VISÃO TELEFÔNICA": 49,
        "TELEFÔNICA BD": 22
    }

    # De-para de perfis
    plan_profile = [{
        "PREVISÃO": {"PREVISÃO": 21},
        "TELEFÔNICA BD": {"TELEFÔNICA BD": 3},
        "VISÃO MULTI": {"AGRESSIVO": 26, "AGRESSIVO RF LP": 25, "CONSERVADOR": 23, "MODERADO": 24, "SUPER CONSER": 22},
        "VISÃO TELEFÔNICA": {"AGRESSIVO": 31, "AGRESSIVO RF LP": 30, "CONSERVADOR": 28, "MODERADO": 29, "SUPER CONSER": 27}
    }]

    # Checagem se o arquivo existe antes de ler
    if not os.path.exists(path_loan_interest):
        print(f"❌ Arquivo de rendimentos não encontrado: {path_loan_interest}")
        sys.exit()
    df_income = pd.read_excel(path_loan_interest)

    # Tratamento de tipos
    df_income.columns = df_income.columns.str.strip()
    df_income['Data'] = df_income["Data"].astype(str)
    df_income['Perfil'] = df_income['Perfil'].str.strip()

    if date not in df_income['Data'].values:
        print("❌ A Data não foi encontrada, seu arquivo não será gerado!")
        sys.exit()
    else:
        df_income = df_income[df_income["Data"] == date]
        df_income = df_income[["Data", "Plano", "Perfil", "Rendimento"]]

    # Inserindo campos
    df_income['CC'] = 9
    df_income['Patroc'] = '001'
    df_income['Historico do lancamento'] = 'APROP DE JUROS DO PROGRAMA DE EMPRESTIMO'
    df_income['Valor'] = df_income['Rendimento']

    # Excluindo campos
    df_income.drop(["Rendimento", 'Data'], inplace=True, axis=1)

    # De-Para de perfil
    for row_index, row in df_income.iterrows():
        for dict_plan in plan_profile:
            if row['Plano'] in dict_plan:
                df_income.at[row_index, 'Perfil'] = dict_plan[row['Plano']][row['Perfil']]
                break

    # De-Para de plano
    for index, row in df_income.iterrows():
        df_income.at[index, 'Plano'] = plan[row['Plano']]

    for index, row in df_income.iterrows():
        if row['Valor'] >= 0:
            debit_entry = row.copy()
            debit_entry['Conta contabil'] = debit_account
            debit_entry['D/C'] = 'D'

            credit_entry = row.copy()
            credit_entry['Conta contabil'] = credit_account
            credit_entry['D/C'] = 'C'
        else:
            debit_entry = row.copy()
            debit_entry['Conta contabil'] = negative_debit_account
            debit_entry['D/C'] = 'D'
            debit_entry['Valor'] = abs(row['Valor'])

            credit_entry = row.copy()
            credit_entry['Conta contabil'] = negative_credit_account
            credit_entry['D/C'] = 'C'
            credit_entry['Valor'] = abs(row['Valor'])

        debit_entry['Valor'] = abs(debit_entry['Valor'])
        credit_entry['Valor'] = abs(credit_entry['Valor'])

        debit_credit_entries.append(debit_entry)
        debit_credit_entries.append(credit_entry)

        result_df = pd.DataFrame(debit_credit_entries)

        additional_account = "10203080101020"
        additional_account_debit = "10203080101020"
        additional_account_credit = "10203080101010"

        new_entries = []

        for index, row in result_df.iterrows():
            if row ['Conta contabil'] == additional_account:
                debit_posting = row.copy()
                debit_posting['Conta contabil'] = additional_account_debit
                debit_posting['D/C'] = 'D'
                debit_posting['Valor'] = abs(row['Valor'])

                credit_posting = row.copy()
                credit_posting['Conta contabil'] = additional_account_credit
                credit_posting['D/C'] = 'C'
                credit_posting['Valor'] = abs(row['Valor'])

                new_entries.append(debit_posting)
                new_entries.append(credit_posting)

                result_df = pd.concat([[result_df], pd.DataFrame(new_entries)], ignore_index=True)

        result_df = result_df[['Conta contabil', 'Valor', 'D/C', 'Historico do lancamento', 'CC', 'Plano', 'Perfil', 'Patroc']]

        os.makedirs(base_path, exist_ok=True)
        result_df.to_csv(path_save, header=False, index=False, sep=';')

    print(f'✅ Arquivo gerado com sucesso! \nCaminho: {path_save}')
