from dotenv import load_dotenv
import os

load_dotenv()
base_path = os.path.expanduser(os.getenv("BASE_PATH"))
year, mon, day = os.getenv('DATA_ATUAL').split('-')
dt_cash_flow = f'{day}/{mon}/{year}'