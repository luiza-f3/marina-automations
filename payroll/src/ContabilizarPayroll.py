import pandas as pd
import os
from unidecode import unidecode
from dotenv import load_dotenv

load_dotenv()

VISAO_MULTI_PERCENTUAL = os.getenv('VISAO_MULTI_PERCENTUAL')
BD_PERCENTUAL = os.getenv('BD_PERCENTUAL')
VISAO_TELEFONICA_PERCENTUAL = os.getenv('VISAO_TELEFONICA_PERCENTUAL')
PREVISAO_PERCENTUAL = os.getenv('PREVISAO_PERCENTUAL')

base_path = os.path.expanduser('~/Documents/Folha de pagamentos')
class ContabilizarPayroll:
    def __init__(self, df: pd.DataFrame):
        self.payroll = df
        self.consult_payroll = pd.read_excel(os.path.join(base_path, os.getenv("CONSULT_PAYROLL")))

    def contabilizar(self):
        # padronizar tipo de dados da folha de pagamento
        self.payroll['Rubrica'] = self.payroll['Rubrica'].astype(str)
        self.payroll['Folha'] = self.payroll['Folha'].astype(str)

        # padronizar tipo de dados da base de consulta da folha de pagamento
        self.consult_payroll['Rubrica'] = self.consult_payroll['Rubrica'].astype(str)
        self.consult_payroll['Folha'] = self.consult_payroll['Folha'].astype(str)
        df = self.encontrarContaContabil()

        multi_accounting = self.lancamento(df, 908, VISAO_MULTI_PERCENTUAL)
        bd_accounting = self.lancamento(df, 922, BD_PERCENTUAL)
        visao_telefonica_accounting = self.lancamento(df, 949, VISAO_TELEFONICA_PERCENTUAL)
        previsao_accounting = self.lancamento(df, 951, PREVISAO_PERCENTUAL)

        df = pd.concat([multi_accounting, bd_accounting, visao_telefonica_accounting, previsao_accounting])

        return df

    def encontrarContaContabil(self):
        # Realiza a junção dos DataFrames com base nas colunas 'Rubrica' e 'Folha'
        resultado = self.payroll.merge(
            self.consult_payroll[['Rubrica', 'Folha', 'Conta debito', 'Conta credito', 'Descricao', 'CC']],
            on=['Rubrica', 'Folha'],
            how='left'
        )
        return resultado

    def lancamento(self, df, plano, percentual):
        lista_d_c = []
        percentual = float(percentual) / 100

        for _, row in df.iterrows():
            day, mont, year = row['DataEmissao'].split('-')
            rubrica = row['Rubrica']
            descricao = unidecode(str(row['Descricao'])).upper()
            conta_debito = str(row['Conta debito']).split('.')[0]
            conta_credito = str(row['Conta credito']).split('.')[0]
            valor = abs(float(row['ValorLiquido'])) * percentual

            cc_formatado = str(int(row['CC'])) if pd.notna(row['CC']) else '0000'
            cc_formatado = cc_formatado.zfill(4)

            historico = f'FOLHA SALARIO {day}/{year} {rubrica} {descricao}'

            debito = {
                'Conta contabil': conta_debito,
                'Historico': historico,
                'Valor': valor,
                'D/C': 'D',
                'CC': cc_formatado,
                'Plano': plano,
                'Perfil': 19
            }

            credito = {
                'Conta contabil': conta_credito,
                'Historico': historico,
                'Valor': valor,
                'D/C': 'C',
                'CC': cc_formatado,
                'Plano': plano,
                'Perfil': 19
            }
            lista_d_c.extend([debito, credito])
        df_final = pd.DataFrame(lista_d_c)

        # do colunas
        df_final = df_final[['Conta contabil', 'Valor', 'D/C', 'Historico', 'CC', 'Plano', 'Perfil']]

        return df_final