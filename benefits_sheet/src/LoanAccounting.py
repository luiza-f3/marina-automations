import pandas as pd
import datetime

class LoanAccounting:
    def __init__(self, df, competencia):
        self.payroll_benefits = df
        self.competence_date = competencia

    def create_loans(self):
        return pd.DataFrame(self.filter_loans())

    def filter_loans(self):
        """Retorna os itens de empréstimo presente na folha de benefícios"""
        self.payroll_benefits["Competencia"] = pd.to_datetime(
            self.payroll_benefits["Data de pagamento"]).dt.strftime(
            "%m-%Y")

        # Condições
        cond1 = (
                    (self.payroll_benefits["Item folha"].isin(["41-EMPRESTIMO", "45-QUITACAODEEMPRESTIMO"])) &
                    (self.payroll_benefits["Competencia"] != self.competence_date)
            )

        cond2 = self.payroll_benefits["Item folha"].isin([
                "1013-DESCONTOCONTRIB.ASSISTIDOSP/PLANO",
                "55-DESCONTODEREVISAODEBENEFICIO"
            ])

        return self.payroll_benefits[cond1 | cond2]