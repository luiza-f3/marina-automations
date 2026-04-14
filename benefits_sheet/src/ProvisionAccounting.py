import pandas as pd
import datetime

class ProvisionAccounting:
    def __init__(self, df, competencia):
        self.payroll_benefits = df
        self.competence_date = competencia

    def create_provision(self):
        return pd.DataFrame(self.filter_provision())

    def filter_provision(self):
        """Retorna os itens de provisão presentes na folha de benefícios."""
        provision_items = [
            '14121-IN1343-DEDUÇAOBASETRIBUTAVEL(INFORMATIVO)',
            '14122-IN1343-DEDUÇAOBASETRIBUTAVELREGR.(INFORMATIVO)',
            '14131-IN1343-DEDUÇAOBASETRIBUTAVEL(INFORMATIVO)',
            '14151-IN1343-BAIXAESTOQUEISENTO(INFORMATIVO)',
            '14152-IN1343-BAIXAESTOQUEISENTOREGR.(INFORMATIVO)',
            '14171-IN1343-BAIXAESTOQUEISENTORESG.(INFORMATIVO)'
        ]

        condition = (
                self.payroll_benefits["Item folha"].isin(provision_items) |
                ~(self.payroll_benefits["Valor"] < 0)
        )

        # Captura os índices onde a condição é verdadeira
        valid_indices = self.payroll_benefits.index[condition]

        # Filtra o DataFrame com base nos índices
        return self.payroll_benefits.loc[valid_indices]