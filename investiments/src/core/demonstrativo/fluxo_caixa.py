from investiments.src.core.usecases.executeFromTo import executeFromTo
from investiments.src.utils.consultas.expenses_mapping import expenses_mapping
from investiments.src.utils.consultas.fees_info import fees_info
from investiments.src.utils.data_loader import DataLoader
from investiments.src.utils.consultas.cash_flow_info import cash_flow_info
from investiments.src.utils.tools import filtrar_data_demonstrativo, normalize_text
from investiments.src.utils.tools import define_profile_plan
import pandas as pd


class FluxoDeCaixa:
    cod_carteira = [item[0] for item in cash_flow_info]
    taxas_demonstrativo = fees_info

    @classmethod
    def preparar_fluxo_caixa(cls, path_file, dt):
        cash_flow = DataLoader.load_file_directory(path_file, cls.cod_carteira)
        cash_flow = {key: df.iloc[7:, :4] for key, df in cash_flow.items()}
        cash_flow = {key: pd.DataFrame(df.set_axis(['Data', 'Historico', 'Entrada', 'Saida'], axis='columns')) for key, df in
                     cash_flow.items()}
        cash_flow = {key: filtrar_data_demonstrativo(df, dt) for key, df in cash_flow.items()}

        for key, df in cash_flow.items():
            if df is not None and not df.empty:
                cash_flow[key] = define_profile_plan(cash_flow[key], key, cash_flow_info)

        cash_flow = pd.concat(cash_flow).reset_index(drop=True)

        if not cash_flow.empty:
            cash_flow['Historico'] = cash_flow['Historico'].apply(normalize_text)

            cash_flow = executeFromTo(cash_flow, 'Historico', expenses_mapping)

            cash_flow['Cod Fundo'] = cash_flow['Cod Fundo'].str.zfill(6)

            cash_flow.drop('Data', axis=1, inplace=True)
            return cash_flow
        return pd.DataFrame()

    @classmethod
    def totalizar_entrada_saida(cls, demonstrativo):
        """Este métod realiza a totalização das entradas e saídas financeiras de forma independente, agrupando os
        valores de acordo com taxas ou fundos específicos"""
        if demonstrativo.empty:
            return pd.DataFrame()

        valores_demonstrativo = {}
        taxa_count = 0

        for index, row in demonstrativo.iterrows():
            fundo = row['Historico']
            entrada = row['Entrada']
            saida = row['Saida']
            plano = row['Plano']
            perfil = row['Perfil']
            cod_fundo = row['Cod Fundo']
            chave_composta = f'{cod_fundo}_{plano}_{perfil}_{"Pos" if entrada > 0 else "Neg"}'

            taxa_encontrada = False
            for taxa in cls.taxas_demonstrativo:
                if taxa in row['Historico']:
                    chave_composta_taxa = f'{chave_composta}_{taxa_count}'
                    valores_demonstrativo[chave_composta_taxa] = {
                        'Historico': fundo,
                        'Entrada': entrada,
                        'Saida': saida,
                        'Plano': plano,
                        'Perfil': perfil,
                        'Cod Fundo': cod_fundo
                    }
                    taxa_count += 1
                    taxa_encontrada = True
                    break
            if taxa_encontrada:
                continue
            if chave_composta in valores_demonstrativo:
                fundo_existente = valores_demonstrativo[chave_composta]
                # Verifica se há entrada positiva no fundo existente e na entrada atual
                if fundo_existente['Entrada'] > 0 and entrada > 0:
                    fundo_existente['Entrada'] += entrada
                # Verifica se há saída positiva no fundo existente e na saída atual
                elif fundo_existente['Saida'] > 0 and saida > 0:
                    fundo_existente['Saida'] += saida
                else:
                    # Se não se encaixar nas condições acima, cria uma nova entrada para a chave composta
                    valores_demonstrativo[chave_composta]['Entrada'] += entrada
                    valores_demonstrativo[chave_composta]['Saida'] += saida
            else:
                # Cria uma nova entrada no dicionário com a chave composta caso não exista
                valores_demonstrativo[chave_composta] = {
                    'Historico': fundo,
                    'Entrada': entrada,
                    'Saida': saida,
                    'Plano': plano,
                    'Perfil': perfil,
                    'Cod Fundo': cod_fundo
                }
        valores_demonstrativo = pd.DataFrame.from_dict(valores_demonstrativo, orient='index').reset_index()
        valores_demonstrativo = valores_demonstrativo[['Historico', 'Entrada', 'Saida', 'Plano', 'Perfil', 'Cod Fundo']]
        return valores_demonstrativo

    @classmethod
    def gerar_diferenca_entradas_saidas(cls, demonstrativo):
        """Este métod soma todas as entradas e saídas financeiras e armazena a diferença resultante, representando o
        saldo final que será alocado como saida ou entrada a depender do valor. Obs: a saida é usada no balanço
        patrimonial"""
        if demonstrativo.empty:
            return pd.DataFrame()

        valores_demonstrativo = {}
        for index, row in demonstrativo.iterrows():
            fundo = row['Historico']
            cod_fundo = row['Cod Fundo']
            entrada = row['Entrada']
            saida = row['Saida']
            plano = row['Plano']
            perfil = row['Perfil']
            chave_composta = f'{cod_fundo}_{plano}_{perfil}'

            if chave_composta in valores_demonstrativo:
                valores_demonstrativo[chave_composta]['Saida'] += saida
                valores_demonstrativo[chave_composta]['Entrada'] += entrada
                if valores_demonstrativo[chave_composta]['Saida'] != 0 and valores_demonstrativo[chave_composta][
                    'Entrada'] != 0:
                    diferenca = valores_demonstrativo[chave_composta]['Entrada'] + \
                                valores_demonstrativo[chave_composta]['Saida']
                    if diferenca < 0:
                        valores_demonstrativo[chave_composta]['Entrada'] = 0
                        valores_demonstrativo[chave_composta]['Saida'] = diferenca
                    else:
                        valores_demonstrativo[chave_composta]['Saida'] = 0
                        valores_demonstrativo[chave_composta]['Entrada'] = diferenca
            else:
                # Crie uma nova entrada no dicionário com a chave composta caso não exista
                valores_demonstrativo[chave_composta] = {
                    'Historico': fundo,
                    'Cod Fundo': cod_fundo,
                    'Entrada': entrada,
                    'Saida': saida,
                    'Plano': plano,
                    'Perfil': perfil
                }
        valores_demonstrativo = pd.DataFrame.from_dict(valores_demonstrativo, orient='index').reset_index()
        valores_demonstrativo = valores_demonstrativo[['Historico','Cod Fundo', 'Entrada', 'Saida', 'Plano', 'Perfil']]
        return valores_demonstrativo

    @classmethod
    def filtrar_registros(cls, demonstrativo):
        """Filtra os registros do DataFrame para incluir apenas aqueles relacionados a resgate, aquisicões, fundos e
        despesas. O objetivo é retornar um subconjunto de dados que é relevante para gerar o balanço patrimonial."""
        linhas_resg_aquis = []
        linhas_despesas = []
        linhas_fundos = []

        for index, row in demonstrativo.iterrows():
            if any(keyword in row['Historico'] for keyword in cls.taxas_demonstrativo):
                linhas_despesas.append(dict(row))
            elif ('RESGATE DE COTAS' in row['Historico'] or 'AQUISICAO DE COTAS' in row['Historico']):
                linhas_resg_aquis.append(dict(row))
            else:
                linhas_fundos.append(dict(row))

        linhas_despesas = pd.DataFrame(linhas_despesas)
        linhas_resg_aquis = pd.DataFrame(linhas_resg_aquis)
        demonstrativo_atualizado = pd.DataFrame(linhas_fundos)

        return linhas_resg_aquis, demonstrativo_atualizado, linhas_despesas
