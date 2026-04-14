import pandas as pd
import os
from datetime import datetime
from benefits_sheet.utils.AccountingAccount import AccountingAccount
from src.LoanAccounting import LoanAccounting
from src.ProvisionAccounting import ProvisionAccounting
from src.DeductionAccounting import DeductionAccounting
from src.BenefitsAccounting import BenefitsAccounting
from utils.tools import normalize_text

payment_date = "2025-07-29"

BASE_PATH = os.path.expanduser('~\\Documents')
benefits_path = os.path.join(BASE_PATH, 'data', 'processed', 'folha_beneficios_processado.csv')

benefits_query_path = os.path.join(BASE_PATH, 'Beneficios' , 'consulta_folha_beneficios.xlsx')

year, month, day = payment_date.split('-')
competence_date = f'{month}-{year}'
date_br = f'{day}-{month}-{year}'

if __name__ == "__main__":
    benefits_query = pd.read_excel(benefits_query_path,sheet_name="Planilha2")
    df = pd.read_csv(benefits_path)

    df = df[df['Data de pagamento'] == payment_date]

    # padronização de valores na planilha de consulta
    benefits_query = normalize_text(benefits_query,
                                      ['Tipo de folha', 'Item folha', 'Grupo de beneficio',
                                       'Tipo de beneficio'])

    loans = LoanAccounting(df, competence_date).create_loans()
    provision = ProvisionAccounting(df, competence_date).create_provision()
    deduction = DeductionAccounting(df, competence_date, benefits_query).create_deduction()

    # --- Validação de valores na Planilha2 ---
    required_columns = ['Tipo de beneficio', 'Item folha']  # Colunas que você quer conferir
    overall_valid_columns = []

    for df_name, df_entry in [("Deducao", deduction), ("Emprestimos", loans), ("Provisao", provision)]:
        if df_entry.empty:
            print(f"⚠️ DataFrame {df_name} está vazio, nenhuma validação necessária")
            continue

        missing_entries = []
        for col in required_columns:
            df_entry_col = df_entry[col].astype(str).str.strip().str.upper()
            query_col = benefits_query[col].astype(str).str.strip().str.upper()

            for idx, value in df_entry_col.items():
                if value not in query_col.values:
                    entry_date = df_entry.loc[idx, "Data de pagamento"]
                    missing_entries.append(
                        f'"{value}" - {col} - Data = {datetime.strptime(entry_date, "%Y-%m-%d").strftime("%d/%m/%Y")}')

            if not any(v for v in missing_entries if col in v) and col not in overall_valid_columns:
                overall_valid_columns.append(col)

            if missing_entries:
                print(f"❌ DataFrame {df_name} possui valores ausentes na coluna '{col}':")
                for entry in missing_entries:
                    print(f"   - {entry}")

            if overall_valid_columns:
                print(f"✅ Colunas validadas com sucesso! Todos os valores presentes: {', '.join(overall_valid_columns)}")

            # Fim da validação ---

            accounted_benefits = BenefitsAccounting(deduction, loans, provision,
                                                    benefits_query, payment_date, competence_date).account()
            accounted_benefits = accounted_benefits.loc[accounted_benefits['Valor'] != 0]
            accounted_benefits = AccountingAccount().duplicate_postings_for_accounts(accounted_benefits)

            accounted_benefits["Valor"] = accounted_benefits["Valor"].abs()
            accounted_benefits['Data'] = date_br
            accounted_benefits['Patrocinadora'] = accounted_benefits['Patrocinadora'].astype(lambda x: str(x).zfill(3))

            accounted_benefits = accounted_benefits.sort_values(by=['Plano', 'Perfil', 'Valor', 'D/C'], ascending=[True, True, True, False])
            accounted_benefits.to_excel(os.path.join(BASE_PATH, 'Beneficios', f'folha_contabilizada{date_br}.xlsx'), index=False)
            print('✅ Sua folha foi gerada com sucesso!')

