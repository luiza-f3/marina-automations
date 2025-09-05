import pandas as pd
import os

from benefits_sheet.utils.AccountingAccount import AccountingAccount
from src.Emprestimos import Emprestimos
from src.Provisao import Provisao
from src.Deducao import Deducao
from src.ContabilizarBeneficios import ContabilizarBeneficios
from utils.tools import limparTexto

data_pagamento = "2025-07-02"

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