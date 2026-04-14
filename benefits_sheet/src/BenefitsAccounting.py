import pandas as pd
from benefits_sheet.utils.tools import build_benefits_posting_dataframe
from datetime import datetime

class BenefitsAccounting:
    """Classe com métodos para gerar contabilização para todos itens da folha de benefícios"""

    def __init__(self, deduction: pd.DataFrame, loans: pd.DataFrame, provision: pd.DataFrame,
                 lookup_df: pd.DataFrame, payment_date: str, competence_date: str):
        self.provision = provision
        self.deduction = deduction
        self.loans = loans
        self.lookup_df = lookup_df
        self.payment_date = payment_date
        self.competence_date = competence_date

    def account(self):
        deduction = self.account_deduction()
        loans = self.account_loans()
        provision = self.account_provision()
        return pd.concat([deduction, loans, provision], ignore_index=True)

    def account_deduction(self):
        """Contabiliza itens dedutivos da folha de beneficios"""
        if not isinstance(self.deduction, pd.DataFrame):
            return "É esperado um dataframe"

        debit_entries = []
        credit_entries = []

        debit_account = 20101010100000  # Fixed value for debit account

        for idx, row in self.deduction.iterrows():
            # Definir a data conforme a condição
            formatted_date = datetime.strptime(row["Data de pagamento"], "%Y-%m-%d").strftime("%d/%m/%Y")
            date = formatted_date if "IMPOSTODERENDA" not in row["Item folha"] else self.payment_date

            # Filtro para buscar as contas de débito e crédito correspondentes
            filter_condition = (self.lookup_df["Tipo de beneficio"] == row["Tipo de beneficio"]) & (
                    self.lookup_df["Item folha"] == row["Item folha"])

            credit_account = None
            if not self.lookup_df.loc[filter_condition].empty:
                payment_date_formatted = datetime.strptime(row["Data de pagamento"], "%Y-%m-%d").strftime("%m-%Y")
                if payment_date_formatted == self.competence_date:
                    credit_account = self.lookup_df.loc[filter_condition, "Pgto dentro do mes - credito"].iloc[0]
                else:
                    credit_account = self.lookup_df.loc[filter_condition, "Pgto mes seguinte - Credito"].iloc[0]

            if credit_account is None:
                return f"Erro: Não foi encontrada uma conta de crédito para o tipo de benefício {row['Tipo de beneficio']} e item {row['Item folha']}"

            # Criando os lançamentos de débito e crédito
            debit = build_benefits_posting_dataframe(date, debit_account, row["Valor"], 'D','DESCONTO S/ FOLHA DE BENEF/RESG', 3, row['Plano'], row['Perfil'], row['Patrocinadora'])
            credit = build_benefits_posting_dataframe(date, credit_account, row["Valor"], 'C','DESCONTO S/ FOLHA DE BENEF/RESG', 3, row['Plano'], row['Perfil'], row['Patrocinadora'])

            debit_entries.append(debit)
            credit_entries.append(credit)

            df_debit = pd.concat(debit_entries, ignore_index=True) if debit_entries else pd.DataFrame()
            df_credit = pd.concat(credit_entries, ignore_index=True) if credit_entries else pd.DataFrame()

            df_entries = pd.concat([df_debit, df_credit], ignore_index=True)

            return df_entries

    def account_loans(self):
        # Contabiliza itens de emprestimos da folha de beneficios
        debit_account = 20101990400000

        debit_entries = []
        credit_entries = []

        # Verifica se 'emprestimos' é um DataFrame
        if isinstance(self.loans, pd.DataFrame):
            for idx, row in self.loans.iterrows():
                formatted_date = datetime.strptime(row["Data de pagamento"], "%Y-%m-%d").strftime("%d/%m/%Y")

                # Filtra o DataFrame 'df_consulta' com base no Tipo de benefício e Item da folha
                filter_condition = (self.lookup_df["Tipo de beneficio"] == row["Tipo de beneficio"]) & (
                        self.lookup_df["Item folha"] == row["Item folha"])

                # # Verifica se o filtro encontra algum valor correspondente
                if not self.df_lookup.loc[filter_condition].empty:
                    item_folha = self.lookup_df.loc[filter_condition, "Item folha"].iloc[0]

                    if "1313" not in item_folha and "1013" not in item_folha and "55-DESCONTO" not in item_folha:
                        continue

                    credit_account = self.lookup_df.loc[filter_condition, "Pgto dentro do mes - credito"].iloc[0]

                    # Criando os lançamentos de débito e crédito
                    debit = build_benefits_posting_dataframe(formatted_date, debit_account, row["Valor"], 'D','DESCONTO S/ FOLHA DE BENEF/RESG', 3, row['Plano'], row['Perfil'], row['Patrocinadora'])
                    credit = build_benefits_posting_dataframe(formatted_date, credit_account, row["Valor"], 'C','DESCONTO S/ FOLHA DE BENEF/RESG', 3, row['Plano'], row['Perfil'], row['Patrocinadora'])

                    # Adicionando os lançamentos às listas
                    debit_entries.append(debit)
                    credit_entries.append(credit)

                # Concatenar os DataFrames de débito e crédito após o loop
                df_debit = pd.concat(debit_entries, ignore_index=True) if debit_entries else pd.DataFrame()
                df_credit = pd.concat(credit_entries, ignore_index=True) if credit_entries else pd.DataFrame()

                # Concatenar os DataFrames de débito e crédito no DF
                df_entries = pd.concat([df_debit, df_credit], ignore_index=True)

                return df_entries
            else:
                return "É esperado um dataframe para emprestimos"

    def account_provision(self):
        # Contabiliza itens de provisão da folha de beneficios
        debit_entries = []
        credit_entries = []

        # Verifica se 'provisao' é um DataFrame
        if not isinstance(self.provision, pd.DataFrame):
            return "É esperado um dataframe para provisão"

        for idx, row in self.provision.iterrows():
            # Filtro para buscar as contas de débito e crédito correspondentes
            filter_condition = (self.lookup_df["Tipo de beneficio"] == row["Tipo de beneficio"]) & \
                     (self.lookup_df["Item folha"] == row["Item folha"])

            # Verifica se o filtro encontra algum valor correspondente
            if not self.lookup_df.loc[filter_condition].empty:
                debit_account = self.lookup_df.loc[filter_condition, "Conta contabil - debito"].iloc[0]
                credit_account = self.lookup_df.loc[filter_condition, "Conta contabil - credito"].iloc[0]

                # Criando os lançamentos de débito e crédito
                debit = build_benefits_posting_dataframe(self.payment_date, debit_account, row["Valor"], 'D','PROVISAO S/ FOLHA DE BENEF/RESG', 3, row['Plano'], row['Perfil'], row['Patrocinadora'])

                credit = build_benefits_posting_dataframe(self.payment_date, credit_account, row["Valor"], 'C','PROVISAO S/ FOLHA DE BENEF/RESG', 3, row['Plano'], row['Perfil'], row['Patrocinadora'])

                # Adicionando os lançamentos às listas
                debit_entries.append(debit)
                credit_entries.append(credit)

        # Concatenar os DataFrames de débito e crédito após o loop
        df_debit = pd.concat(debit_entries, ignore_index=True) if debit_entries else pd.DataFrame()
        df_credit = pd.concat(credit_entries, ignore_index=True) if credit_entries else pd.DataFrame()

        # Concatenar os DataFrames de débito e crédito no DF
        df_entries = pd.concat([df_debit, df_credit], ignore_index=True)

        return df_entries

