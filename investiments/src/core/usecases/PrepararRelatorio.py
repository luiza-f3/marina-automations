import sys

"""
# Definição da data manual
data = "2025-02-26"
ano, mes, dia = data.split('-')
file_name = 'Relatorio_validador.xlsx'

caminho_base = os.path.expanduser("~/Documents/investimentos/")
caminho_saida = os.path.expanduser("~/Documents/relatorios_finais/")

# Lista dos arquivos esperados com seus respectivos leitores
arquivos_entrada = {
    f"{caminho_base}evolucao_patrimonial26-02.xlsx": pd.read_excel,
    f"{caminho_base}lancamentos_protheus26-02.csv": pd.read_csv,
}

# Verifica quais arquivos existem e carrega com o leitor apropriado
faltando = []
dfs = []

for caminho, leitor in arquivos_entrada.items():
    if os.path.exists(caminho):
        try:
            dfs.append(leitor(caminho))
        except Exception as e:
            print(f"Erro ao ler o arquivo {os.path.basename(caminho)}: {e}")
            faltando.append(os.path.basename(caminho))
    else:
        faltando.append(os.path.basename(caminho))

# Se faltar algum, exibe mensagem e finaliza
if faltando:
    print("Os seguintes arquivos não foram encontrados ou tiveram erro de leitura:")
    for arq in faltando:
        print(f" - {arq}")
    print(f"Total de arquivos com problemas: {len(faltando)}")
    exit()

# Continua processamento se todos arquivos estiverem OK
df1, df2 = dfs

try:
    df = pd.merge(df1, df2, on=['Plano', 'Perfil', 'Classificacao'], suffixes=('_1', '_2'))
except KeyError:
    print("Os arquivos precisam conter as colunas: 'Plano', 'Perfil', 'Classificacao'")
    exit()

"""

import pandas as pd
import os
import re
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment

# ==================== Configurações Base ====================
PASTA_ORIGEM = os.path.expanduser("~/Documents/investimentos/")
PASTA_DESTINO = os.path.expanduser("~/Documents/relatorios_finais/")

# ========= Extração de datas e decisão do relatório a ser utilizado =============

def extrair_data_do_nome(nome_arquivo):
    """Extrai dia e mês do nome do arquivo no formato relatorioDD-MM.xlsx"""
    match = re.search(r"evolucao_patrimonial(\d{2})-(\d{2})\.xlsx", nome_arquivo) #Visualizando todos os arquivos que possuem esse padrão no nome.
    if match:
        dia, mes = map(int, match.groups()) #Caso encontre o arquivo ele junta o mês e o dia para adicionar como data final
        return dia, mes
    return None, None

# ============================================================

def processar_arquivos():
    """Processa todos os arquivos e gera o novo relatório"""
    dados_consolidados = []

    for nome_arquivo in os.listdir(PASTA_ORIGEM):
        if not nome_arquivo.endswith('.xlsx'):
            continue

        dia, mes = extrair_data_do_nome(nome_arquivo)
        if not dia or not mes:
            continue

        try:
            # 1. Extrai a data do nome do arquivo
            data_completa = datetime(2025, mes, dia).strftime("%d/%m/%Y")

            # 2. Carrega o arquivo Excel
            caminho_arquivo = os.path.join(PASTA_ORIGEM, nome_arquivo)
            df = pd.read_excel(caminho_arquivo)

            # 3. Seleciona apenas as colunas necessárias
            colunas_necessarias = [
                'Plano',
                'Perfil',
                'Classificacao',
                'Saldo Anterior',
                'Entrada',
                'Saida',
                'Saldo Atual',
                'Rendimento'
            ]

            # Verifica se as colunas existem
            for col in colunas_necessarias:
                if col not in df.columns:
                    raise KeyError(f"Coluna '{col}' não encontrada")

            df = df[colunas_necessarias]

            # 4. Adiciona colunas calculadas e informações adicionais
            df['Data'] = data_completa
            df['Dia'] = dia
            df['Mes'] = mes
            df['Arquivo_Origem'] = nome_arquivo

            # 5. Calcula diferença entre saldo atual e anterior (para conferência)
            df['Variacao_Calculada'] = df['Saldo Atual'] - df['Saldo Anterior']
            df['Rendimento_Calculado'] = df['Saldo Atual'] - df['Saldo Anterior'] - df['Entrada'] + df['Saida']

            dados_consolidados.append(df)
            print(f"✅ Processado: {nome_arquivo}")

        except Exception as e:
            print(f"❌ Erro no arquivo {nome_arquivo}: {str(e)}")
            continue

    if not dados_consolidados:
        print("\n⚠️ Nenhum arquivo válido encontrado!")
        return False

    # 6. Consolida todos os dados
    df_final = pd.concat(dados_consolidados, ignore_index=True)

    # 7. Ordena as colunas
    colunas_ordenadas = [
        'Data', 'Dia', 'Mes', 'Plano', 'Perfil', 'Classificacao',
        'Saldo Anterior', 'Entrada', 'Saida', 'Saldo Atual', 'Rendimento',
        'Variacao_Calculada', 'Rendimento_Calculado', 'Arquivo_Origem'
    ]
    df_final = df_final[colunas_ordenadas]

    # 8. Salva o relatório final
    os.makedirs(PASTA_DESTINO, exist_ok=True)
    caminho_final = os.path.join(PASTA_DESTINO, "RELATORIO_APOIO.xlsx")

    with pd.ExcelWriter(caminho_final, engine='openpyxl') as writer:
        # Aba principal com todos os dados
        df_final.to_excel(writer, sheet_name='Dados', index=False)

        # Aba de resumo por plano
        resumo = df_final.groupby(['Plano', 'Perfil']).agg({
            'Saldo Anterior': 'first',
            'Saldo Atual': 'last',
            'Entrada': 'sum',
            'Saida': 'sum',
            'Rendimento': 'sum'
        })
        resumo['Variacao'] = resumo['Saldo Atual'] - resumo['Saldo Anterior']
        resumo.to_excel(writer, sheet_name='Resumo por Plano')

        # Aba de resumo por data
        df_final.groupby('Data').agg({
            'Entrada': 'sum',
            'Saida': 'sum',
            'Rendimento': 'sum'
        }).to_excel(writer, sheet_name='Resumo por Data')

    # 9. Formatação profissional
    wb = load_workbook(caminho_final)
    for sheet in wb.sheetnames:
        ws = wb[sheet]

        # Formata cabeçalho
        for col in ws[1]:
            col.font = Font(bold=True, color="FFFFFF")
            col.fill = PatternFill(start_color="4F81BD", fill_type="solid")
            col.border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )

        # Ajusta largura das colunas
        for column in ws.columns:
            max_length = max(len(str(cell.value)) for cell in column)
            ws.column_dimensions[column[0].column_letter].width = max_length + 2

    wb.save(caminho_final)
    print(f"\n🎉 Relatório gerado com sucesso em: {caminho_final}")
    return True


# ========================== EXECUÇÃO =======================

def main():
    """Execução principal"""
    print("\n" + "=" * 60)
    print("📊 GERADOR DE RELATÓRIO DE INVESTIMENTOS")
    print("=" * 60)

    processar_arquivos()


if __name__ == "__main__":
    main()