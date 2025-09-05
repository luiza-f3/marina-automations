import pandas as pd

class Deducao:
    def __init__(self, df, competencia, df_consulta):
        self.folha_beneficios = df
        self.data_competencia = competencia
        self.df_consulta = df_consulta

    def criarDeducao(self):
        return self.filtroDeducao()

    def filtroDeducao(self):
        """Retorna os itens dedutivos presente na folha de beneficios"""
        return self.folha_beneficios[
            self.folha_beneficios[["Tipo de beneficio", "Item folha"]].apply(tuple, axis=1).isin(
                self.df_consulta[self.df_consulta["Pgto dentro do mes - credito"].notna()][
                    ["Tipo de beneficio", "Item folha"]
                ].apply(tuple, axis=1)
            )
        ]

