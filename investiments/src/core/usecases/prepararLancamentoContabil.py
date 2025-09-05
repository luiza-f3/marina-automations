import pandas as pd
import os
from investiments.src.utils.tools import criar_lancamento_contabil

path_consulta_fundos = os.path.expanduser(os.getenv("CONSULTA_FUNDOS"))
df_fundos = pd.read_excel(path_consulta_fundos, sheet_name='para')
df_fundos['Cod Fundo'] = df_fundos['Cod Fundo'].astype(str).str.zfill(6)

def processarLancamentoContabil(df_rendimentos, demonstrativos):
    finalProtheus = []

    # --- Processa rendimentos ---
    for index, row in df_rendimentos.iterrows():
        plano = int(row['Plano'])
        perfil = int(row['Perfil'])
        fundo = row['Fundo']
        cod_fundo = row['Cod Fundo']
        rendimentos = round(row['Rendimento'], 2)

        try:
            conta_rentabilidade_positiva = df_fundos.loc[df_fundos['Cod Fundo'] == cod_fundo, 'Rentabilidade Positiva'].values[0]
            conta_rentabilidade_negativa = df_fundos.loc[df_fundos['Cod Fundo'] == cod_fundo, 'Rentabilidade Negativa'].values[0]
            conta_custo_atualizado = df_fundos.loc[df_fundos['Cod Fundo'] == cod_fundo, 'Custo Atualizado'].values[0]
        except IndexError:
            print(f"⚠️ Fundo não encontrado no df_fundos: {cod_fundo}")
            continue

        if rendimentos < 0:
            finalProtheus.append(criar_lancamento_contabil(conta_rentabilidade_negativa, abs(rendimentos), 'D', f'RENDIMENTO - {fundo}', plano, perfil))
            finalProtheus.append(criar_lancamento_contabil(conta_custo_atualizado, abs(rendimentos), 'C', f'RENDIMENTO - {fundo}', plano, perfil))
        elif rendimentos > 0:
            finalProtheus.append(criar_lancamento_contabil(conta_custo_atualizado, rendimentos, 'D', f'RENDIMENTO - {fundo}', plano, perfil))
            finalProtheus.append(criar_lancamento_contabil(conta_rentabilidade_positiva, rendimentos, 'C', f'RENDIMENTO - {fundo}', plano, perfil))

    # --- Processa demonstrativos ---
    df_fundos['Plano'] = df_fundos['Plano'].astype(int)
    df_fundos['Perfil'] = df_fundos['Perfil'].astype(int)

    if not demonstrativos.empty:
        for index, row in demonstrativos.iterrows():
            fundo = row['Historico']
            cod_fundo = str(row['Cod Fundo']).zfill(6)
            entrada = row['Entrada']
            saida = row['Saida']
            plano = int(row['Plano'])
            perfil = int(row['Perfil'])

            contaAplicFundo = None
            contaResgFundo = None

            try:
                contaContabil_carteira = df_fundos.loc[
                    (df_fundos['Plano'] == plano) & (df_fundos['Perfil'] == perfil)
                ]['Investimentos'].values[0]
            except IndexError:
                print(f"⚠️ Conta carteira não encontrada para Plano {plano}, Perfil {perfil}")
                contaContabil_carteira = None

            try:
                contaAplicFundo = df_fundos.loc[
                    (df_fundos['Plano'] == plano) & (df_fundos['Perfil'] == perfil) & (df_fundos['Cod Fundo'] == cod_fundo)
                ]['Aplicacao'].values[0]
            except IndexError:
                print(f"⚠️ Conta aplicação não encontrada para Plano {plano}, Perfil {perfil}, Fundo {cod_fundo}")

            try:
                contaResgFundo = df_fundos.loc[
                    (df_fundos['Plano'] == plano) & (df_fundos['Perfil'] == perfil) &
                    (df_fundos['Cod Fundo'].astype(str).str.zfill(6) == cod_fundo)
                ]['Resgate'].values[0]
            except IndexError:
                print(f"⚠️ Conta resgate não encontrada para Plano {plano}, Perfil {perfil}, Fundo {cod_fundo}")

            if entrada:
                entrada = round(entrada, 2)
                finalProtheus.append(criar_lancamento_contabil(contaContabil_carteira, abs(entrada), 'D', f'RESGATE - {fundo}', plano, perfil))
                finalProtheus.append(criar_lancamento_contabil(contaAplicFundo, abs(entrada), 'C', f'RESGATE - {fundo}', plano, perfil))

            if saida:
                saida = round(saida, 2)
                finalProtheus.append(criar_lancamento_contabil(contaResgFundo, abs(saida), 'D', f'APLICACAO - {fundo}', plano, perfil))
                finalProtheus.append(criar_lancamento_contabil(contaContabil_carteira, abs(saida), 'C', f'APLICACAO - {fundo}', plano, perfil))

    df_final = pd.DataFrame(finalProtheus)

    # --- Garante colunas no Excel ---
    colunas_fixas = ['Conta', 'Valor', 'Tipo', 'Historico', 'Plano', 'Perfil']
    for col in colunas_fixas:
        if col not in df_final.columns:
            df_final[col] = None

            # Remove colunas indesejadas
            colunas_para_remover = ['Conta', 'Tipo', 'Historico']
            df_final = df_final.drop(columns=colunas_para_remover, errors='ignore')

    return df_final
