# 🌳 ÁRVORE DE DEPENDÊNCIAS E CHAMADAS DE FUNÇÕES

## INÍCIO: main.py → main()

```
main.py
│
└─ main()
   │
   ├─ load_dotenv() ...................... Carrega .env
   │
   ├─ os.getenv() ....................... Obtém variáveis
   │
   ├─ print("Starting investment processing...")
   │
   │
   ├─── ETAPA 1-2: PROVISÕES (Data Atual + Anterior)
   │
   ├─ prepare_provisions(
   │  │  'BASE_PATH/Carteiras/{day}_{mon}/'
   │  │)
   │  │
   │  └─ data_transforms.py → prepare_provisions()
   │     │
   │     ├─ utils.py → load_file_directory()
   │     │  │
   │     │  ├─ list_files()
   │     │  ├─ load_data()  (Para cada arquivo)
   │     │  │
   │     │  └─ retorna: dados = {
   │     │                '010134': DataFrame,
   │     │                '011607': DataFrame,
   │     │                ...
   │     │              }
   │     │
   │     ├─ Define Plano/Perfil
   │     │  └─ utils.py → define_profile_plan()
   │     │
   │     ├─ Extrai RESGATE/APLICACAO
   │     ├─ Normaliza texto
   │     │  └─ utils.py → normalize_text()
   │     │
   │     ├─ utils.py → executeFromTo()
   │     │  └─ Aplica rename_datas (depara)
   │     │
   │     └─ retorna:
   │        ├─ redemptions_applications_provisions
   │        └─ provisions
   │
   ├─ redemptions_applications_provisions_pre, _ = prepare_provisions(
   │       'BASE_PATH/Carteiras/{day_pre}_{mon_pre}/'
   │  )
   │
   │
   ├─── ETAPA 3-4: CARTEIRAS (Data Atual + Anterior)
   │
   ├─ current_wallet = prepare_wallets(
   │       'BASE_PATH/Carteiras/{day}_{mon}/'
   │  )
   │  │
   │  └─ data_transforms.py → prepare_wallets()
   │     │
   │     ├─ utils.py → load_file_directory()
   │     │  └─ Carrega colunas [A, B, H]
   │     │
   │     ├─ Remove linha "Total"
   │     ├─ utils.py → define_profile_plan()
   │     ├─ utils.py → executeFromTo()
   │     ├─ utils.py → mapear_classificacoes()
   │     │  └─ Busca em df_fundos
   │     │
   │     └─ retorna: current_wallet (DataFrame)
   │
   ├─ previous_wallet = prepare_wallets(
   │       'BASE_PATH/Carteiras/{day_pre}_{mon_pre}/'
   │  )
   │
   │
   ├─── ETAPA 5: MAPEAR FUNDOS
   │
   ├─ previous_wallet = mapear_fundo(
   │       current_wallet,
   │       previous_wallet
   │  )
   │  │
   │  └─ utils.py → mapear_fundo()
   │     └─ Cria mapeamento de nomes
   │
   │
   ├─── ETAPA 6: GERAR RELATÓRIO
   │
   ├─ gerarRelatorio(
   │       redemptions_applications_provisions,
   │       current_wallet
   │  )
   │  │
   │  └─ gerarRelatorio.py → gerarRelatorio()
   │     └─ Cria arquivo de relatório
   │
   │
   ├─── ETAPA 7-8: MESCLAR CARTEIRAS
   │
   ├─ current_wallet = pd.merge(
   │       current_wallet,
   │       redemptions_applications_provisions,
   │       left_on=['Fundo', 'Plano', 'Perfil'],
   │       right_on=['Despesa', 'Plano', 'Perfil'],
   │       how='left'
   │  )
   │  └─ Soma valores
   │
   ├─ previous_wallet = pd.merge(
   │       previous_wallet,
   │       redemptions_applications_provisions_pre,
   │       left_on=['Fundo', 'Plano', 'Perfil'],
   │       right_on=['Despesa', 'Plano', 'Perfil'],
   │       how='left'
   │  )
   │
   │
   ├─── ETAPA 9: PREPARAR FLUXO DE CAIXA
   │
   ├─ cash_flow = prepare_cash_flow(
   │       'BASE_PATH/demonstrativos/',
   │       dt_cash_flow
   │  )
   │  │
   │  └─ data_transforms.py → prepare_cash_flow()
   │     │
   │     ├─ utils.py → load_file_directory()
   │     │
   │     ├─ utils.py → filtrar_data_demonstrativo()
   │     │  ├─ utils.py → extrair_cod_fundo()
   │     │  ├─ utils.py → extrair_valor()
   │     │  └─ Filtra por data
   │     │
   │     ├─ utils.py → define_profile_plan()
   │     ├─ utils.py → normalize_text()
   │     ├─ utils.py → executeFromTo()
   │     │
   │     └─ retorna: cash_flow (DataFrame)
   │
   │
   ├─── ETAPA 10: PROCESSAR DEMONSTRATIVOS
   │
   ├─ resultado = processarDemonstrativos(
   │       cash_flow=cash_flow,
   │       dt_referencia=dt_cash_flow,
   │       base_path=base_path
   │  )
   │  │
   │  └─ gerarRelatorioDemonstrativo.py → processarDemonstrativos()
   │     └─ Valida e processa
   │
   ├─ if not resultado:
   │     print("❌ Errors occurred...")
   │     return (encerra)
   │
   │
   ├─── ETAPA 11-12: TOTALIZAR E DIFERENCIAR
   │
   ├─ cash_flow = totalize_entries_exits(cash_flow)
   │  │
   │  └─ data_transforms.py → totalize_entries_exits()
   │     ├─ Agrupa por chave composta
   │     ├─ Verifica se é taxa (em fees_info)
   │     └─ Soma Entrada/Saida
   │
   ├─ cash_flow_balance = generate_entries_exits_difference(cash_flow)
   │  │
   │  └─ data_transforms.py → generate_entries_exits_difference()
   │     ├─ Calcula diferença
   │     ├─ Se diff < 0: Saida = diff, Entrada = 0
   │     └─ Se diff ≥ 0: Entrada = diff, Saida = 0
   │
   │
   ├─── ETAPA 13: FILTRAR REGISTROS
   │
   ├─ (acquisition_redemption,
   │  cash_flow_filtered,
   │  expenses) = filter_records(cash_flow)
   │  │
   │  └─ data_transforms.py → filter_records()
   │     ├─ Identifica taxas (fees_info)
   │     ├─ Identifica RESGATE/AQUISICAO
   │     └─ retorna: 3 DataFrames
   │
   │
   ├─── ETAPA 14: EVOLUÇÃO PATRIMONIAL
   │
   ├─ asset_evolution = prepare_asset_evolution(
   │       current_wallet,
   │       previous_wallet,
   │       cash_flow_balance
   │  )
   │  │
   │  └─ data_transforms.py → prepare_asset_evolution()
   │     ├─ Busca saldo anterior
   │     ├─ Busca fluxo do dia
   │     ├─ Calcula rendimento
   │     └─ retorna: asset_evolution (DataFrame)
   │
   │
   ├─── ETAPA 15-17: CONTABILIZAÇÕES (PARALELO)
   │
   ├─┬─ income_accounting = process_income_accounting(
   │ │       asset_evolution,
   │ │       cash_flow_filtered
   │ │  )
   │ │  │
   │ │  └─ accounting.py → process_income_accounting()
   │ │     ├─ Processa rendimentos
   │ │     ├─ Busca contas em df_fundos
   │ │     ├─ Cria lançamentos D/C
   │ │     └─ retorna: income_accounting
   │ │
   │ ├─ cash_flow_tax_accounting = process_tax_accounting(expenses)
   │ │  │
   │ │  └─ accounting.py → process_tax_accounting()
   │ │     ├─ Processa taxas/despesas
   │ │     ├─ Busca contas em fees_accounts
   │ │     ├─ Diferencia por plano/perfil
   │ │     ├─ Casos especiais (ESTORNO, IOF, etc)
   │ │     └─ retorna: cash_flow_tax_accounting
   │ │
   │ └─ if execute_provision == 'True':
   │      provisions_accounting = process_provision_accounting(provisions)
   │      │
   │      └─ accounting.py → process_provision_accounting()
   │         ├─ Processa provisões
   │         ├─ Busca em fees_accounts
   │         ├─ Diferencia planos (PGA vs Plano)
   │         └─ retorna: provisions_accounting
   │    else:
   │      provisions_accounting = pd.DataFrame()
   │
   │
   ├─── ETAPA 18: SALVAR DADOS
   │
   ├─ save_data(
   │       asset_evolution,
   │       income_accounting,
   │       cash_flow_tax_accounting,
   │       provisions_accounting,
   │       base_path,
   │       day,
   │       mon
   │  )
   │  │
   │  └─ utils.py → save_data()
   │     │
   │     ├─ Filtra dados específicos
   │     │  ├─ procurar_palavra(income_accounting, ..., 'APLICACAO')
   │     │  │  └─ utils.py → procurar_palavra()
   │     │  │     └─ filters.py → search_word()
   │     │  │
   │     │  ├─ procurar_palavra(income_accounting, ..., 'RESGATE')
   │     │  │
   │     │  └─ filtrar_dados(income_accounting, 'RENDIMENTO')
   │     │     └─ filters.py → filter_data()
   │     │
   │     ├─ Cria diretório
   │     │  └─ os.makedirs(investiments_path)
   │     │
   │     ├─ Salva Excel 1 (Evolução Patrimonial)
   │     │  └─ asset_evolution.to_excel(...)
   │     │
   │     ├─ Concatena lançamentos
   │     │  └─ pd.concat([income, tax, provisions])
   │     │
   │     ├─ Salva CSV (Protheus)
   │     │  └─ df_protheus.to_csv(..., sep=';')
   │     │
   │     └─ Salva Excel 2 (Segregado)
   │        └─ pd.ExcelWriter() com 5 sheets:
   │           ├─ Provisoes
   │           ├─ Despesas
   │           ├─ Rentabilidade
   │           ├─ Aplicacao
   │           └─ Resgate
   │
   │
   ├─── ETAPA 19: CONCLUSÃO
   │
   ├─ print("✅ Investment processing completed successfully!")
   │
   └─ except Exception as e:
      ├─ print(f"❌ Error in main processing: {e}")
      └─ raise

if __name__ == "__main__":
    main()
```

---

## 📦 ESTRUTURA DE IMPORTS

```
main.py (arquivo principal)
│
├─ os, load_dotenv (configurações)
│
├─ pandas (manipulação de dados)
│
├─ data_transforms.py
│  ├─ prepare_wallets()
│  ├─ prepare_provisions()
│  ├─ prepare_cash_flow()
│  ├─ totalize_entries_exits()
│  ├─ generate_entries_exits_difference()
│  ├─ filter_records()
│  └─ prepare_asset_evolution()
│
├─ accounting.py
│  ├─ process_income_accounting()
│  ├─ process_tax_accounting()
│  └─ process_provision_accounting()
│
├─ utils.py
│  ├─ mapear_fundo()
│  ├─ save_data()
│  ├─ load_file_directory()
│  ├─ load_data()
│  ├─ list_files()
│  ├─ define_profile_plan()
│  ├─ filtrar_data_demonstrativo()
│  ├─ extrair_valor()
│  ├─ extrair_cod_fundo()
│  ├─ mapear_classificacoes()
│  ├─ normalize_text()
│  ├─ executeFromTo()
│  ├─ procurar_palavra()
│  ├─ criar_lancamento_contabil()
│  ├─ ordenar_coluna()
│  └─ filtrar_dados()
│
├─ config.py (importado por utils e accounting)
│  ├─ cash_flow_info
│  ├─ fees_info
│  ├─ fees_accounts
│  ├─ expenses_mapping
│  ├─ provisions_mapping
│  ├─ rename_datas
│  └─ df_fundos
│
├─ filters.py
│  ├─ filter_data()
│  ├─ search_word()
│  └─ sort_columns()
│
└─ Módulos externos (reports)
   ├─ gerarRelatorio.py
   └─ gerarRelatorioDemonstrativo.py
```

---

## 🔄 FLUXO DE DADOS ENTRE ARQUIVOS

```
ARQUIVO FONTE → FUNÇÃO → TRANSFORMAÇÃO → ARQUIVO DESTINO

1. .env
   ↓
   main.py → load_dotenv()
   ↓
   Variáveis: base_path, dates, flags

2. BASE_PATH/Carteiras/{day}_{mon}/*.xlsx
   ↓
   data_transforms.py → prepare_provisions()
   ↓
   remedptions_applications_provisions, provisions

3. BASE_PATH/Carteiras/{day}_{mon}/*.xlsx
   ↓
   data_transforms.py → prepare_wallets()
   ↓
   current_wallet

4. BASE_PATH/Carteiras/{day_pre}_{mon_pre}/*.xlsx
   ↓
   Idem (current_wallet + provisions_pre)
   ↓
   previous_wallet (+ merge)

5. current_wallet + redemptions_applications_provisions
   ↓
   pd.merge()
   ↓
   current_wallet (merged)

6. previous_wallet + redemptions_applications_provisions_pre
   ↓
   pd.merge()
   ↓
   previous_wallet (merged)

7. BASE_PATH/demonstrativos/*.xlsx
   ↓
   data_transforms.py → prepare_cash_flow()
   ↓
   cash_flow

8. cash_flow
   ↓
   processarDemonstrativos() [validation]
   ↓
   True/False → continue/abort

9. cash_flow
   ↓
   data_transforms.py → totalize_entries_exits()
   ↓
   cash_flow (totalized)

10. cash_flow (totalized)
    ↓
    data_transforms.py → generate_entries_exits_difference()
    ↓
    cash_flow_balance

11. cash_flow (totalized)
    ↓
    data_transforms.py → filter_records()
    ↓
    3 DataFrames:
    ├─ acquisition_redemption
    ├─ cash_flow_filtered
    └─ expenses

12. current_wallet (merged) + previous_wallet (merged) + cash_flow_balance
    ↓
    data_transforms.py → prepare_asset_evolution()
    ↓
    asset_evolution

13. asset_evolution + cash_flow_filtered
    ↓
    accounting.py → process_income_accounting()
    ↓
    income_accounting

14. expenses
    ↓
    accounting.py → process_tax_accounting()
    ↓
    cash_flow_tax_accounting

15. provisions
    ↓
    accounting.py → process_provision_accounting()
    ↓
    provisions_accounting

16. asset_evolution + income_accounting + cash_flow_tax_accounting + provisions_accounting
    ↓
    utils.py → save_data()
    ↓
    3 Arquivos:
    ├─ evolucao_patrimonial{day}-{mon}.xlsx
    ├─ lancamentos_protheus{day}-{mon}.csv
    └─ lancamentos_segregados{day}-{mon}.xlsx
```

---

## 🎯 RESUMO: QUAL ARQUIVO CHAMA QUAL

| Quem Chama | O Quê | Arquivo | Função |
|-----------|-------|---------|---------|
| main.py | Provisões (atual) | data_transforms.py | prepare_provisions() |
| main.py | Provisões (anterior) | data_transforms.py | prepare_provisions() |
| main.py | Carteiras (atual) | data_transforms.py | prepare_wallets() |
| main.py | Carteiras (anterior) | data_transforms.py | prepare_wallets() |
| main.py | Mapear fundos | utils.py | mapear_fundo() |
| main.py | Gerar relatório | gerarRelatorio.py | gerarRelatorio() |
| main.py | Merge carteira+provisões | pandas | pd.merge() |
| main.py | Fluxo de caixa | data_transforms.py | prepare_cash_flow() |
| main.py | Validar demonstrativos | gerarRelatorioDemonstrativo.py | processarDemonstrativos() |
| main.py | Totalizar | data_transforms.py | totalize_entries_exits() |
| main.py | Diferenciar | data_transforms.py | generate_entries_exits_difference() |
| main.py | Filtrar | data_transforms.py | filter_records() |
| main.py | Evolução | data_transforms.py | prepare_asset_evolution() |
| main.py | Rendimentos | accounting.py | process_income_accounting() |
| main.py | Taxas | accounting.py | process_tax_accounting() |
| main.py | Provisões | accounting.py | process_provision_accounting() |
| main.py | Salvar | utils.py | save_data() |
| data_transforms.py | Carregar | utils.py | load_file_directory() |
| data_transforms.py | Normalizar | utils.py | normalize_text() |
| data_transforms.py | Depara | utils.py | executeFromTo() |
| data_transforms.py | Filtrar data | utils.py | filtrar_data_demonstrativo() |
| data_transforms.py | Mapear | utils.py | mapear_classificacoes() |
| accounting.py | Lançamento | utils.py | criar_lancamento_contabil() |
| utils.py | Carregar arquivo | utils.py | load_data() |
| utils.py | Listar arquivos | utils.py | list_files() |
| utils.py | Salvar Excel/CSV | pandas | to_excel(), to_csv() |


