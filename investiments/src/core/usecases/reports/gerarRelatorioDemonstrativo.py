import pandas as pd
import os
from datetime import datetime

def gerarRelatorioDemonstrativo(df, date):
    """
    Gera relatório de demonstrativos de caixa formatado
    Retorna:
        - DataFrame com relatório formatado em caso de sucesso
        - False em caso de falha
    """
    try:
        print("\n=== INÍCIO DA GERAÇÃO DO RELATÓRIO ===")

        # 1. Verificação inicial do DataFrame
        if not isinstance(df, pd.DataFrame):
            print("❌ Erro: O objeto recebido não é um DataFrame")
            return False

        if df.empty:
            print("❌ Erro: DataFrame vazio recebido")
            return False

        print(f"✅ DataFrame válido recebido com {len(df)} registros")
        print("Colunas disponíveis:", df.columns.tolist())

        # 2. Verificação de colunas obrigatórias
        colunas_necessarias = ['Historico','Cod Fundo', 'Entrada', 'Saida', 'Plano', 'Perfil']
        colunas_faltantes = [col for col in colunas_necessarias if col not in df.columns]

        if colunas_faltantes:
            print(f"❌ Colunas obrigatórias faltantes: {colunas_faltantes}")
            return False

        # 3. Processamento do relatório
        try:
            relatorio = df.copy()

            # 3.1 Adicionar data formatada
            try:
                relatorio['Data'] = pd.to_datetime(date, dayfirst=True).strftime('%Y-%m-%d')
            except:
                relatorio['Data'] = date

            # 3.2 e 3.3 Consolidar valores mantendo entradas e saídas separadas
            relatorio['Entrada'] = relatorio['Entrada'].apply(lambda x: x if x > 0 else 0)
            relatorio['Saida'] = relatorio['Saida'].apply(lambda x: -x if x < 0 else 0)

            # 3.4 Selecionar colunas finais
            colunas_finais = ['Data', 'Plano', 'Perfil', 'Historico', 'Cod Fundo' , 'Entrada', 'Saida']
            relatorio = relatorio[colunas_finais].rename(columns={'Historico': 'Histórico', 'Cod Fundo': 'Código do Fundo'})

            print("\n✅ Relatório formatado com sucesso")
            print("Amostra do relatório final:")
            print(relatorio.head())

            return relatorio

        except Exception as e:
            print(f"❌ Erro durante a formatação: {str(e)}")
            return False

    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        return False


def salvarRelatorioConsolidado(relatorio, output_path):
    """Salva o relatório em arquivo CSV auto-incrementado"""
    try:
        # 1. Criar diretório se não existir
        os.makedirs(output_path, exist_ok=True)

        # 2. Definir caminho completo do arquivo
        caminho_arquivo = os.path.join(output_path, "RELATORIO_DEMONSTRATIVOS.csv")

        # 3. Verificar se arquivo existe para auto-incremento
        if os.path.exists(caminho_arquivo):
            try:
                # Tentar ler o arquivo existente
                existente = pd.read_csv(caminho_arquivo, sep=';')

                # Concatenar com novos dados, removendo possíveis duplicatas
                relatorio_completo = pd.concat([existente, relatorio]).drop_duplicates()

                # Verificar se houve alteração
                if len(relatorio_completo) == len(existente):
                    print("⚠️ Nenhum novo registro para adicionar")
                else:
                    print(f"📊 Registros existentes: {len(existente)} | Novos registros: {len(relatorio)}")
            except Exception as e:
                print(f"⚠️ Erro ao ler arquivo existente, criando novo: {str(e)}")
                relatorio_completo = relatorio
        else:
            relatorio_completo = relatorio

        # 4. Salvar arquivo com tratamento de permissão
        try:
            relatorio_completo.to_csv(
                caminho_arquivo,
                sep=';',
                index=False,
                encoding='utf-8-sig'
            )
            print(f"✅ Relatório salvo em: {caminho_arquivo}")
            print(f"📌 Total de registros: {len(relatorio_completo)}")
            return True
        except PermissionError:
            print("❌ Erro de permissão. Soluções possíveis:")
            print("1. Feche o arquivo se estiver aberto em outro programa")
            print("2. Execute o script como administrador")
            print(f"3. Verifique as permissões da pasta: {output_path}")
            return False

    except Exception as e:
        print(f"❌ Erro ao salvar relatório: {str(e)}")
        return False


def processarDemonstrativos(cash_flow, dt_referencia, base_path):
    """
    Função principal que orquestra todo o processamento
    """
    print("\n" + "=" * 50)
    print(" PROCESSAMENTO DE DEMONSTRATIVOS ".center(50, '='))
    print("=" * 50 + "\n")

    # 1. Gerar relatório formatado
    relatorio = gerarRelatorioDemonstrativo(cash_flow, dt_referencia)

    if not isinstance(relatorio, pd.DataFrame) or relatorio.empty:
        print("⛔ Processamento interrompido - relatório vazio")
        return False

    # 2. Salvar relatório
    output_dir = os.path.join(base_path, 'relatorios')
    if not salvarRelatorioConsolidado(relatorio, output_dir):
        print("⛔ Falha ao salvar relatório")
        return False

    print("\n" + "=" * 50)
    print(" PROCESSAMENTO CONCLUÍDO ".center(50, '='))
    print("=" * 50 + "\n")

    return True