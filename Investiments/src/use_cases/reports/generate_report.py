from dotenv import load_dotenv
import os

load_dotenv()
base_path = os.path.expanduser(os.getenv("BASE_PATH"))
year, mon, day = os.getenv('CURRENT_DATE').split('-')
dt_cash_flow = f'{day}/{mon}/{year}'
execute_provision = os.getenv('PROVISION')

def generate_report(df_provision, wallet):
    """Gerar relatórios"""
    investiments_path = os.path.join(base_path, 'Investimentos')
    os.makedirs(investiments_path, exist_ok=True)

    provision_copy = df_provision.groupby(['Plano', 'Perfil'])['Valor'].sum().reset_index()

    reconciliation_report = wallet.groupby(['Plano', 'Perfil'])['Valor Atual'].sum().reset_index()
    reconciliation_report = reconciliation_report.merge(provision_copy, on=['Plano', 'Perfil'], how='left')
    reconciliation_report['Valor'].fillna(0, inplace=True)
    reconciliation_report['Total'] = reconciliation_report[['Valor Atual', 'Valor']].sum(axis=1)

    reconciliation_report['Dia'] = f'{day}/{mon}'
    reconciliation_report.rename(columns={'Valor Atual': 'Total liquido', 'Valor': 'Total contas a receber'},
                                 inplace=True)

    reconciliation_report.drop('Despesa', axis=1, inplace=True, errors='ignore')

    # ordenando os campos
    reconciliation_report = reconciliation_report[
        ['Plano', 'Perfil', 'Dia', 'Total liquido', 'Total contas a receber', 'Total']]
    reconciliation_report.to_excel(os.path.join(investiments_path, f'relatorio_provisao_{day}-{mon}.xlsx'), index=False)