import pandas as pd
import datetime

class Provisao:
    def __init__(self, df, competencia):
        self.folha_beneficios = df
        self.data_competencia = competencia

    def criarProvisao(self):
        return self.filtroProvisao()

    def filtroProvisao(self):
        """Retorna os itens de provisão presentes na folha de benefícios."""
        valores_itens = [
            '14121-IN1343-DEDUÇAOBASETRIBUTAVEL(INFORMATIVO)',
            '14122-IN1343-DEDUÇAOBASETRIBUTAVELREGR.(INFORMATIVO)',
            '14131-IN1343-DEDUÇAOBASETRIBUTAVEL(INFORMATIVO)',
            '14151-IN1343-BAIXAESTOQUEISENTO(INFORMATIVO)',
            '14152-IN1343-BAIXAESTOQUEISENTOREGR.(INFORMATIVO)',
            '14171-IN1343-BAIXAESTOQUEISENTORESG.(INFORMATIVO)'
        ]

        condicao = (
                self.folha_beneficios["Item folha"].isin(valores_itens) |
                ~(self.folha_beneficios["Valor"] < 0)
        )

        # Captura os índices onde a condição é verdadeira
        indices_validos = self.folha_beneficios.index[condicao]

        # Filtra o DataFrame com base nos índices
        return self.folha_beneficios.loc[indices_validos]

        # return self.folha_beneficios[
        #     (
        #      (self.folha_beneficios["Item folha"] == '14121-IN1343-DEDUÇAOBASETRIBUTAVEL(INFORMATIVO)') |
        #      (self.folha_beneficios["Item folha"] == '14122-IN1343-DEDUÇAOBASETRIBUTAVELREGR.(INFORMATIVO)') |
        #      (self.folha_beneficios["Item folha"] == '14131-IN1343-DEDUÇAOBASETRIBUTAVEL(INFORMATIVO)') |
        #      (self.folha_beneficios["Item folha"] == '14151-IN1343-BAIXAESTOQUEISENTO(INFORMATIVO)') |
        #      (self.folha_beneficios["Item folha"] == '14152-IN1343-BAIXAESTOQUEISENTOREGR.(INFORMATIVO)') |
        #      (self.folha_beneficios["Item folha"] == '14171-IN1343-BAIXAESTOQUEISENTORESG.(INFORMATIVO)') |
        #      (self.folha_beneficios["Valor"] < 0)
        #     )]