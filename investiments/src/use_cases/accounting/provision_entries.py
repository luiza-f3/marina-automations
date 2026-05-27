import pandas as pd
from investiments.src.utils.mappings.fees_accounts import fees_accounts
from investiments.src.utils.mappings.fees_info import fees_info
from investiments.src.utils.tools import create_accounting_entry

def provision_entries(df_provision):
    accounting_entries = []

    for _, row in df_provision.iterrows():
        amount = row['Valor']
        plan = row['Plano']
        profile = row['Perfil']
        expense = row['Despesa']

        round(amount, 2)

        for fee in fees_info:
            if fee in expense:
                # Determina a conta de crédito com base no plano e perfil
                credit_account = 'PGA' if (plan, profile) in [(987, 19), (952, 20)] else 'Plano'

                # Cria os lançamentos contábeis: debita a conta de despesa e credita a conta de provisão correspondente
                booking1 = create_accounting_entry(fees_accounts[fee]['Despesa'], abs(amount), 'D', fee, plan, profile)
                booking2 = create_accounting_entry(fees_accounts[fee][credit_account], abs(amount), 'C', fee, plan, profile)

                if booking1:
                    accounting_entries.append(booking1)
                if booking2:
                    accounting_entries.append(booking2)

                break

    return pd.DataFrame(accounting_entries)
