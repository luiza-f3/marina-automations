
# 🔄 FLUXO COMPLETO DO PROJETO INVESTIMENTOS

## 📍 PONTO DE INÍCIO

```
🟢 INÍCIO: main.py (função main())
   ↓
   Carrega arquivo: .env
   - BASE_PATH (caminho dos dados)
   - DATA_ATUAL (data de processamento)
   - DATA_ANTERIOR (data anterior para comparação)
   - PROVISAO (ativa/desativa provisões)
```

---

## 🔗 FLUXO DETALHADO PASSO A PASSO

### ETAPA 1: CARREGAR CONFIGURAÇÕES
```
main.py
├─ Linha 24: load_dotenv()
├─ Linha 25: BASE_PATH ← .env
├─ Linha 26-27: DATA_ATUAL (yyyy-mm-dd) → separar em year, mon, day
├─ Linha 28-29: DATA_ANTERIOR → separar em year_pre, mon_pre, day_pre
├─ Linha 30: Formatar dt_cash_flow = 'dd/mm/yyyy'
└─ Linha 31: execute_provision ← .env ('True' ou 'False')
```

---

### ETAPA 2: PREPARAR PROVISÕES (DATA ATUAL)
```
main.py (Linha 35-37)
    ↓
data_transforms.py → prepare_provisions()
    ↓
    Arquivo de entrada: 
    BASE_PATH/Carteiras/{day}_{mon}/*.xlsx
    
    Processamento:
    └─ utils.py → load_file_directory()
       └─ Carrega arquivos XLS/XLSX dos códigos de carteira
    └─ data_transforms.py → prepare_provisions()
       ├─ Define Plano e Perfil
       ├─ Extrai RESGATE e APLICACAO (redemptions_applications_provisions)
       ├─ Extrai outras provisões (provisions)
       └─ Normaliza textos
    
    Retorna:
    ├─ redemptions_applications_provisions (DataFrame)
    └─ provisions (DataFrame)
```

---

### ETAPA 3: PREPARAR PROVISÕES (DATA ANTERIOR)
```
main.py (Linha 39-41)
    ↓
data_transforms.py → prepare_provisions()
    ↓
    Arquivo de entrada: 
    BASE_PATH/Carteiras/{day_pre}_{mon_pre}/*.xlsx
    
    Mesmo processamento da ETAPA 2
    
    Retorna:
    ├─ redemptions_applications_provisions_pre (DataFrame)
    └─ _ (ignorado)
```

---

### ETAPA 4: PREPARAR CARTEIRAS (DATA ATUAL)
```
main.py (Linha 44)
    ↓
data_transforms.py → prepare_wallets()
    ↓
    Arquivo de entrada: 
    BASE_PATH/Carteiras/{day}_{mon}/*.xlsx
    
    Processamento:
    └─ utils.py → load_file_directory()
    └─ data_transforms.py → prepare_wallets()
       ├─ Carrega colunas: Cod Fundo, Fundo, Valor Atual
       ├─ Remove linha "Total"
       ├─ Define Plano e Perfil
       ├─ Padroniza código do fundo (6 caracteres)
       ├─ Normaliza nomes de fundos
       └─ Mapeia classificações CVM
    
    Retorna:
    └─ current_wallet (DataFrame com carteira atual)
```

---

### ETAPA 5: PREPARAR CARTEIRAS (DATA ANTERIOR)
```
main.py (Linha 45)
    ↓
data_transforms.py → prepare_wallets()
    ↓
    Arquivo de entrada: 
    BASE_PATH/Carteiras/{day_pre}_{mon_pre}/*.xlsx
    
    Mesmo processamento da ETAPA 4
    
    Retorna:
    └─ previous_wallet (DataFrame com carteira anterior)
```

---

### ETAPA 6: MAPEAR NOMES DE FUNDOS
```
main.py (Linha 48)
    ↓
utils.py → mapear_fundo()
    ↓
    Entrada:
    ├─ current_wallet (DataFrame)
    └─ previous_wallet (DataFrame)
    
    Processamento:
    └─ Cria dicionário de mapeamento:
       Cod Fundo → Fundo (do current_wallet)
    └─ Aplica mapeamento ao previous_wallet
    
    Retorna:
    └─ previous_wallet (atualizado com nomes de fundos)
```

---

### ETAPA 7: GERAR RELATÓRIO DE PROVISÕES
```
main.py (Linha 51)
    ↓
gerarRelatorio()
(em: investiments/src/core/usecases/reports/gerarRelatorio.py)
    ↓
    Entrada:
    ├─ redemptions_applications_provisions (DataFrame)
    └─ current_wallet (DataFrame)
    
    Processamento:
    └─ Cria relatório de provisões de resgate/aplicação
    
    Arquivo de saída:
    └─ Relatório em Excel/arquivo (conforme implementação)
```

---

### ETAPA 8: MESCLAR CARTEIRA ATUAL COM PROVISÕES
```
main.py (Linha 53-56)
    ↓
Entrada:
├─ current_wallet (DataFrame)
└─ redemptions_applications_provisions (DataFrame)

Processamento:
└─ pd.merge():
   ├─ Junta por: Fundo, Plano, Perfil
   ├─ Tipo: left (mantém todos da carteira)
   └─ Soma valores:
      Valor Atual = Valor Atual + Valor (provisões)

Retorna:
└─ current_wallet (atualizado com provisões)
```

---

### ETAPA 9: MESCLAR CARTEIRA ANTERIOR COM PROVISÕES (ANTERIOR)
```
main.py (Linha 58-61)
    ↓
Entrada:
├─ previous_wallet (DataFrame)
└─ redemptions_applications_provisions_pre (DataFrame)

Processamento:
└─ Mesmo da ETAPA 8

Retorna:
└─ previous_wallet (atualizado com provisões)
```

---

### ETAPA 10: PREPARAR FLUXO DE CAIXA
```
main.py (Linha 64)
    ↓
data_transforms.py → prepare_cash_flow()
    ↓
    Arquivo de entrada: 
    BASE_PATH/demonstrativos/*.xlsx
    (Filtrado pela data: dt_cash_flow = 'dd/mm/yyyy')
    
    Processamento:
    └─ utils.py → load_file_directory()
    └─ data_transforms.py → prepare_cash_flow()
       ├─ Carrega colunas: Data, Historico, Entrada, Saida
       ├─ Filtra pela data atual
       ├─ utils.py → filtrar_data_demonstrativo()
       ├─ Define Plano e Perfil
       ├─ Normaliza históricos
       ├─ Padroniza códigos de fundo
       └─ Remove coluna Data
    
    Retorna:
    └─ cash_flow (DataFrame com movimentações do dia)
```

---

### ETAPA 11: PROCESSAR DEMONSTRATIVOS
```
main.py (Linha 67-74)
    ↓
gerarRelatorioDemonstrativo() → processarDemonstrativos()
(em: investiments/src/core/usecases/reports/gerarRelatorioDemonstrativo.py)
    ↓
    Entrada:
    ├─ cash_flow (DataFrame)
    ├─ dt_referencia (dd/mm/yyyy)
    └─ base_path (caminho base)
    
    Processamento:
    └─ Processa e valida demonstrativos
    
    Retorna:
    └─ resultado (True/False - sucesso/erro)
    
    Se erro → Retorna função (não continua)
```

---

### ETAPA 12: TOTALIZAR ENTRADAS E SAÍDAS
```
main.py (Linha 77)
    ↓
data_transforms.py → totalize_entries_exits()
    ↓
    Entrada:
    └─ cash_flow (DataFrame com movimentações)
    
    Processamento:
    ├─ Para cada linha:
    │  ├─ Identifica se é taxa (fees_info)
    │  ├─ Cria chave composta: cod_fundo_plano_perfil_direcao
    │  ├─ Agrupa movimentações iguais
    │  └─ Soma Entrada e Saida separadamente
    └─ Evita duplas contabilizações
    
    Retorna:
    └─ cash_flow (DataFrame totalizado)
```

---

### ETAPA 13: GERAR DIFERENÇA ENTRE ENTRADAS E SAÍDAS
```
main.py (Linha 80)
    ↓
data_transforms.py → generate_entries_exits_difference()
    ↓
    Entrada:
    └─ cash_flow (DataFrame totalizado da ETAPA 12)
    
    Processamento:
    ├─ Para cada linha (por cod_fundo_plano_perfil):
    │  ├─ Soma todas as Entradas
    │  ├─ Soma todas as Saidas
    │  ├─ Calcula diferença = Entrada + Saida
    │  ├─ Se diferença < 0 → Entrada = 0, Saida = diferença
    │  └─ Se diferença ≥ 0 → Saida = 0, Entrada = diferença
    └─ Resultado: saldo líquido do dia
    
    Retorna:
    └─ cash_flow_balance (DataFrame com diferenças)
```

---

### ETAPA 14: FILTRAR REGISTROS
```
main.py (Linha 83)
    ↓
data_transforms.py → filter_records()
    ↓
    Entrada:
    └─ cash_flow (DataFrame da ETAPA 12)
    
    Processamento:
    ├─ Itera sobre cada linha
    ├─ Se contém taxa (fees_info) → linhas_despesas
    ├─ Se contém "RESGATE DE COTAS" ou "AQUISICAO DE COTAS" → linhas_resg_aquis
    └─ Demais linhas → linhas_fundos
    
    Retorna 3 DataFrames:
    ├─ linhas_resg_aquis (acquisition_redemption)
    ├─ linhas_fundos (cash_flow_filtered)
    └─ linhas_despesas (expenses)
```

---

### ETAPA 15: PREPARAR EVOLUÇÃO PATRIMONIAL
```
main.py (Linha 86)
    ↓
data_transforms.py → prepare_asset_evolution()
    ↓
    Entrada:
    ├─ current_wallet (carteira atual - ETAPA 8)
    ├─ previous_wallet (carteira anterior - ETAPA 9)
    └─ cash_flow_balance (diferença - ETAPA 13)
    
    Processamento:
    ├─ Para cada fundo na carteira atual:
    │  ├─ Busca saldo anterior no previous_wallet
    │  ├─ Busca entrada/saida no cash_flow_balance
    │  ├─ Calcula rendimento:
    │     rendimento = Valor Atual - Saldo Anterior - Entrada - Saida
    │  └─ Adiciona à lista
    └─ Cria DataFrame final com colunas:
       Fundo, Cod Fundo, Plano, Perfil, Classificacao, 
       Saldo Anterior, Entrada, Saida, Saldo Atual, Rendimento
    
    Retorna:
    └─ asset_evolution (DataFrame - evolução patrimonial)
```

---

### ETAPA 16: PROCESSAR CONTABILIZAÇÃO DE RENDIMENTOS
```
main.py (Linha 89)
    ↓
accounting.py → process_income_accounting()
    ↓
    Entrada:
    ├─ asset_evolution (DataFrame - ETAPA 15)
    └─ cash_flow_filtered (DataFrame - ETAPA 14)
    
    Processamento:
    
    PARTE 1: Processa Rendimentos
    ├─ Para cada fundo em asset_evolution:
    │  ├─ Se Rendimento < 0:
    │  │  ├─ D: Conta Rentabilidade Negativa
    │  │  └─ C: Conta Custo Atualizado
    │  └─ Se Rendimento > 0:
    │     ├─ D: Conta Custo Atualizado
    │     └─ C: Conta Rentabilidade Positiva
    
    PARTE 2: Processa Demonstrativos (Entrada/Saida)
    ├─ Para cada linha em cash_flow_filtered:
    │  ├─ Se há Entrada:
    │  │  ├─ D: Conta Carteira
    │  │  └─ C: Conta Aplicação
    │  └─ Se há Saida:
    │     ├─ D: Conta Resgate
    │     └─ C: Conta Carteira
    
    Retorna:
    └─ income_accounting (DataFrame com lançamentos)
```

---

### ETAPA 17: PROCESSAR CONTABILIZAÇÃO DE TAXAS/DESPESAS
```
main.py (Linha 90)
    ↓
accounting.py → process_tax_accounting()
    ↓
    Entrada:
    └─ expenses (DataFrame - ETAPA 14)
    
    Processamento:
    ├─ Para cada linha em expenses:
    │  ├─ Identifica tipo de taxa/despesa
    │  ├─ Busca contas contábeis em fees_accounts
    │  ├─ Diferencia por plano/perfil:
    │  │  ├─ Se Plano=987,Perfil=19 ou Plano=952,Perfil=20 → usa PGA
    │  │  └─ Senão → usa Plano
    │  └─ Casos especiais:
    │     ├─ ESTORNO DE TAXA CETIP (reversão)
    │     ├─ IOF (cálculo diferenciado)
    │     ├─ (AJUSTE) TAXA CETIP
    │     ├─ DESPESA B 10 - TARIFA
    │     └─ (AJUSTE) TARIFA
    │
    │  Cria dois lançamentos (D/C) para cada:
    │  ├─ D: Conta da despesa
    │  └─ C: Conta do plano/PGA
    
    Retorna:
    └─ cash_flow_tax_accounting (DataFrame com lançamentos de taxa)
```

---

### ETAPA 18: PROCESSAR CONTABILIZAÇÃO DE PROVISÕES
```
main.py (Linha 91-93)
    ↓
    Se execute_provision == 'True':
        ↓
        accounting.py → process_provision_accounting()
        ↓
        Entrada:
        └─ provisions (DataFrame - ETAPA 2)
        
        Processamento:
        ├─ Para cada linha em provisions:
        │  ├─ Busca se contém alguma taxa (fees_info)
        │  ├─ Se encontra taxa:
        │  │  ├─ Se Plano≠987,19 E Plano≠952,20:
        │  │  │  ├─ D: Conta Despesa
        │  │  │  └─ C: Conta Plano
        │  │  └─ Se Plano=987,19 OU Plano=952,20:
        │  │     ├─ D: Conta Despesa
        │  │     └─ C: Conta PGA
        │  └─ Adiciona ambos os lançamentos
        
        Retorna:
        └─ provisions_accounting (DataFrame com lançamentos)
    
    Senão:
        └─ provisions_accounting = DataFrame vazio
```

---

### ETAPA 19: SALVAR DADOS
```
main.py (Linha 96-97)
    ↓
utils.py → save_data()
    ↓
    Entrada:
    ├─ asset_evolution (DataFrame)
    ├─ income_accounting (DataFrame)
    ├─ cash_flow_tax_accounting (DataFrame)
    ├─ provisions_accounting (DataFrame)
    ├─ base_path (caminho)
    ├─ day (dia)
    └─ mon (mês)
    
    Processamento:
    
    Passo 1: Filtrar dados específicos
    ├─ Filtra APLICACAO de income_accounting
    ├─ Filtra RESGATE de income_accounting
    ├─ Filtra RENDIMENTO de income_accounting
    
    Passo 2: Criar diretório
    └─ Cria: BASE_PATH/investimentos/
    
    Passo 3: Salvar Excel 1 (Evolução Patrimonial)
    └─ Nome: evolucao_patrimonial{day}-{mon}.xlsx
       └─ Contém: asset_evolution
    
    Passo 4: Salvar CSV (Protheus)
    └─ Nome: lancamentos_protheus{day}-{mon}.csv
       └─ Contém: income_accounting + tax + provisions (concatenado)
       └─ Formato: ';' como separador
    
    Passo 5: Salvar Excel 2 (Segregado)
    └─ Nome: lancamentos_segregados{day}-{mon}.xlsx
       ├─ Sheet "Provisoes{day}_{mon}": provisions_accounting
       ├─ Sheet "Despesas{day}_{mon}": cash_flow_tax_accounting
       ├─ Sheet "Rentabilidade_{day}_{mon}": filtro_rent
       ├─ Sheet "Aplicacao_{day}_{mon}": df_aplic
       └─ Sheet "Resgate_{day}_{mon}": df_resg
```

---

### ETAPA 20: CONCLUSÃO
```
main.py (Linha 99)
    ↓
    Imprime: "✅ Investment processing completed successfully!"
    ↓
    FIM DO FLUXO
```

---

## 📊 RESUMO VISUAL DO FLUXO

```
┌─────────────────────────────────────────────────────────────────┐
│                         INÍCIO: main.py                          │
│                    Carrega .env (config)                         │
└────────────────────────────────┬────────────────────────────────┘
                                 ↓
┌──────────────────────────────────────────────────────────────────┐
│                    ETAPA 1-2: Provisões (Data Atual + Anterior)   │
│         data_transforms.py → prepare_provisions()               │
└────────────────────────────────┬────────────────────────────────┘
                                 ↓
┌──────────────────────────────────────────────────────────────────┐
│                    ETAPA 3-4: Carteiras (Data Atual + Anterior)   │
│           data_transforms.py → prepare_wallets()                │
└────────────────────────────────┬────────────────────────────────┘
                                 ↓
┌──────────────────────────────────────────────────────────────────┐
│                    ETAPA 5: Mapear Fundos                         │
│              utils.py → mapear_fundo()                           │
└────────────────────────────────┬────────────────────────────────┘
                                 ↓
┌──────────────────────────────────────────────────────────────────┐
│                    ETAPA 6: Gerar Relatório                       │
│              gerarRelatorio()                                    │
└────────────────────────────────┬────────────────────────────────┘
                                 ↓
┌──────────────────────────────────────────────────────────────────┐
│                    ETAPA 7-8: Mesclar Carteiras + Provisões       │
│                         (pd.merge)                               │
└────────────────────────────────┬────────────────────────────────┘
                                 ↓
┌──────────────────────────────────────────────────────────────────┐
│                    ETAPA 9: Preparar Fluxo Caixa                  │
│           data_transforms.py → prepare_cash_flow()              │
└────────────────────────────────┬────────────────────────────────┘
                                 ↓
┌──────────────────────────────────────────────────────────────────┐
│                    ETAPA 10: Processar Demonstrativos             │
│              processarDemonstrativos() ✓/✗                      │
└────────────────────────────────┬────────────────────────────────┘
                                 ↓
┌──────────────────────────────────────────────────────────────────┐
│                    ETAPA 11-12: Totalizar + Diferenciar           │
│         totalize_entries_exits() + generate_entries_exits...     │
└────────────────────────────────┬────────────────────────────────┘
                                 ↓
┌──────────────────────────────────────────────────────────────────┐
│                    ETAPA 13: Filtrar Registros                    │
│              filter_records() → 3 DataFrames                     │
└────────────────────────────────┬────────────────────────────────┘
                                 ↓
┌──────────────────────────────────────────────────────────────────┐
│                    ETAPA 14: Evolução Patrimonial                 │
│           prepare_asset_evolution()                              │
└────────────────────────────────┬────────────────────────────────┘
                                 ↓
        ┌────────────────────────┴────────────────────────┐
        ↓                        ↓                        ↓
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  ETAPA 15:       │  │  ETAPA 16:       │  │  ETAPA 17:       │
│  Rendimentos     │  │  Taxas/Despesas  │  │  Provisões       │
│  process_income_ │  │  process_tax_    │  │  process_       │
│  accounting()    │  │  accounting()    │  │  provision_      │
│                  │  │                  │  │  accounting()    │
└────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
         │                     │                     │
         └─────────────────────┴─────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────────┐
│                    ETAPA 18: Salvar Dados                         │
│         save_data() → Excel + CSV (3 arquivos)                  │
└────────────────────────────────┬────────────────────────────────┘
                                 ↓
┌──────────────────────────────────────────────────────────────────┐
│                    ✅ CONCLUSÃO: Sucesso!                         │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔑 MAPEAMENTO DE VARIÁVEIS IMPORTANTES

| Variável | Tipo | Origem | Contém |
|----------|------|--------|--------|
| `base_path` | str | .env | Caminho raiz dos dados |
| `dt_cash_flow` | str | Calculo | Data formatada (dd/mm/yyyy) |
| `provisions` | DataFrame | ETAPA 2 | Provisões do dia atual |
| `current_wallet` | DataFrame | ETAPA 4 | Carteira do dia atual |
| `previous_wallet` | DataFrame | ETAPA 5 | Carteira do dia anterior |
| `cash_flow` | DataFrame | ETAPA 9 | Fluxo de caixa do dia |
| `cash_flow_balance` | DataFrame | ETAPA 13 | Saldo líquido por fundo |
| `asset_evolution` | DataFrame | ETAPA 15 | Evolução patrimonial |
| `income_accounting` | DataFrame | ETAPA 16 | Lançamentos de rendimento |
| `cash_flow_tax_accounting` | DataFrame | ETAPA 17 | Lançamentos de taxa |
| `provisions_accounting` | DataFrame | ETAPA 18 | Lançamentos de provisão |

---

## 📂 ARQUIVOS DE SAÍDA

```
BASE_PATH/investimentos/
├─ evolucao_patrimonial{day}-{mon}.xlsx
├─ lancamentos_protheus{day}-{mon}.csv
└─ lancamentos_segregados{day}-{mon}.xlsx
   ├─ Sheet: Provisoes{day}_{mon}
   ├─ Sheet: Despesas{day}_{mon}
   ├─ Sheet: Rentabilidade_{day}_{mon}
   ├─ Sheet: Aplicacao_{day}_{mon}
   └─ Sheet: Resgate_{day}_{mon}
```


