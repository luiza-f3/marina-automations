import shutil
from pre_processing.config.settings import *

def download_autopatrocinado(type_file):
    #path = os.path.normpath(os.path.expanduser(PATH_AUTOPATROCINADO))
    if not PATH_AUTOPATROCINADO or not os.path.exists(PATH_AUTOPATROCINADO):
        raise FileNotFoundError(f"File not found: {PATH_AUTOPATROCINADO}")
    file_name = f"autopatrocinado.{type_file}"
    copy_file(PATH_AUTOPATROCINADO, file_name)

def download_reservas():
    if not PATH_RESERVAS or not os.path.exists(PATH_RESERVAS):
        raise FileNotFoundError(f"File not found: {PATH_RESERVAS}")
    file_name = "reservas.xlsx"
    copy_file(PATH_RESERVAS, file_name)

def download_folha_beneficios():
    if not PATH_FOLHA_BENEFICIOS or not os.path.exists(PATH_FOLHA_BENEFICIOS):
        raise FileNotFoundError(f"File not found: {PATH_FOLHA_BENEFICIOS}")
    file_name = "folha_beneficios.xls"
    copy_file(PATH_FOLHA_BENEFICIOS, file_name)

def download_arrecadacao():
    if not PATH_ARRECADACAO or not os.path.exists(PATH_ARRECADACAO):
        raise FileNotFoundError(f"File not found: {PATH_ARRECADACAO}")
    file_name = "arrecadacao.xlsx"
    copy_file(PATH_ARRECADACAO, file_name)

def download_folha_pagamentos():
    if not PATH_RESERVAS or not os.path.exists(PATH_RESERVAS):
        raise FileNotFoundError(f"File not found: {PATH_RESERVAS}")
    file_name = "folha_pagamento.xlsx"
    copy_file(PATH_RESERVAS, file_name)

def copy_file(source_path, file_name):
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)
        print(f"Directory created: {BASE_PATH}")
    
    destination_path = os.path.join(BASE_PATH, 'data', 'raw', file_name)
    
    try:
        shutil.copy(source_path, destination_path)
        print(f"File copied to: {destination_path}")
    except Exception as e:
        print(f"Error copying file: {e}")
