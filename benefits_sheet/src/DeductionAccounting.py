import pandas as pd

class DeductionAccounting:
    def __init__(self, df, competencia, df_consulta):
        self.payroll_benefits = df
        self.competence_date = competencia
        self.df_query = df_consulta

    def create_deduction(self):
        return pd.DataFrame(self.filter_deduction())

    def filter_deduction(self):
        """Retorna os itens dedutivos presente na folha de beneficios"""
        return self.payroll_benefits[
            self.payroll_benefits[["Tipo de beneficio", "Item folha"]].apply(tuple, axis=1).isin(
                self.df_query[self.df_query["Pgto dentro do mes - credito"].notna()][
                    ["Tipo de beneficio", "Item folha"]
                ].apply(tuple, axis=1)
            )
        ]