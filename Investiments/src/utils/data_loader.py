from investiments.src.utils.mappings.cash_flow_info import cash_flow_info
import pandas as pd
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
        """Lista e filtra todos os arquivos de um diretório com base em substrings fornecidas."""
        try:
            files = [f for f in os.listdir(directory)
                        if os.path.isfile(os.path.join(directory, f)) and f.endswith(('.xls', '.csv', '.xlsx'))]

            filtered_files = [f for f in files if any(substring in f for substring in substrings)]
            print(f"{len(filtered_files)} arquivos filtrados no diretório {directory}: {filtered_files}")
            return filtered_files
        except Exception as e:
            print(f"Erro ao listar arquivos do diretório: {e}")
            return None

    @staticmethod
    def load_file_directory(directory, substrings):
        """Lista e carrega todos os arquivos do diretório que correspondem às substrings fornecidas usando
        DataLoader."""
        print(f"[DEBUG] Tentando acessar diretório: {directory}")
        print(f"[DEBUG] Verificando se diretório existe: {os.path.exists(directory)}")
        
        files = DataLoader.list_files(directory, substrings)
        if files is not None:
            funds_data = {}
            for file in files:
                key_name = [substring for substring in substrings if substring in file]
                file_path = os.path.join(directory, file)
                print(f"Carregando arquivo: {file_path}")
                funds_data[key_name[0]] = DataLoader.load_data(file_path)
            return funds_data
        else:
            return None
