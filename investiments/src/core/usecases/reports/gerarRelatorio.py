from dotenv import load_dotenv
import os

load_dotenv()
base_path = os.path.expanduser(os.getenv("BASE_PATH"))
year, mon, day = os.getenv('DATA_ATUAL').split('-')
dt_cash_flow = f'{day}/{mon}/{year}'
execute_provision = os.getenv('PROVISAO')

def gerarRelatorio(df_provision, wallet):
    """Gerar relatórios"""
    investiments_path = os.path.join(base_path, 'investimentos')
    os.makedirs(investiments_path, exist_ok=True)

    provisao_ant_copy = df_provision.groupby(['Plano', 'Perfil'])['Valor'].sum().reset_index()

    relatorio_conciliacao = wallet.groupby(['Plano', 'Perfil'])['Valor Atual'].sum().reset_index()
    relatorio_conciliacao = relatorio_conciliacao.merge(provisao_ant_copy, on=['Plano', 'Perfil'], how='left')
    relatorio_conciliacao['Valor'].fillna(0, inplace=True)
    relatorio_conciliacao['Total'] = relatorio_conciliacao[['Valor Atual', 'Valor']].sum(axis=1)

    relatorio_conciliacao['Dia'] = f'{day}/{mon}'
    relatorio_conciliacao.rename(columns={'Valor Atual': 'Total liquido', 'Valor': 'Total contas a receber'},
                                 inplace=True)

    relatorio_conciliacao.drop('Despesa', axis=1, inplace=True, errors='ignore')

    # ordenando os campos
    relatorio_conciliacao = relatorio_conciliacao[
        ['Plano', 'Perfil', 'Dia', 'Total liquido', 'Total contas a receber', 'Total']]
    relatorio_conciliacao.to_excel(os.path.join(investiments_path, f'relatorio_provisao_{day}-{mon}.xlsx'), index=False)