import pandas as pd
import os
from datetime import datetime
from benefits_sheet.utils.AccountingAccount import AccountingAccount
from src.Emprestimos import Emprestimos
from src.Provisao import Provisao
from src.Deducao import Deducao
from src.ContabilizarBeneficios import ContabilizarBeneficios
from utils.tools import limparTexto

data_pagamento = "2025-07-29"

BASE_PATH = os.path.expanduser('~\\Documents')
beneficios = os.path.join(BASE_PATH, 'data', 'processed', 'folha_beneficios_processado.csv')

consulta_beneficios_path = os.path.join(BASE_PATH, 'Beneficios' , 'consulta_folha_beneficios.xlsx')

year, month, day = data_pagamento.split('-')
data_competencia = f'{month}-{year}'
data_br = f'{day}-{month}-{year}'

if __name__ == "__main__":
    consulta_beneficios = pd.read_excel(consulta_beneficios_path,sheet_name="Planilha2")
    df = pd.read_csv(beneficios)

    df = df[df['Data de pagamento'] == data_pagamento]

    # padronização de valores na planilha de consulta
    consulta_beneficios = limparTexto(consulta_beneficios,
                                      ['Tipo de folha', 'Item folha', 'Grupo de beneficio',
                                       'Tipo de beneficio'])

    emprestimos = Emprestimos(df, data_competencia).criarEmprestimos()
    provisao = Provisao(df, data_competencia).criarProvisao()
    deducao = Deducao(df, data_competencia, consulta_beneficios).criarDeducao()

    # --- Validação de valores na Planilha2 ---
    colunas_verificar = ['Tipo de beneficio', 'Item folha']  # Colunas que você quer conferir
    colunas_ok_geral = []

    for df_nome, df_lanc in [("Deducao", deducao), ("Emprestimos", emprestimos), ("Provisao", provisao)]:
        if df_lanc.empty:
            print(f"⚠️ DataFrame {df_nome} está vazio, nenhuma validação necessária")
            continue

        ausentes = []
        for col in colunas_verificar:
            df_lanc_col = df_lanc[col].astype(str).str.strip().str.upper()
            consulta_col = consulta_beneficios[col].astype(str).str.strip().str.upper()

            for idx, valor in df_lanc_col.items():
                if valor not in consulta_col.values:
                    data_lanc = df_lanc.loc[idx, "Data de pagamento"]
                    ausentes.append(
                        f'"{valor}" - {col} - Data = {datetime.strptime(data_lanc, "%Y-%m-%d").strftime("%d/%m/%Y")}')

            if not any(v for v in ausentes if col in v) and col not in colunas_ok_geral:
                colunas_ok_geral.append(col)

        if ausentes:
            print(f"⚠️ Colunas e valores ausentes no {df_nome}:")
            for aviso in ausentes:
                print(aviso)

    if colunas_ok_geral:
        print(f"✅ Colunas com todos os valores presentes: {', '.join(colunas_ok_geral)}")
    # --- Fim da validação ---

    beneficios_contabilizado = ContabilizarBeneficios(deducao, emprestimos, provisao, consulta_beneficios, data_pagamento, data_competencia).contabilizar()

    beneficios_contabilizado = beneficios_contabilizado.loc[beneficios_contabilizado["Valor"] != 0]
    beneficios_contabilizado = AccountingAccount().duplicar_lancamentos_para_conta(beneficios_contabilizado)
    # beneficios_contabilizado['Data'] = pd.to_datetime(beneficios_contabilizado['Data'])

    beneficios_contabilizado["Valor"] = beneficios_contabilizado["Valor"].abs()

    beneficios_contabilizado['Data'] = data_br
    beneficios_contabilizado['Patrocinadora'] = beneficios_contabilizado['Patrocinadora'].apply(lambda x: str(x).zfill(3))


    # dataframes_por_data = {data: grupo for data, grupo in beneficios_contabilizado.groupby('Data')}

    # for data, df_grupo in dataframes_por_data.items():
    #     # Formatando a data para ser usada no nome do arquivo
    #     data_str = data.strftime('%d-%m-%Y')
    #     df_grupo["Data"] = data_str
    #     file_name = rf"C:\Users\WevertonRodriguesBar\Documents\data_preprocessing\data\processed\folha_contabilizada{data_str}.xlsx"

        # Salvando o DataFrame como um arquivo Excel
        # df_grupo.sort_values(by=['Plano', 'Perfil', 'Valor', 'D/C'], ascending=[True, True, True, False])
        # df_grupo.to_excel(file_name, index=False)
        # print(f"Arquivo salvo: {file_name}")

beneficios_contabilizado = beneficios_contabilizado.sort_values(by=['Plano', 'Perfil', 'Valor', 'D/C'], ascending=[True, True, True, False])
beneficios_contabilizado.to_excel(os.path.join(BASE_PATH,'Beneficios', f'folha_contabilizada{data_br}.xlsx'), index=False)
print('Folha gerada com sucesso')