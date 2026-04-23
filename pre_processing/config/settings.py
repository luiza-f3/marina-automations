from dotenv import load_dotenv
import os

load_dotenv()

BASE_PATH = os.path.expanduser(os.path.join('~', 'Documents'))
RAW_DIR = os.path.join(BASE_PATH, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_PATH, "data", "processed")

DATABASE_URI = os.getenv("DATABASE_URI")
DB_NAME = os.getenv("DB_NAME")

PATH_AUTOPATROCINADO = os.path.normpath(os.path.expanduser(os.getenv("PATH_AUTOPATROCINADO")))
AUTOPATROCINADO_COLL = os.getenv("AUTOPATROCINADO_COLL")
TYPE_FILE_AUTOPATROCINADO = os.getenv("TYPE_FILE_AUTOPATROCINADO")

PATH_RESERVAS_FILE = os.getenv("PATH_RESERVAS_FILE")
PATH_RESERVAS = os.path.join(BASE_PATH, 'Folha de pagamentos', PATH_RESERVAS_FILE)
RESERVAS_COLL = os.getenv("RESERVAS_COLL")

FOLHA_BENEFICIOS_FILE = os.getenv("FOLHA_BENEFICIOS_FILE")
PATH_FOLHA_BENEFICIOS = os.path.join(BASE_PATH, 'Beneficios', FOLHA_BENEFICIOS_FILE)

FOLHA_BENEFICIOS_COLL = os.getenv("FOLHA_BENEFICIOS_COLL")

PATH_ARRECADACAO=os.getenv("PATH_ARRECADACAO")
ARRECADACAO_COLL=os.getenv("ARRECADACAO_COLL")

RAW_DIR_PAGAMENTOS = os.path.join(BASE_PATH, "data", "raw")
PROCESSED_DIR_PAGAMENTOS = os.path.join(BASE_PATH, "data", "processed")

