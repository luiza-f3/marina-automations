import pandas as pd
import datetime

class Emprestimos:
    def __init__(self, df, competencia):
        self.folha_beneficios = df
        self.data_competencia = competencia

    def criarEmprestimos(self):
        return pd.DataFrame(self.filtroEmprestimos())

    def filtroEmprestimos(self):
        """Retorna os itens de empréstimo presente na folha de benefícios"""
        self.folha_beneficios["Competencia"] = pd.to_datetime(self.folha_beneficios["Data de pagamento"]).dt.strftime(
            "%m-%Y")

        # Condições
        cond1 = (
                (self.folha_beneficios["Item folha"].isin(["41-EMPRESTIMO", "45-QUITACAODEEMPRESTIMO"])) &
                (self.folha_beneficios["Competencia"] != self.data_competencia)
        )

        cond2 = self.folha_beneficios["Item folha"].isin([
            "1013-DESCONTOCONTRIB.ASSISTIDOSP/PLANO",
            "55-DESCONTODEREVISAODEBENEFICIO"
        ])

        return self.folha_beneficios[cond1 | cond2]

        # Formata a data de pagamento para comparar com a data de competência
        # return self.folha_beneficios[
        #     (
        #         # Filtro para "EMPRESTIMO" ou "QUITACAO DE EMPRÉSTIMO" e data de pagamento do item diferente da competência
        #             ((self.folha_beneficios["Item folha"] == '41-EMPRESTIMO') |
        #              (self.folha_beneficios["Item folha"] == '45-QUITACAODEEMPRESTIMO')) &
        #             (self.folha_beneficios["Data de pagamento"].apply(
        #                 lambda x: f"{x.split('-')[1]}-{x.split('-')[0]}") != self.data_competencia)
        #     ) |
        #     (
        #         # Filtro para "DESCONTO CONTRIBUIÇÃO ASSISTIDOS" ou "REVISÃO DE BENEFÍCIO"
        #             (self.folha_beneficios["Item folha"] == '1013-DESCONTOCONTRIB.ASSISTIDOSP/PLANO') |
        #             (self.folha_beneficios["Item folha"] == '55-DESCONTODEREVISAODEBENEFICIO')
        #     )
        #     ]
