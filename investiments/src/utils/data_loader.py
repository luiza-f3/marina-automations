import pandas as pd
from investiments.src.utils.consultas.cash_flow_info import cash_flow_info
import os

class DataLoader:
    substrings = [item[0] for item in cash_flow_info]
    @staticmethod
    def load_data(file):
        """Carrega dados de um arquivo CSV ou XLSX com base na extensão do arquivo."""
        try:
            if file.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.endswith('.xlsx'):
                df = pd.read_excel(file)
            elif file.endswith('.xls'):
                df = pd.read_excel(file)
            else:
                raise ValueError("Tipo de arquivo não suportado. Utilize um arquivo CSV ou XLSX.")
            print(f"Dados carregados com sucesso do arquivo: {file}")
            return df
        except Exception as e:
            print(f"Erro ao carregar o arquivo: {e}")
            return None

    @staticmethod
    def list_files(directory, substrings):
        """Lista e filtra todos os arquivos em um diretório com base em substrings fornecidas."""
        try:
            arquivos = [f for f in os.listdir(directory)
                        if os.path.isfile(os.path.join(directory, f)) and f.endswith(('.xls', '.csv', '.xlsx'))]

            arquivos_filtrados = [f for f in arquivos if any(substring in f for substring in substrings)]
            print(f"{len(arquivos_filtrados)} arquivos filtrados no diretório {directory}: {arquivos_filtrados}")
            return arquivos_filtrados
        except Exception as e:
            print(f"Erro ao listar arquivos do diretório: {e}")
            return None

    @staticmethod
    def load_file_directory(directory, substrings):
        """Lista e carrega todos os arquivos do diretório que correspondem às substrings fornecidas usando
        DataLoader."""
        arquivos = DataLoader.list_files(directory, substrings)
        if arquivos is not None:
            dados = {}
            for arquivo in arquivos:
                key_name = [substring for substring in substrings if substring in arquivo]
                caminho_arquivo = os.path.join(directory, arquivo)
                print(f"Carregando arquivo: {caminho_arquivo}")
                dados[key_name[0]] = DataLoader.load_data(caminho_arquivo)
            return dados
        else:
            return None
