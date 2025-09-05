import os
import pandas as pd
import math
import re
from datetime import datetime

fundos_dict = {
    '36518029000107': {'fundo': 'WESTERN MIRAN FIRFCP', 'fluxo_caixa': 'WESTERN MIRAN FIRFCP',
                       'classe': 'FUNDO INVESTIMENTO RENDA FIXA'},
    '20726076000106': {'fundo': 'FI RF VISAO PREV BRADESCO', 'fluxo_caixa': 'FI RF VISAO PREV BRA',
                       'classe': 'FUNDO INVESTIMENTO RENDA FIXA'},
    '18936232000111': {'fundo': 'ICATU VANGUARDA MIRANTE LIQUIDEZ FIRF', 'fluxo_caixa': 'ICA MIRANTE LIQ FIRF',
                       'classe': 'FUNDO INVESTIMENTO RENDA FIXA'},
    '37174176000170': {'fundo': 'BB AÇÕES GLOBAIS TEC', 'fluxo_caixa': 'BB ACOES GLOBAIS FIA',
                       'classe': 'FUNDO INVESTIMENTO EXTERIOR'},
    '52350495000182': {'fundo': 'ALTERNATIVOS MIR FIM', 'fluxo_caixa': 'ALTERNATIVOS MIR FIM',
                       'classe': 'MULTIMERCADO ESTRUTURADO'},
    '12636386000101': {'fundo': 'BRAD MIRANT ALM FIRF', 'fluxo_caixa': 'BRAD MIRANT ALM FIRF',
                       'classe': 'FUNDO INVESTIMENTO RENDA FIXA'},
    '20726130000113': {'fundo': 'FI RF VISAO PREV SANTANDER', 'fluxo_caixa': 'FI RF VISAO PREV SAN',
                       'classe': 'FUNDO INVESTIMENTO RENDA FIXA'},
    '32240211000198': {'fundo': 'WESTERN MIRANTE RFFI', 'fluxo_caixa': 'WESTERN MIRANTE RFFI',
                       'classe': 'FUNDO INVESTIMENTO RENDA FIXA'},
    '03079923000179': {'fundo': 'FI RF VISAO PREV II', 'fluxo_caixa': 'FI RF VISAO PREV II',
                       'classe': 'FUNDO INVESTIMENTO RENDA FIXA'},
    '28206291000198': {'fundo': 'FI RF VP WESTERN AS', 'fluxo_caixa': 'FI RF VP WESTERN AS',
                       'classe': 'FUNDO INVESTIMENTO RENDA FIXA'},
    '20726061000148': {'fundo': 'FI RF VISAO PREV ITAU', 'fluxo_caixa': 'FI RF VISAO PREV ITA',
                       'classe': 'FUNDO INVESTIMENTO RENDA FIXA'},
    '26978182000163': {'fundo': 'CSHG MIRANTE FIC FIM', 'fluxo_caixa': 'CSHG MIRANTE FIC FIM',
                       'classe': 'MULTIMERCADO ESTRUTURADO'},
    '21596641000120': {'fundo': 'FI RF PREVISÃO II', 'fluxo_caixa': 'FI RF PREVISAO II',
                       'classe': 'FUNDO INVESTIMENTO RENDA FIXA'},
    '39272865000142': {'fundo': 'BB ACOES B ASIA EX-JA FC FIA BDR ETF N I', 'fluxo_caixa': 'BB BOLSAS ASI FICFIA',
                       'classe': 'FUNDO INVESTIMENTO EXTERIOR'},
    '08035716000136': {'fundo': 'FIC DE FI AÇÕES IBRX', 'fluxo_caixa': 'FIC DE FI ACOES IBRX',
                       'classe': 'FUNDO INVESTIMENTO ACOES'},
    '03497804000136': {'fundo': 'SANTANDER FI INSTITUCIONAL RF MIRANTE', 'fluxo_caixa': 'SANTANDER FI INST RF',
                       'classe': 'FUNDO INVESTIMENTO RENDA FIXA'},
    '21595984000170': {'fundo': 'FI RF PREVISÃO I', 'fluxo_caixa': 'FI RF PREVISAO I',
                       'classe': 'FUNDO INVESTIMENTO RENDA FIXA'},
    '23732198000101': {'fundo': 'FI RF BRADESCO VP PGA', 'fluxo_caixa': 'FIRF BRADESCO VP PGA',
                       'classe': 'FUNDO INVESTIMENTO RENDA FIXA'},
    '36617679000100': {'fundo': 'ICATU VANGUARDA MIRANTE', 'fluxo_caixa': 'ICAT MIRANTE FIRF CP',
                       'classe': 'FUNDO INVESTIMENTO RENDA FIXA'},
    '19602288000100': {'fundo': 'BRADESCO FI RF MIRANTE', 'fluxo_caixa': 'BRAD FI RF MIRANTE',
                       'classe': 'FUNDO INVESTIMENTO RENDA FIXA'},
    '06182371000118': {'fundo': 'FOR-TE FIDC SENIOR', 'fluxo_caixa': 'FOR-TE FIDC SENIOR',
                       'classe': 'FUNDO INVESTIMENTO DIREITOS CREDITORIOS'},
    '18936235000155': {'fundo': 'BRADESCO MIRANTE LIQUIDEZ FIRF', 'fluxo_caixa': 'BRA MIRANTE LIQ FIRF',
                       'classe': 'FUNDO INVESTIMENTO RENDA FIXA'},
}
# codigo carteira | Sheetname | Plano | Perfil
planilhas_info = [
    ('010134', 'BRADESCO BD', 22, 3), #
    ('011607', 'BRADESCO PGA', 987, 19), #
    ('011828', 'BRADESCO PREVISÃO', 51, 21), #
    ('015723', 'VISÃO TELEF - SUPER CONSERVADOR', 49, 27), #
    ('015724', 'VISÃO TELF - CONSERVADOR', 49, 28), #
    ('015725', 'VISÃO TELF - MODERADO', 49, 29), #
    ('015726', 'VISÃO TELEF - AGRESSIVO', 49, 31), #
    ('015727', 'VISÃO TELEF - AGRESSIVO RF LP', 49, 30), #
    ('015728', 'VISÃO MULT - SUPER CONSERVADOR', 8, 22), #
    ('015729', 'VISÃO MULTI - CONSERVADOR', 8, 23), #
    ('015730', 'VISÃO MULTI - MODERADO', 8, 24), #
    ('015731', 'VISÃO MULTI - AGRESSIVO', 8, 26), #
    ('015732', 'VISÃO MULTI - AGRESSIVO RF LP', 8, 25), #
    ('017666', 'MAIS VISÃO - SUPER CONSERVADOR', 52, 32), #
    ('017667', 'MAIS VISÃO - CONSERVADOR', 52, 33),
    ('017668', 'MAIS VI SÃO - MODERADO', 52, 34), #
    ('017669', 'MAIS VISÃO - AGRESSIVO', 52, 36), #
    ('017670', 'MAIS VISÃO - AGRESSIVO RF LP', 52, 35), #
    ('017671', 'MAIS VISÃO - PGA', 952, 20), #
]

provisao_dict = {
    '15': 'Taxa CUSTODIA',
    '13': 'Taxa CETIP',
    '47': '',
    '34': 'Taxa administracao',
    '8': 'Tarifa de liquidacao financeira'
}

taxas_demonstrativo = ('IOF',

                       'Taxa CUSTODIA',
                       'Taxa CETIP',
                       'Taxa administracao',
                       'Tarifa de liquidacao financeira',

                       'Ajuste de Taxa CETIP',
                       'Ajuste de Taxa SELIC',
                       'Despesa de CUSTO SELIC',
                       'Despesa de CUSTO CETIP',
                       'Taxa de Custodia Bruta',
                       'Tx de Controladoria s/ Tx de Admin.',
                       'Ajuste de TARIFA DE LIQUIDACAO FINANCEIRA',
                       'Despesa - SELIC',
                       'Despesa - CETIP',
                       'Despesa de B 10 - TARIFA DE LIQUIDACAO FINANCEIRA',
                       'Despesa de B 10 - TARIFA DE LIQUIDAÇÃO FINANCEIRA',
                       'TARIFA DE LIQUIDACAO FINANCEIRA'
                       )
contaPagarReceber = {
    'Taxa CUSTODIA': {'Plano': 20103100101000, 'PGA': 20103100102000, 'Despesa': 50298990100000},
    'Tx de Controladoria s/ Tx de Admin.': {'Plano': 20103100101000, 'PGA': 20103100102000,
                                            'Despesa': 50298990200000},
    'Taxa CETIP': {'Plano': 20103100101000, 'PGA': 20103100102000, 'Despesa': 50298990300000},
    'Despesa de CUSTO SELIC': {'Plano': 20103100101000, 'PGA': 20103100102000, 'Despesa': 50298990300000},
    'Tarifa de liquidacao financeira': {'Plano': 20103100101000, 'PGA': 20103100102000, 'Despesa': 50298999900000},
    'Despesa de B 10 - TARIFA DE LIQUIDACAO FINANCEIRA': {'Plano': 20103100101000, 'PGA': 20103100102000,
                                                          'Despesa': 50298999900000}
}
base_path = os.path.expanduser("~/Documentos/investimentos/")

base_path_demonstrativos = os.path.expanduser("~/Documentos/demonstrativos/")

data = '2025-01-31'
ano, mes, dia = data.split('-')

data_ant = '2025-01-30'
ano_ant, mes_ant, dia_ant = data_ant.split('-')

path = os.path.expanduser(f'~/Documentos/Carteiras/{dia}_{mes}/')
carteira_files = os.listdir(path)

path_carteira_anterior = os.path.expanduser(f'~/Documentos/Carteiras/{dia_ant}_{mes_ant}/')
carteira_files_anterior = os.listdir(path_carteira_anterior)

path_demonstrativo = os.path.expanduser('~/Documentos/demonstrativos/')
demonstrativos_list = os.listdir(path_demonstrativo)

fundos = os.path.expanduser(f'~/Documentos/consulta_fundo.xlsx')

titulos_carteira = ['Cod Fundo', 'Fundo', 'Valor Atual']

df_fundos = pd.read_excel(fundos, sheet_name="para")

titulos_demonstrativo = ['Data', 'Historico', 'Entrada', 'Saida']

data_obj = datetime.strptime(data, "%Y-%m-%d")
data_demonstrativo = data_obj.strftime("%d/%m/%Y")


def extrair_valor(texto):
    inicio = texto.find('Fundo')
    fim = texto.find('[')
    if inicio > 0 and fim > 0:
        valor = texto[inicio + 5:fim].strip()
        return valor
    return texto


def pesquisar_dados_por_data(df, data_fundo):
    demonstrativo = []
    coleta_ativa = False
    for index, row in df.iterrows():
        if 'Tx' in row['Historico']:
            print('to aq')
        if coleta_ativa:
            if pd.notna(row['Data']):
                if 'Saldo' in row['Historico']:
                    continue
                else:
                    break
            if 'Saldo' not in row['Historico']:
                historico = extrair_valor(row['Historico'])
                demonstrativo.append((historico, row['Entrada'], row['Saida'], row['Plano'], row['Perfil']))
        elif pd.notna(row['Data']) and row['Data'] == data_fundo and 'Saldo' not in row['Historico']:
            coleta_ativa = True
            # Extrair valores numéricos do Histórico e armazená-los em 'cod fundo'
            historico = extrair_valor(row['Historico'])
            demonstrativo.append((historico, row['Entrada'], row['Saida'], row['Plano'], row['Perfil']))
    return demonstrativo

def substituir_nome(df, coluna, nome_antigo, nome_novo):
    df[coluna] = df[coluna].str.replace(nome_antigo, nome_novo)
    return df

def levantar_entrada_saida(demonstrativo, taxas_demonstrativo):
    valores_demonstrativo = {}
    taxa_count = 0

    for index, row in demonstrativo.iterrows():
        fundo = row['Historico']
        entrada = row['Entrada']
        saida = row['Saida']
        plano = row['Plano']
        perfil = row['Perfil']
        chave_composta = f'{fundo}_{plano}_{perfil}_{"Pos" if entrada > 0 else "Neg"}'

        taxa_encontrada = False
        for taxa in taxas_demonstrativo:
            if taxa in row['Historico']:
                chave_composta_taxa = f'{chave_composta}_{taxa_count}'
                valores_demonstrativo[chave_composta_taxa] = {
                    'Historico': fundo,
                    'Entrada': entrada,
                    'Saida': saida,
                    'Plano': plano,
                    'Perfil': perfil
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
                'Perfil': perfil
            }
    valores_demonstrativo = pd.DataFrame.from_dict(valores_demonstrativo, orient='index').reset_index()
    valores_demonstrativo = valores_demonstrativo[['Historico', 'Entrada', 'Saida', 'Plano', 'Perfil']]
    return valores_demonstrativo


def somar_entrada_saida(demonstrativo):
    valores_demonstrativo = {}
    for index, row in demonstrativo.iterrows():
        fundo = row['Historico']
        entrada = row['Entrada']
        saida = row['Saida']
        plano = row['Plano']
        perfil = row['Perfil']
        chave_composta = f'{fundo}_{plano}_{perfil}'

        if chave_composta in valores_demonstrativo:
            valores_demonstrativo[chave_composta]['Saida'] += saida
            valores_demonstrativo[chave_composta]['Entrada'] += entrada
            if valores_demonstrativo[chave_composta]['Saida'] != 0 and valores_demonstrativo[chave_composta][
                'Entrada'] != 0:
                diferenca = valores_demonstrativo[chave_composta]['Entrada'] + valores_demonstrativo[chave_composta][
                    'Saida']
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
                'Entrada': entrada,
                'Saida': saida,
                'Plano': plano,
                'Perfil': perfil
            }
    valores_demonstrativo = pd.DataFrame.from_dict(valores_demonstrativo, orient='index').reset_index()
    valores_demonstrativo = valores_demonstrativo[['Historico', 'Entrada', 'Saida', 'Plano', 'Perfil']]
    return valores_demonstrativo


def filtrar_resgates_aquisicoes_despesas(demonstrativo, taxas_demonstrativo):
    linhas_resg_aquis = []
    linhas_despesas = []
    linhas_fundos = []

    for index, row in demonstrativo.iterrows():
        if any(keyword in row['Historico'] for keyword in taxas_demonstrativo):
            linhas_despesas.append(dict(row))
        elif 'Resgate de Cotas' in row['Historico'] or 'Aquisicao de Cotas' in row['Historico']:
            linhas_resg_aquis.append(dict(row))
        else:
            linhas_fundos.append(dict(row))

    linhas_despesas = pd.DataFrame(linhas_despesas)
    linhas_resg_aquis = pd.DataFrame(linhas_resg_aquis)
    demonstrativo_atualizado = pd.DataFrame(linhas_fundos)

    return linhas_resg_aquis, demonstrativo_atualizado, linhas_despesas


def mapear_classificacoes(df, consulta_classificao):
    consulta_classificao['Cod Fundo'] = consulta_classificao['Cod Fundo'].astype(str).apply(
        lambda x: x.zfill(6) if x.isdigit() else x)
    mapeamento = consulta_classificao.set_index("Cod Fundo")["Classificacao CVM"].to_dict()
    df["Classificacao"] = df["Cod Fundo"].map(mapeamento)
    return df


def criar_rendimentos(df_carteira, df_saldo_anterior, demonstrativos_entrada_saida):
    # Crie listas para armazenar os dados
    fundo_lista = []
    plano_lista = []
    perfil_lista = []
    classificacao_lista = []
    valor_atual_lista = []
    saldo_anterior_lista = []
    entrada_lista = []
    saida_lista = []
    rendimento_lista = []  # Lista para armazenar o rendimento

    # Itera pelas linhas do DataFrame de carteira
    for index, row in df_carteira.iterrows():
        fundo = row['Fundo']
        plano = row['Plano']
        perfil = row['Perfil']
        valor_atual = row['Valor Atual']
        classe = row['Classificacao']

        # Verifica se há uma correspondência no DataFrame de saldo anterior
        saldo_anterior_row = df_saldo_anterior[
            (df_saldo_anterior['Fundo'] == fundo) & (df_saldo_anterior['Plano'] == plano)
            & (df_saldo_anterior['Perfil'] == perfil)
            ]

        if not saldo_anterior_row.empty:
            saldo_anterior = saldo_anterior_row.iloc[0]["Valor Atual"]
        else:
            saldo_anterior = 0

        if not demonstrativos_entrada_saida.empty:
            # Verifica se há uma correspondência no DataFrame de resultados
            resultados_row = demonstrativos_entrada_saida[(demonstrativos_entrada_saida['Historico'] == fundo) &
                                                          (demonstrativos_entrada_saida['Plano'] == plano) &
                                                          (demonstrativos_entrada_saida['Perfil'] == perfil)]
        else:
            resultados_row = pd.DataFrame()
        if not resultados_row.empty:
            entrada = resultados_row.iloc[0]['Saida']
            saida = resultados_row.iloc[0]['Entrada']
        else:
            entrada = 0
            saida = 0

        if entrada != 0 or saida != 0:
            entrada = entrada * -1
            saida = saida * -1

        rendimento = valor_atual - saldo_anterior - entrada - saida  # Calcula o rendimento

        # Adicione os dados às listas
        fundo_lista.append(fundo)
        plano_lista.append(plano)
        perfil_lista.append(perfil)
        classificacao_lista.append(classe)
        valor_atual_lista.append(valor_atual)
        saldo_anterior_lista.append(saldo_anterior)
        entrada_lista.append(entrada)
        saida_lista.append(saida)
        rendimento_lista.append(rendimento)  # Adiciona o rendimento à lista

    # Crie um DataFrame final a partir das listas, incluindo a coluna 'Rendimento'
    df_final = pd.DataFrame({
        'Fundo': fundo_lista,
        'Plano': plano_lista,
        'Perfil': perfil_lista,
        'Classificacao': classificacao_lista,
        'Saldo Anterior': saldo_anterior_lista,
        'Entrada': entrada_lista,
        'Saida': saida_lista,
        'Saldo Atual': valor_atual_lista,
        'Rendimento': rendimento_lista
    })
    return df_final


def processar_lancamento_contabil(df_rendimentos, demonstrativos, df_fundos):
    finalProtheus = []
    for index, row in df_rendimentos.iterrows():
        plano = row['Plano']
        perfil = row['Perfil']
        fundo = row['Fundo']
        rendimentos = row['Rendimento']
        rendimentos = round(rendimentos, 2)
        print(fundo)
        conta_rentabilidade_positiva = df_fundos.loc[df_fundos['Nome do Fundo'] == fundo, 'Rentabilidade Positiva'].values[0]
        conta_rentabilidade_negativa = df_fundos.loc[df_fundos['Nome do Fundo'] == fundo, 'Rentabilidade Negativa'].values[0]
        conta_custo_atualizado = df_fundos.loc[df_fundos['Nome do Fundo'] == fundo, 'Custo Atualizado'].values[0]

        if rendimentos < 0:
            finalProtheus.append(criar_lancamento_contabil(
                conta_rentabilidade_negativa, abs(rendimentos), 'D', f'Rent. negativa {fundo}', plano, perfil))
            finalProtheus.append(criar_lancamento_contabil(
                conta_custo_atualizado, abs(rendimentos), 'C', f'Rent. negativa {fundo}', plano, perfil))
        if rendimentos > 0:
            finalProtheus.append(criar_lancamento_contabil(
                conta_custo_atualizado, rendimentos, 'D', f'Rent. positiva {fundo}', plano, perfil))
            finalProtheus.append(criar_lancamento_contabil(
                conta_rentabilidade_positiva, rendimentos, 'C', f'Rent. positiva {fundo}', plano, perfil))

    if not demonstrativos.empty:
        for index, row in demonstrativos.iterrows():
            fundo = row['Historico']
            entrada = row['Entrada']
            saida = row['Saida']
            plano = row['Plano']
            perfil = row['Perfil']

            contaContabil_carteira = df_fundos.loc[
                (df_fundos['Plano'] == plano) &
                (df_fundos['Perfil'] == perfil)
                ]['Investimentos'].values[0]

            contaAplicFundo = df_fundos.loc[(df_fundos['Plano'] == plano) &
                                            (df_fundos['Perfil'] == perfil) &
                                            (df_fundos['Nome do Fundo'] == fundo)]['Aplicacao'].values[0]
            contaResgFundo = df_fundos.loc[(df_fundos['Plano'] == plano) &
                                           (df_fundos['Perfil'] == perfil) &
                                           (df_fundos['Nome do Fundo'] == fundo)]['Resgate'].values[0]
            if entrada:
                entrada = round(entrada, 2)
                finalProtheus.append(criar_lancamento_contabil(
                    contaContabil_carteira, abs(entrada), 'D', f'Resg. no {fundo}', plano, perfil))
                finalProtheus.append(criar_lancamento_contabil(
                    contaAplicFundo, abs(entrada), 'C', f'Resg. no {fundo}', plano, perfil))

            if saida:
                saida = round(saida, 2)
                finalProtheus.append(criar_lancamento_contabil(
                    contaResgFundo, abs(saida), 'D', f'Aplic. no {fundo}', plano, perfil))
                finalProtheus.append(criar_lancamento_contabil(
                    contaContabil_carteira, abs(saida), 'C', f'Aplic. no {fundo}', plano, perfil))
    finalProtheus = pd.DataFrame(finalProtheus)
    return finalProtheus


def criar_lancamento_contabil(conta, valor, d_c, historico, plano, perfil):
    return {
        'Conta contabil': conta,
        'Valor': valor,
        'D/C': d_c,
        'Historico de lancamento': historico,
        'CC': 2,
        'Plano': plano,
        'Perfil': perfil
    }


def processar_taxa(taxas, df_despesas):
    finalProtheus = []
    for index, row in df_despesas.iterrows():
        valor = row['Valor']
        plano = row['Plano']
        perfil = row['Perfil']
        despesa = row['Despesa']
        round(valor, 2)
        for taxa in taxas:
            if taxa in despesa:
                lancamento1 = None
                lancamento2 = None

                if (plano, perfil) != (987, 19) and (plano, perfil) != (952, 20):
                    lancamento1 = criar_lancamento_contabil(contaPagarReceber[taxa]['Despesa'], abs(valor), 'D', taxa,
                                                            plano, perfil)
                    lancamento2 = criar_lancamento_contabil(contaPagarReceber[taxa]['Plano'], abs(valor), 'C', taxa,
                                                            plano, perfil)

                if (plano, perfil) == (987, 19) or (plano, perfil) == (952, 20):
                    lancamento1 = criar_lancamento_contabil(contaPagarReceber[taxa]['Despesa'], abs(valor), 'D', taxa,
                                                            plano, perfil)
                    lancamento2 = criar_lancamento_contabil(contaPagarReceber[taxa]['PGA'], abs(valor), 'C', taxa,
                                                            plano, perfil)

                # Adicionar os lançamentos apenas se eles não forem None
                if lancamento1:
                    finalProtheus.append(lancamento1)
                if lancamento2:
                    finalProtheus.append(lancamento2)
                break
    finalProtheus = pd.DataFrame(finalProtheus)
    return finalProtheus


def despesas_taxas_demonstrativo(df_despesas, df_fundos, taxaDemonstrativo):
    finalProtheus = []
    for index, row in df_despesas.iterrows():
        taxas = 'Despesa de CUSTO CETIP', 'Tx de Controladoria s/ Tx de Admin.', 'Taxa de Custodia Bruta'
        fundo = row['Historico']
        plano = row['Plano']
        perfil = row['Perfil']
        saida = row['Saida']
        entrada = row['Entrada']
        contaContabil_carteira = df_fundos.loc[
            (df_fundos['Plano'] == plano) &
            (df_fundos['Perfil'] == perfil)
            ]['Investimentos'].values[0]
        if (plano == 987 and perfil == 19) or (plano == 952 and perfil == 20):
            if entrada != 0:
                valor = abs(entrada)
                if fundo in taxas:
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaPagarReceber['Despesa de CUSTO CETIP']['PGA'], valor, 'C', fundo, plano,
                        perfil))
                    continue
                if fundo == 'Ajuste de Taxa CETIP' or fundo == 'Ajuste de Taxa SELIC':
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaPagarReceber['Taxa CETIP']['Despesa'], valor, 'C', fundo, plano, perfil))
                    continue
                if 'Despesa de B' in fundo:
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaPagarReceber['Tarifa de liquidacao financeira']['PGA'], valor, 'C', fundo, plano, perfil))
                    continue
                if fundo == 'AJUSTE DE TARIFA DE LIQUIDACAO FINANCEIRA' or fundo == 'Ajuste de TARIFA DE LIQUIDACAO FINANCEIRA':
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaPagarReceber['Tarifa de liquidacao financeira']['Despesa'], valor, 'C', fundo, plano, perfil))
                    continue
            if saida != 0:
                valor = abs(saida)
                if fundo in taxas:
                    finalProtheus.append(criar_lancamento_contabil(
                        contaPagarReceber['Taxa CETIP']['PGA'], valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'C', fundo, plano, perfil))
                    continue
                if fundo == 'Ajuste de Taxa CETIP' or fundo == 'Ajuste de Taxa SELIC':
                    finalProtheus.append(criar_lancamento_contabil(
                        contaPagarReceber['Taxa CETIP']['Despesa'], valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'C', fundo, plano, perfil))
                    continue
                if 'Despesa de B' in fundo:
                    finalProtheus.append(criar_lancamento_contabil(
                        contaPagarReceber['Tarifa de liquidacao financeira']['PGA'], valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'C', fundo, plano, perfil))
                    continue
                if fundo == 'AJUSTE DE TARIFA DE LIQUIDACAO FINANCEIRA' or fundo == 'Ajuste de TARIFA DE LIQUIDACAO FINANCEIRA':
                    finalProtheus.append(criar_lancamento_contabil(
                        contaPagarReceber['Tarifa de liquidacao financeira']['Despesa'], valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'C', fundo, plano, perfil))
                    continue
        else:
            if entrada != 0:
                valor = abs(entrada)
                if fundo in taxas:
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaPagarReceber['Taxa CETIP']['Plano'], valor, 'C', fundo, plano, perfil))
                    continue
                if fundo == 'Ajuste de Taxa CETIP' or fundo == 'Ajuste de Taxa SELIC':
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaPagarReceber['Taxa CETIP']['Despesa'], valor, 'C', fundo, plano, perfil))
                    continue
                if 'Despesa de B' in fundo:
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaPagarReceber['Tarifa de liquidacao financeira']['Plano'], valor, 'C', fundo, plano,
                        perfil))
                    continue
                if fundo == 'AJUSTE DE TARIFA DE LIQUIDACAO FINANCEIRA' or fundo == 'Ajuste de TARIFA DE LIQUIDACAO FINANCEIRA':
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaPagarReceber['Tarifa de liquidacao financeira']['Despesa'], valor, 'C', fundo, plano,
                        perfil))
                    continue
            if saida != 0:
                valor = abs(saida)
                if fundo in taxas:
                    finalProtheus.append(criar_lancamento_contabil(
                        contaPagarReceber['Taxa CETIP']['Plano'], valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'C', fundo, plano, perfil))
                    continue
                if fundo == 'Ajuste de Taxa CETIP' or fundo == 'Ajuste de Taxa SELIC':
                    finalProtheus.append(criar_lancamento_contabil(
                        contaPagarReceber['Taxa CETIP']['Despesa'], valor, 'D', fundo, plano, perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'C', fundo, plano, perfil))
                    continue
                if 'Despesa de B' in fundo:
                    finalProtheus.append(criar_lancamento_contabil(
                        contaPagarReceber['Tarifa de liquidacao financeira']['Plano'], valor, 'D', fundo, plano,
                        perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'C', fundo, plano, perfil))
                    continue
                if fundo == 'AJUSTE DE TARIFA DE LIQUIDACAO FINANCEIRA' or fundo == 'Ajuste de TARIFA DE LIQUIDACAO FINANCEIRA':
                    finalProtheus.append(criar_lancamento_contabil(
                        contaPagarReceber['Tarifa de liquidacao financeira']['Despesa'], valor, 'D', fundo, plano,
                        perfil))
                    finalProtheus.append(criar_lancamento_contabil(
                        contaContabil_carteira, valor, 'C', fundo, plano, perfil))
                    continue
    finalProtheus = pd.DataFrame(finalProtheus)
    return finalProtheus


def procurar_palavra(df, coluna, palavra_chave):
    filtro = df[coluna].str.contains(palavra_chave, case=False)
    resultado = df[filtro]

    resultado['Conta contabil'] = resultado['Conta contabil'].astype(str)
    resultado = ordenar_coluna(resultado, 'Plano', 'Perfil')
    return resultado


def ordenar_coluna(df, coluna1, coluna2=None):
    if coluna1 and coluna2:
        return df.sort_values(by=[coluna1, coluna2], ascending=[True, True])
    else:
        return df.sort_values(by=coluna1)


def filtrar_dados(df, lista_palavras):
    # Cria um filtro booleano para as linhas que contêm parcialmente alguma palavra da lista
    filtro = df['Historico de lancamento'].str.contains('|'.join(lista_palavras), case=False, regex=True)

    # Aplica o filtro ao DataFrame original para obter um novo DataFrame
    novo_df = df[filtro]
    novo_df['Conta contabil'] = novo_df['Conta contabil'].astype(str)
    novo_df = ordenar_coluna(novo_df, 'Plano', 'Perfil')
    return novo_df


def prepararDemonstrativos(info, path_demonstrativo, data_demonstrativo, titulos_demonstrativo):
    carteira_id = info[0]
    plano = info[2]
    perfil = info[3]

    df_demonstrativo = pd.DataFrame(columns=titulos_demonstrativo + ['Plano', 'Perfil'])
    for file in path_demonstrativo:
        if carteira_id in file:
            df = pd.read_excel(f"{base_path_demonstrativos}/{file}", skiprows=8, header=None)
            df = df.iloc[:, 0:4]
            df.columns = titulos_demonstrativo

            df['Data'] = data_demonstrativo
            df["Plano"] = plano
            df["Perfil"] = perfil
            df = pesquisar_dados_por_data(df, data_demonstrativo)
            df = pd.DataFrame(df)

            df.columns = ['Historico', 'Entrada', 'Saida', 'Plano', 'Perfil']

            df['Data'] = data_demonstrativo

            df_demonstrativo = pd.concat([df_demonstrativo, df])
            break

    return df_demonstrativo


def prepararCarteiras(info, path, arquivos_carteira, titulos_carteira):
    carteira_id = info[0]
    plano = info[2]
    perfil = info[3]

    df_carteira = pd.DataFrame(columns=titulos_carteira + ['Plano', 'Perfil'])
    for file in arquivos_carteira:
        if carteira_id in file:
            df = pd.read_excel(f"{path}/{file}", skiprows=11, header=None)
            df = df.iloc[:, [0, 1, 7]]
            df.columns = titulos_carteira
            df["Plano"] = plano
            df["Perfil"] = perfil

            total_index = df[df['Cod Fundo'] == 'Total'].index.min()
            if not pd.isna(total_index):
                df = df.iloc[:total_index]
            df = df.dropna(thresh=df.shape[1] - 2 + 1)
            df_carteira = pd.concat([df_carteira, df])
            break

    return df_carteira


def prepararDespesas(info, path, arquivos_despesas):
    carteira_id = info[0]
    plano = info[2]
    perfil = info[3]

    df_despesas_atual = pd.DataFrame(columns=['Despesa', 'Valor', 'Plano', 'Perfil'])

    for file in arquivos_despesas:
        if carteira_id in file:
            df_despesas = pd.read_excel(f"{path}/{file}", header=None)
            df_despesas = df_despesas.iloc[:, [0, 1]]
            df_despesas.columns = ['Despesa', 'Valor']
            df_despesas["Plano"] = plano
            df_despesas["Perfil"] = perfil
            df_despesas['Valor'] = pd.to_numeric(df_despesas['Valor'], errors='coerce')

            # Filtra entre 'Descrição' e 'TOTAL'
            descricao_idx = df_despesas[df_despesas['Despesa'] == 'Descrição'].index
            total_idx = df_despesas[df_despesas['Despesa'] == 'TOTAL'].index
            if not descricao_idx.empty and not total_idx.empty:
                descricao_idx = descricao_idx[0]
                total_idx = total_idx[0]
                df_despesas_filtrado = df_despesas.iloc[descricao_idx + 1:total_idx]
                df_despesas_atual = pd.concat([df_despesas_atual, df_despesas_filtrado])
            break

    return df_despesas_atual

def main():
    dataframes_demonstrativos = []
    carteiras = []
    carteira_anterior = []
    despesas = []
    provisao_retiradas_1 = []
    provisao_retiradas_2 = []

    for info in planilhas_info:
        df = prepararDemonstrativos(info, demonstrativos_list, data_demonstrativo, titulos_demonstrativo)
        if not df.empty:
            dataframes_demonstrativos.append(df)

    for info in planilhas_info:
        df_carteira = prepararCarteiras(info, path, carteira_files, titulos_carteira)
        df_carteira_anterior = prepararCarteiras(info, path_carteira_anterior, carteira_files_anterior,
                                                 titulos_carteira)
        if not df_carteira.empty:
            carteiras.append(df_carteira)
        if not df_carteira_anterior.empty:
            carteira_anterior.append(df_carteira_anterior)

        # if "29" in data or "30" in data or "25" in data:
        df_despesa = prepararDespesas(info, path, carteira_files)
        provisao_retiradas_atual = prepararDespesas(info, path, carteira_files)
        provisao_retiradas_anterior = prepararDespesas(info, path_carteira_anterior, carteira_files_anterior)
        if not df_despesa.empty:
            despesas.append(df_despesa)
            provisao_retiradas_1.append(provisao_retiradas_atual)
            provisao_retiradas_2.append(provisao_retiradas_anterior)

    demonstrativos = pd.concat(dataframes_demonstrativos, axis=0, ignore_index=True)

    #####
    despesas_filter = demonstrativos.apply(lambda despesa: despesa.isin(taxas_demonstrativo))

    df_despesas = pd.concat(despesas, axis=0, ignore_index=True)
    df_despesas = df_despesas.loc[~df_despesas['Despesa'].str.contains('Resgate do', case=False, na=False)]

    provisao_retiradas = pd.concat(provisao_retiradas_1, axis=0, ignore_index=True)
    provisao_retiradas_ant = pd.concat(provisao_retiradas_2, axis=0, ignore_index=True)

    provisao_retiradas = provisao_retiradas.loc[
        provisao_retiradas['Despesa'].str.contains('Resgate do', case=False, na=False)]
    provisao_retiradas_ant = provisao_retiradas_ant.loc[
        provisao_retiradas_ant['Despesa'].str.contains('Resgate do', case=False, na=False)]

    if not provisao_retiradas.empty:
        provisao_retiradas['Despesa'] = provisao_retiradas['Despesa'].apply(lambda value: extrair_valor(value))

    if not provisao_retiradas_ant.empty:
        provisao_retiradas_ant['Despesa'] = provisao_retiradas_ant['Despesa'].apply(lambda value: extrair_valor(value))

    carteira_atual = pd.concat(carteiras, axis=0, ignore_index=True)

    carteira_atual = pd.merge(carteira_atual, provisao_retiradas, left_on=['Fundo', 'Plano', 'Perfil'],
                              right_on=['Despesa', 'Plano', 'Perfil'], how='left')
    carteira_atual['Valor Atual'] = carteira_atual['Valor Atual'].fillna(0) + carteira_atual['Valor'].fillna(0)

    carteira_anterior = pd.concat(carteira_anterior, axis=0, ignore_index=True)

    # ========== Relatorio ==========
    provisao_ant_copy = provisao_retiradas_ant.groupby(['Despesa', 'Plano', 'Perfil'])['Valor'].sum().reset_index()

    provisao_ant_copy = provisao_retiradas_ant.groupby(['Plano', 'Perfil'])['Valor'].sum().reset_index()

    relatorio_conciliacao = carteira_anterior.groupby(['Plano', 'Perfil'])['Valor Atual'].sum().reset_index()
    relatorio_conciliacao = relatorio_conciliacao.merge(provisao_ant_copy, on=['Plano', 'Perfil'], how='left')
    relatorio_conciliacao['Valor'].fillna(0, inplace=True)
    relatorio_conciliacao['Total'] = relatorio_conciliacao[['Valor Atual', 'Valor']].sum(axis=1)

    relatorio_conciliacao['Dia'] = f'{dia_ant}/{mes_ant}'
    relatorio_conciliacao.rename(columns={'Valor Atual': 'Total liquido', 'Valor': 'Total contas a receber'},
                                 inplace=True)

    relatorio_conciliacao.drop('Despesa', axis=1, inplace=True, errors='ignore')

    # ordenando os campos
    relatorio_conciliacao = relatorio_conciliacao[
        ['Plano', 'Perfil', 'Dia', 'Total liquido', 'Total contas a receber', 'Total']]
    relatorio_conciliacao.to_excel(os.path.join(base_path, f'relatorio_provisao_{dia_ant}-{mes_ant}.xlsx'), index=False)

    carteira_anterior = pd.merge(carteira_anterior, provisao_retiradas_ant, left_on=['Fundo', 'Plano', 'Perfil'],
                                 right_on=['Despesa', 'Plano', 'Perfil'], how='left')
    carteira_anterior['Valor Atual'] = carteira_anterior['Valor Atual'].fillna(0) + carteira_anterior['Valor'].fillna(0)

    if not df_despesas.empty:
        df_despesas.loc[df_despesas['Despesa'].str.contains(
            'Despesa de B 10'), 'Despesa'] = 'Despesa de B 10 - TARIFA DE LIQUIDACAO FINANCEIRA'

        df_despesas.loc[df_despesas['Despesa'].str.contains(
            'Tx Custódia Bruta'), 'Despesa'] = 'Taxa CUSTODIA'

        df_despesas.loc[df_despesas['Despesa'].str.contains(
            'CUSTO CETIP'), 'Despesa'] = 'Taxa CETIP'

        df_despesas.loc[df_despesas['Despesa'].str.contains(
            'Tx de Controladoria s/'), 'Despesa'] = 'Tx de Controladoria s/ Tx de Admin.'

    df_resultado_provisao = pd.DataFrame()
    if not df_despesas.empty and "30" in data:
        df_resultado_provisao = processar_taxa(taxas_demonstrativo, df_despesas)

    carteira_atual = substituir_nome(carteira_atual, 'Cod Fundo', '17760', '017760')
    carteira_atual = substituir_nome(carteira_atual, 'Fundo', 'FIC DE FI AÇÕES IBRX', 'FIC DE FI ACOES IBRX')
    carteira_atual = substituir_nome(carteira_atual, 'Fundo', 'ALTERNA MIRANTE FICM', 'ALTERNATIVOS MIR FIM')

    carteira_anterior = substituir_nome(carteira_anterior, 'Cod Fundo', '17760', '017760')
    carteira_anterior = substituir_nome(carteira_anterior, 'Fundo', 'FIC DE FI AÇÕES IBRX', 'FIC DE FI ACOES IBRX')

    demonstrativos = substituir_nome(demonstrativos, 'Historico', 'LIQUIDAÃ‡ÃƒO FINANCEIRA', 'LIQUIDACAO FINANCEIRA')
    demonstrativos = substituir_nome(demonstrativos, 'Historico', 'Tx de Controladoria s/ Tx de Admin. [BBDC] Bruta',
                                     'Tx de Controladoria s/ Tx de Admin.')
    demonstrativos = substituir_nome(demonstrativos, 'Historico', 'Taxa de Custódia Bruta', 'TAXA DE CUSTODIA')
    demonstrativos = substituir_nome(demonstrativos, 'Historico', 'FIC DE FI AÇÕES IBRX', 'FIC DE FI ACOES IBRX')
    demonstrativos = substituir_nome(demonstrativos, 'Historico', 'Aquisição de Cotas', 'Aquisicao de Cotas')
    demonstrativos = levantar_entrada_saida(demonstrativos, taxas_demonstrativo)
    entrada_saida_rendimento = somar_entrada_saida(demonstrativos)
    linhas_aquis_resg, demonstrativos, linhas_desp_demonstrativo = filtrar_resgates_aquisicoes_despesas(demonstrativos,
                                                                                                        taxas_demonstrativo)

    df_resultado_taxas = pd.DataFrame()
    if not linhas_desp_demonstrativo.empty:
        df_resultado_taxas = despesas_taxas_demonstrativo(linhas_desp_demonstrativo, df_fundos, taxas_demonstrativo)

    carteira_atual = mapear_classificacoes(carteira_atual, df_fundos)
    carteira_anterior = mapear_classificacoes(carteira_anterior, df_fundos)
    carteira_anterior = substituir_nome(carteira_anterior, 'Fundo', 'ALTERNA MIRANTE FICM', 'ALTERNATIVOS MIR FIM')

    rendimento = criar_rendimentos(carteira_atual, carteira_anterior, entrada_saida_rendimento)
    rendimento = substituir_nome(rendimento, 'Fundo', 'BB ACOES GL HEDGE IE', 'BB ACOES GLOBAIS FIA')

    df_rentabilidade = processar_lancamento_contabil(rendimento, demonstrativos, df_fundos)

    df_protheus = pd.concat([df_resultado_taxas, df_rentabilidade, df_resultado_provisao], axis=0, ignore_index=True)

    aplic = 'Aplic. no'
    df_aplic = procurar_palavra(df_protheus, 'Historico de lancamento', aplic)

    resg = 'Resg. no'
    df_resg = procurar_palavra(df_protheus, 'Historico de lancamento', resg)

    lista_rentabilidade = 'Rent. positiva', 'Rent. negativa'
    filtro_rent = filtrar_dados(df_protheus, lista_rentabilidade)

    lista_taxas = 'IOF', 'TARIFA DE LIQUIDACAO FINANCEIRA', 'Despesa de CUSTO CETIP', 'Taxa CETIP', 'Tx Custodia Bruta', 'Tx de Controladoria s/ Tx de Admin.', 'Ajuste de Taxa SELIC', 'Ajuste de TARIFA DE LIQUIDACAO FINANCEIRA', 'Ajuste de Taxa CETIP', 'Taxa de Custodia Bruta'
    filtro_desp = filtrar_dados(df_protheus, taxas_demonstrativo)

    os.makedirs(base_path, exist_ok=True)

    # Define os caminhos dos arquivos
    path_lancamentos_segregado = os.path.join(base_path, f"lancamentos_segregado{dia}-{mes}.xlsx")
    path_evolucao_patrimonial = os.path.join(base_path, f"evolucao_patrimonial{dia}-{mes}.xlsx")
    path_lancamentos_protheus = os.path.join(base_path, f"lancamentos_protheus{dia}-{mes}.csv")

    # Salvando os DataFrames no Excel
    with pd.ExcelWriter(path_lancamentos_segregado) as writer:
        filtro_desp.to_excel(writer, sheet_name=f'Despesas_{dia}_{mes}_{ano}', index=False)
        filtro_rent.to_excel(writer, sheet_name=f'Rentabilidade_{dia}_{mes}_{ano}', index=False)
        df_aplic.to_excel(writer, sheet_name=f'Aplicacao_{dia}_{mes}_{ano}', index=False)
        df_resg.to_excel(writer, sheet_name=f'Resgate_{dia}_{mes}_{ano}', index=False)

    # Salvando os outros arquivos
    rendimento.to_excel(path_evolucao_patrimonial, index=False)
    df_protheus.to_csv(path_lancamentos_protheus, header=None, index=False, sep=';')
    # df_protheus.to_excel(r'c:\Users\WevertonRodriguesBar\Desktop\investimentos\lancamentos_protheus.xlsx', index=False)

if __name__ == '__main__':
    main()
