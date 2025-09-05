import os
import pandas as pd
from dotenv import load_dotenv
from src.ContabilizarPayroll import ContabilizarPayroll

load_dotenv()

base_path = os.getenv("BASE_PATH")
payroll_file = os.getenv("PAYROLL")
data = os.getenv("DATA")
path_payroll = os.path.join(base_path, payroll_file)

if __name__ == "__main__":
    payroll = pd.read_csv(path_payroll)

    payroll.drop(columns=['DataApropriacao', 'DataVencimento'], inplace=True)

    payroll_contabilizado = ContabilizarPayroll(payroll).contabilizar()
    print(payroll_contabilizado)
