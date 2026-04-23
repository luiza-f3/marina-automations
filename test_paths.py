#!/usr/bin/env python
"""Script de teste para verificar os caminhos configurados."""

from dotenv import load_dotenv
import os

load_dotenv()

base_path = os.path.expanduser(os.getenv("BASE_PATH"))
print(f"BASE_PATH: {base_path}")
print(f"BASE_PATH existe: {os.path.exists(base_path)}")
print()

# Teste de pastas esperadas
expected_dirs = ['Carteiras', 'Consultas', 'Demonstrativos', 'Investimentos', 'Rendimentos']
for dir_name in expected_dirs:
    full_path = os.path.join(base_path, dir_name)
    exists = os.path.exists(full_path)
    print(f"  {dir_name:<20} - {full_path:<80} - {'✓' if exists else '✗'}")

print()

# Teste de arquivo de consulta
consulta_fundos = os.getenv('CONSULTA_FUNDOS')
full_consulta_path = os.path.normpath(os.path.join(base_path, consulta_fundos))
exists = os.path.exists(full_consulta_path)
print(f"Arquivo de Consulta: {full_consulta_path}")
print(f"Existe: {'✓' if exists else '✗'}")
print()

# Teste de pasta Carteiras com data
current_date = os.getenv('CURRENT_DATE')
year, mon, day = current_date.split('-')
carteira_path = os.path.normpath(os.path.join(base_path, 'Carteiras', f'{day}_{mon}'))
exists = os.path.exists(carteira_path)
print(f"Carteira do dia: {carteira_path}")
print(f"Existe: {'✓' if exists else '✗'}")
if exists:
    files = os.listdir(carteira_path)
    print(f"Arquivos: {files}")

