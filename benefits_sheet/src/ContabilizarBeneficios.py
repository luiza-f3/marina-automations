import pandas as pd

from benefits_sheet.utils.tools import layoutLancamentoBeneficios
from datetime import datetime


class ContabilizarBeneficios:
    """Classe com métodos para gerar contabilização para todos itens da folha de benefícios"""

    def __init__(self, deducao: pd.DataFrame, emprestimos: pd.DataFrame, provisao: pd.DataFrame,
                 df_consulta: pd.DataFrame, data_pagamento: str, data_competencia: str):
        self.provisao = provisao
        self.deducao = deducao
        self.emprestimos = emprestimos
        self.df_consulta = df_consulta
        self.data_pagamento = data_pagamento
        self.data_competencia = data_competencia

    def contabilizar(self):
        deducao = self.contabilizarDeducao()
        emprestimos = self.contabilizarEmprestimos()
        provisao = self.contabilizarProvisao()
        return pd.concat([deducao, emprestimos, provisao], ignore_index=True)

    def contabilizarDeducao(self):
        """Contabiliza itens dedutivos da folha de beneficios"""
        # Verifica se 'deducao' é um DataFrame
        if not isinstance(self.deducao, pd.DataFrame):
            return "É esperado um dataframe"

        # Listas para armazenar os resultados de débitos e créditos
        lancamentos_debito = []
        lancamentos_credito = []

        conta_debito = 20101010100000  # Valor fixo para conta de débito

        for idx, row in self.deducao.iterrows():
            # Definir a data conforme a condição
            data_formatada = datetime.strptime(row["Data de pagamento"], "%Y-%m-%d").strftime("%d/%m/%Y")
            data = data_formatada if "IMPOSTODERENDA" not in row["Item folha"] else self.data_pagamento

            # Filtro para buscar as contas de débito e crédito correspondentes
            filtro = (self.df_consulta["Tipo de beneficio"] == row["Tipo de beneficio"]) & (
                    self.df_consulta["Item folha"] == row["Item folha"])

            # Verifica se o filtro retorna resultados antes de acessar os dados
            conta_credito = None
            if not self.df_consulta.loc[filtro].empty:
                # Verificar se a data de pagamento corresponde à data de competência
                data_pagamento_formatada = datetime.strptime(row["Data de pagamento"], "%Y-%m-%d").strftime("%m-%Y")
                if data_pagamento_formatada == self.data_competencia:
                    conta_credito = self.df_consulta.loc[filtro, "Pgto dentro do mes - credito"].iloc[0]
                else:
                    conta_credito = self.df_consulta.loc[filtro, "Pgto mes seguinte - Credito"].iloc[0]

            if conta_credito is None:
                return f"Erro: Não foi encontrada uma conta de crédito para o tipo de benefício {row['Tipo de beneficio']} e item {row['Item folha']}"

            # Criando os lançamentos de débito e crédito
            debito = layoutLancamentoBeneficios(data, conta_debito, row["Valor"], 'D',
                                                'DESCONTO S/ FOLHA DE BENEF/RESG', 3, row['Plano'], row['Perfil'], row['Patrocinadora'])
            credito = layoutLancamentoBeneficios(data, conta_credito, row["Valor"], 'C',
                                                 'DESCONTO S/ FOLHA DE BENEF/RESG', 3, row['Plano'], row['Perfil'], row['Patrocinadora'])

            # Adicionando os lançamentos às listas
            lancamentos_debito.append(debito)
            lancamentos_credito.append(credito)

        # Concatenar os DataFrames de débito e crédito
        df_debito = pd.concat(lancamentos_debito, ignore_index=True) if lancamentos_debito else pd.DataFrame()
        df_credito = pd.concat(lancamentos_credito, ignore_index=True) if lancamentos_credito else pd.DataFrame()

        # Concatenar débitos e créditos em um único DataFrame
        df_lancamentos = pd.concat([df_debito, df_credito], ignore_index=True)

        # Retorna o DataFrame com todos os lançamentos
        return df_lancamentos

    def contabilizarEmprestimos(self):
        conta_debito = 20101990400000

        # Listas para armazenar os resultados de débitos e créditos
        lancamentos_debito = []
        lancamentos_credito = []

        # Verifica se 'emprestimos' é um DataFrame
        if isinstance(self.emprestimos, pd.DataFrame):
            # Itera sobre as linhas do DataFrame de empréstimos
            for idx, row in self.emprestimos.iterrows():
                # Formatar a data de pagamento para o formato 'dd/mm/yyyy'
                data_formatada = datetime.strptime(row["Data de pagamento"], "%Y-%m-%d").strftime("%d/%m/%Y")

                # Filtra o DataFrame 'df_consulta' com base no Tipo de benefício e Item da folha
                filtro = (self.df_consulta["Tipo de beneficio"] == row["Tipo de beneficio"]) & \
                         (self.df_consulta["Item folha"] == row["Item folha"])

                # Verifica se o filtro encontra algum valor correspondente
                if not self.df_consulta.loc[filtro].empty:
                    # Checa se o 'Item folha' contém os valores especificados
                    item_folha = self.df_consulta.loc[filtro, "Item folha"].iloc[0]

                    # Verifica a condição de exclusão (se o item folha não contém certos valores)
                    if "1313" not in item_folha and "1013" not in item_folha and "55-DESCONTO" not in item_folha:
                        continue  # Pula a iteração se a condição for atendida

                    # Obtém o valor de conta_credito da coluna correspondente no DataFrame de consulta
                    conta_credito = self.df_consulta.loc[filtro, "Pgto dentro do mes - credito2"].iloc[0]

                    # Criando os lançamentos de débito e crédito
                    debito = layoutLancamentoBeneficios(data_formatada, conta_debito, row["Valor"], 'D',
                                                        'DESCONTO S/ FOLHA DE BENEF/RESG', 3, row['Plano'],
                                                        row['Perfil'], row['Patrocinadora'])
                    credito = layoutLancamentoBeneficios(data_formatada, conta_credito, row["Valor"], 'C',
                                                         'DESCONTO S/ FOLHA DE BENEF/RESG', 3, row['Plano'],
                                                         row['Perfil'], row['Patrocinadora'])

                    # Adicionando os lançamentos às listas
                    lancamentos_debito.append(debito)
                    lancamentos_credito.append(credito)

            # Concatenar os DataFrames de débito e crédito após o loop
            df_debito = pd.concat(lancamentos_debito, ignore_index=True) if lancamentos_debito else pd.DataFrame()
            df_credito = pd.concat(lancamentos_credito, ignore_index=True) if lancamentos_credito else pd.DataFrame()

            # Concatenar débitos e créditos em um único DataFrame
            df_lancamentos = pd.concat([df_debito, df_credito], ignore_index=True)

            # Retorna o DataFrame com todos os lançamentos
            return df_lancamentos
        else:
            return "É esperado um dataframe para 'emprestimos'."

    def contabilizarProvisao(self):
        lancamentos_debito = []
        lancamentos_credito = []

        # Verifica se 'provisao' é um DataFrame
        if not isinstance(self.provisao, pd.DataFrame):
            return "É esperado um dataframe para 'provisao'."

        for idx, row in self.provisao.iterrows():
            # Cria o filtro para selecionar as contas de débito e crédito
            filtro = (self.df_consulta["Tipo de beneficio"] == row["Tipo de beneficio"]) & \
                     (self.df_consulta["Item folha"] == row["Item folha"])

            # Verifica se o filtro encontra correspondências na tabela de consulta
            if not self.df_consulta.loc[filtro].empty:
                conta_debito = self.df_consulta.loc[filtro, "Conta contabil - debito"].iloc[0]
                conta_credito = self.df_consulta.loc[filtro, "Conta contabil - credito"].iloc[0]

                # Cria os lançamentos de débito e crédito usando layoutLancamentoBeneficios
                debito = layoutLancamentoBeneficios(self.data_pagamento, conta_debito, row["Valor"], 'D',
                                                    'PROVISAO DE FOLHA DE BENEF/RESG', 3, row['Plano'],
                                                    row['Perfil'], row['Patrocinadora'])
                credito = layoutLancamentoBeneficios(self.data_pagamento, conta_credito, row["Valor"], 'C',
                                                     'PROVISAO DE FOLHA DE BENEF/RESG', 3, row['Plano'],
                                                     row['Perfil'], row['Patrocinadora'])

                # Adiciona os lançamentos às listas
                lancamentos_debito.append(debito)
                lancamentos_credito.append(credito)

        # Concatena os DataFrames de débito e crédito após o loop
        df_debito = pd.concat(lancamentos_debito, ignore_index=True) if lancamentos_debito else pd.DataFrame()
        df_credito = pd.concat(lancamentos_credito, ignore_index=True) if lancamentos_credito else pd.DataFrame()

        # Concatena débitos e créditos em um único DataFrame
        df_lancamentos = pd.concat([df_debito, df_credito], ignore_index=True)

        # Retorna o DataFrame com todos os lançamentos
        return df_lancamentos
