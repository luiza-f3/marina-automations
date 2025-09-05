"""
para cada linha de "df_final = pd.DataFrame(lista_d_c)" que tiver uma conta correspondente a: "10203080101020"

não remover mas adcionar novos lançamentos em débito e crédito nas contas:
D	10203080101020
C	10203080101010
"""

import pandas as pd

class AccountingAccount:
    def __init__(self):
        self.conta_origem = "10203080101020"
        self.conta_destino = "10203080101010"

    def duplicar_lancamentos_para_conta(self, df: pd.DataFrame) -> pd.DataFrame:
        novos_lancamentos = []

        for _, row in df.iterrows():
            if str(row['Conta contabil']) == self.conta_origem and row['D/C'] == 'C':
                # Cria cópia para lançamento em débito
                debito = row.copy()
                debito['Conta contabil'] = self.conta_origem
                debito['D/C'] = 'D'

                # Cria cópia para lançamento em crédito
                credito = row.copy()
                credito['Conta contabil'] = self.conta_destino
                credito['D/C'] = 'C'

                novos_lancamentos.extend([debito, credito])

        if novos_lancamentos:
            novos_df = pd.DataFrame(novos_lancamentos)

            df = pd.concat([df, novos_df], ignore_index=True)

        return df

"""
import pandas as pd
import os

class AccountingAccount:
    def __init__(self, consulta_path: str, output_path: str):
        self.conta_origem = "10203080101020"
        self.conta_destino = "10203080101010"
        self.consulta_path = consulta_path
        self.output_path = output_path

    def duplicar_lancamentos_para_conta(self, df: pd.DataFrame) -> pd.DataFrame:
        # Lê a Planilha2
        consulta_df = pd.read_excel(self.consulta_path, sheet_name="Planilha2")

        novos_lancamentos = []

        for _, row in df.iterrows():
            if str(row['Conta contabil']) == self.conta_origem:
                # Verifica se há correspondência na consulta (opcional: você pode definir o critério exato)
                match = consulta_df[
                    (consulta_df["Tipo de beneficio"] == row.get("Tipo de beneficio", ""))
                    & (consulta_df["Item folha"] == row.get("Item folha", ""))
                ]

                if not match.empty:
                    # Cria os lançamentos
                    debito = row.copy()
                    debito['Conta contabil'] = self.conta_origem
                    debito['D/C'] = 'D'

                    credito = row.copy()
                    credito['Conta contabil'] = self.conta_destino
                    credito['D/C'] = 'C'

                    novos_lancamentos.extend([debito, credito])

        # Se encontrou algo, salva
        if novos_lancamentos:
            df_novos = pd.DataFrame(novos_lancamentos)
            df_novos.to_excel(self.output_path, index=False)
            print(f"Lançamentos ajustados salvos em: {self.output_path}")
            # Retorna DataFrame combinado (original + novos)
            return pd.concat([df, df_novos], ignore_index=True)

        # Se nada for encontrado
        print("Nenhum lançamento ajustado foi encontrado na consulta.")
        return df
"""