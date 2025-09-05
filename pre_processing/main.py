from pre_processing.scripts.download import download
# Caminho pastas nuvem # C:\Users\LuizaMoreira\F3\Sistemas - Documentos\Marina BPO\Operacional\Ano Calendario 2025\POC - 022025\Investimentos\06_02
from scripts.extract import extract_reservas
from scripts.extract import extract_folha_beneficios
from pre_processing.scripts.extract import extract_folha_pagamento

from scripts.transform import transform_reservas
from scripts.transform import transform_folha_beneficios
from pre_processing.scripts.transform import transform_folha_pagamento

from pre_processing.config.settings import *
import os

def process_and_load():
    #download.download_autopatrocinado(TYPE_FILE_AUTOPATROCINADO)
    # download.download_reservas()
    download.download_folha_beneficios()
    #download.download_folha_pagamentos()
    
    raw_dirs = {
        #"autopatrocinado": os.path.join("data", "raw"),
        # "reservas": os.path.join("data", "raw"),
        "folha_beneficios": os.path.join(RAW_DIR),
        #"folha_pagamento": os.path.join(RAW_DIR),
    }
    processed_dirs = {
        #"autopatrocinado": os.path.join("data", "processed"),
        # "reservas": os.path.join("data", "processed"),
        "folha_beneficios": os.path.join(PROCESSED_DIR),
        #"folha_pagamento": os.path.join(PROCESSED_DIR),
    }
    extract_functions = {
        #"autopatrocinado": extract_autopatrocinado.extract_autopatrocinado,
        # "reservas": extract_reservas.extract_reservas,
        "folha_beneficios": extract_folha_beneficios.extract_folha_beneficios,
        #"folha_pagamento": extract_folha_pagamento.extract_folha_pagamento
    }
    transform_functions = {
        #"autopatrocinado": transform_autopatrocinado.transform_autopatrocinado,
        # "reservas": transform_reservas.transform_reservas,
        "folha_beneficios": transform_folha_beneficios.transform_folha_beneficios,
        #"folha_pagamento": transform_folha_pagamento.transform_folha_pagamento
    }

    for sheet, raw_dir in raw_dirs.items():
        files = os.listdir(raw_dir)
        #files = [os.path.join(raw_dir, f) for f in os.listdir(raw_dir) if f.endswith(".xls") or f.endswith(".xlsx")]

        for file in files:
            data = None
            # Verifica se o nome do arquivo corresponde à aba
            if os.path.splitext(os.path.basename(file))[0] == sheet:
                data = extract_functions[sheet](os.path.join(raw_dir, file))
                data = transform_functions[sheet](data)

                output_dir = processed_dirs[sheet]
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                data.to_csv(os.path.join(output_dir, f'{sheet}_processado.csv'), index=False)
            else:
                continue
            # if sheet == "autopatrocinado" and data is not None:
            #     load_data.load_autopatrocinado(data)
            #     break
            # if sheet == "reservas" and data is not None:
            #     load_data.load_reservas(data)
            #     break
            # if sheet == "folha_beneficios" and data is not None:
            #    load_data.load_folha_beneficios(data)
            #    break
            # if sheet == "folha_pagamento" and data is not None:
            #    load_data.load_folha_pagamento(data)
            #    break

        #combined_data = pd.concat(data_frame)
        #combined_data.to_csv(os.path.join(processed_dirs[sheet], f'{sheet}_processado.csv'), sep=";", index=False)
        #all_data[sheet] = combined_data

        #load_data.load_autopatrocinado(data)
        #load_data.load_reservas(data)

if __name__ == "__main__":
    process_and_load()
