import pandas as pd
import os

def generate_statement_report(df, reference_date):
    """
    Gera um relatório de demonstrativos de caixa formatado.

    Args:
        df (DataFrame): DataFrame de entrada
        reference_date (str): Data de referência do relatório

    Returns:
        DataFrame: Relatório formatado ou DataFrame vazio em caso de falha
    """

    if not isinstance(df, pd.DataFrame):
        print("❌ Erro: o objeto recebido não é um DataFrame.")
        return pd.DataFrame()

    if df.empty:
        print("❌ Erro: DataFrame vazio recebido.")
        return pd.DataFrame()

    required_columns = ['Historico', 'Cod Fundo', 'Entrada', 'Saida', 'Plano', 'Perfil']
    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        print(f"❌ Colunas obrigatórias faltantes: {missing_columns}")
        return pd.DataFrame()

    report = df.copy()

    try:
        formatted_date = pd.to_datetime(reference_date, dayfirst=True).strftime('%Y-%m-%d')
    except (ValueError, TypeError):
        formatted_date = reference_date

    report['Data'] = formatted_date

    report['Entrada'] = pd.to_numeric(report['Entrada'], errors='coerce').fillna(0)
    report['Saida'] = pd.to_numeric(report['Saida'], errors='coerce').fillna(0)

    report['Entrada'] = report['Entrada'].apply(lambda value: value if value > 0 else 0)
    report['Saida'] = report['Saida'].apply(lambda value: -value if value < 0 else 0)

    final_columns = ['Data', 'Plano', 'Perfil', 'Historico', 'Cod Fundo', 'Entrada', 'Saida']
    report = report[final_columns].rename(
        columns={
            'Historico': 'Histórico',
            'Cod Fundo': 'Código do Fundo'
        }
    )

    return report


def save_consolidated_report(report, output_path):
    """
    Salva o relatório consolidado em CSV.

    Args:
        report (DataFrame): Relatório a ser salvo
        output_path (str): Caminho da pasta de saída

    Returns:
        bool: True em caso de sucesso, False em caso de falha
    """

    if not isinstance(report, pd.DataFrame) or report.empty:
        print("❌ Erro: relatório inválido ou vazio.")
        return False

    if not output_path:
        print("❌ Erro: o caminho de saída não pode ser vazio.")
        return False

    try:
        os.makedirs(output_path, exist_ok=True)
        file_path = os.path.join(output_path, "RELATORIO_DEMONSTRATIVOS.csv")

        if os.path.exists(file_path):
            try:
                existing_report = pd.read_csv(file_path, sep=';')
                full_report = pd.concat([existing_report, report], ignore_index=True).drop_duplicates()

                if len(full_report) == len(existing_report):
                    print("[INFO] Nenhum novo registro para adicionar.")
                else:
                    print(
                        f"[INFO] Registros existentes: {len(existing_report)} | "
                        f"Novos registros: {len(report)}"
                    )

            except Exception as error:
                print(f"[AVISO] Erro ao ler arquivo existente. Um novo arquivo sera salvo: {error}")
                full_report = report.copy()
        else:
            full_report = report.copy()

        full_report.to_csv(
            file_path,
            sep=';',
            index=False,
            encoding='utf-8-sig'
        )

        print(f"[OK] Relatorio salvo em: {file_path}")
        print(f"[INFO] Total de registros: {len(full_report)}")
        return True

    except PermissionError:
        print("[ERRO] Erro de permissao ao salvar o relatorio.")
        print("1. Feche o arquivo se ele estiver aberto.")
        print("2. Verifique as permissoes da pasta.")
        print("3. Tente executar o script com permissoes adequadas.")
        return False

    except OSError as error:
        print(f"[ERRO] Erro ao salvar relatorio: {error}")
        return False


def process_statements(cash_flow, reference_date, base_path):
    """
    Orquestra o processamento dos demonstrativos.

    Args:
        cash_flow (DataFrame): Dados de fluxo de caixa
        reference_date (str): Data de referência
        base_path (str): Caminho base de saída

    Returns:
        bool: True em caso de sucesso, False em caso de falha
    """

    print("\n" + "=" * 50)
    print(" PROCESSAMENTO DE DEMONSTRATIVOS ".center(50, '='))
    print("=" * 50 + "\n")

    report = generate_statement_report(cash_flow, reference_date)

    if report.empty:
        print("[AVISO] Processamento interrompido: relatorio vazio.")
        return False

    output_dir = os.path.join(base_path, 'reports')

    if not save_consolidated_report(report, output_dir):
        print("[AVISO] Falha ao salvar relatorio.")
        return False

    print("\n" + "=" * 50)
    print(" PROCESSAMENTO CONCLUIDO ".center(50, '='))
    print("=" * 50 + "\n")

    return True