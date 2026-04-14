import pandas as pd

class AccountingAccount:
    def __init__(self):
        self.origin_account = "10203080101020"
        self.target_account = "10203080101010"

    def duplicate_postings_for_accounts(self, df: pd.DataFrame) -> pd.DataFrame:
        # Duplicar lançamentos para contas específicas

        new_entries = []

        for _, row in df.iterrows():
            if str(row['Conta contabil']) == self.origin_account and row['D/C'] == 'C':
                #Cria a cópia para o lançamento em Débito
                debit = row.copy()
                debit['Conta contabil'] = self.origin_account
                debit['D/C'] = 'D'

                # Cria a cópia para o lançamento em Crédito
                credit = row.copy()
                credit['Conta contabil'] = self.target_account
                credit['D/C'] = 'C'

                new_entries.extend([debit,credit])

        if new_entries:
            new_df = pd.DataFrame(new_entries)
            df = pd.concat([df, new_df], ignore_index=True)

        return df

