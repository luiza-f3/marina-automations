# 🔄 DIAGRAMA ENTRADA → PROCESSAMENTO → SAÍDA

## ETAPA 1: Carregar Configurações do .env

```
ENTRADA:
┌─────────────────────┐
│  .env (arquivo)     │
│  ─────────────────  │
│ BASE_PATH           │
│ DATA_ATUAL          │
│ DATA_ANTERIOR       │
│ PROVISAO            │
└─────────────────────┘
         ↓
PROCESSAMENTO:
└─ main.py → load_dotenv()
   ├─ Lê BASE_PATH
   ├─ Split DATA_ATUAL em year, mon, day
   ├─ Split DATA_ANTERIOR em year_pre, mon_pre, day_pre
   └─ Formata dt_cash_flow

SAÍDA:
┌──────────────────────────┐
│ Variáveis Python         │
│ ──────────────────────── │
│ base_path = "caminho"    │
│ day, mon, year           │
│ day_pre, mon_pre, year_pre
│ dt_cash_flow = "dd/mm/yyyy"
│ execute_provision = True/False
└──────────────────────────┘
```

---

## ETAPA 2-3: Preparar Provisões

```
ENTRADA:
┌──────────────────────────────────┐
│ Arquivos XLSX                    │
│ ────────────────────────────────  │
│ BASE_PATH/Carteiras/{day}_{mon}/ │
│  ├─ 010134.xlsx (BRADESCO BD)    │
│  ├─ 011607.xlsx (BRADESCO PGA)   │
│  ├─ 011828.xlsx (BRADESCO PREV)  │
│  └─ ... (todos os fundos)        │
│                                  │
│ Linhas do Excel: [11:]           │
│ ├─ Coluna A: Despesa             │
│ └─ Coluna B: Valor               │
└──────────────────────────────────┘
         ↓ (ETAPA 2 - Data Atual)
PROCESSAMENTO:
└─ main.py → prepare_provisions()
   └─ data_transforms.py
      ├─ Filtra linhas entre "Descrição" e "TOTAL"
      ├─ Define Plano e Perfil por código de fundo
      ├─ Separa:
      │  ├─ RESGATE e APLICACAO
      │  └─ Outras provisões
      ├─ Normaliza textos (upper, sem acentos)
      └─ Aplica mapeamento rename_datas (depara)

SAÍDA (ETAPA 2):
┌──────────────────────────────────┐
│ 2 DataFrames retornados          │
│ ────────────────────────────────  │
│ 1. redemptions_applications_     │
│    provisions (RESGATE/APLICACAO) │
│    Colunas:                       │
│    ├─ Despesa                     │
│    ├─ Valor                       │
│    ├─ Plano                       │
│    └─ Perfil                      │
│                                  │
│ 2. provisions (Outras provisões) │
│    Colunas: Idem acima           │
└──────────────────────────────────┘
         ↓ (ETAPA 3 - Data Anterior)
PROCESSAMENTO: (Repetido para data anterior)

SAÍDA (ETAPA 3):
┌──────────────────────────────────┐
│ 2 DataFrames retornados          │
│ ────────────────────────────────  │
│ redemptions_applications_        │
│ provisions_pre (data anterior)   │
│                                  │
│ (provisions_pre ignorado)        │
└──────────────────────────────────┘
```

---

## ETAPA 4-5: Preparar Carteiras

```
ENTRADA:
┌──────────────────────────────────┐
│ Arquivos XLSX                    │
│ ────────────────────────────────  │
│ BASE_PATH/Carteiras/{day}_{mon}/ │
│ (mesmos arquivos da ETAPA 2)     │
│                                  │
│ Linhas do Excel: [10:]           │
│ ├─ Coluna A: Cod Fundo           │
│ ├─ Coluna B: Fundo               │
│ └─ Coluna H: Valor Atual         │
└──────────────────────────────────┘
         ↓ (ETAPA 4 - Data Atual)
PROCESSAMENTO:
└─ main.py → prepare_wallets()
   └─ data_transforms.py
      ├─ Extrai 3 colunas: [A, B, H]
      ├─ Remove linha com Cod Fundo = "Total"
      ├─ Renomeia colunas:
      │  ├─ A → "Cod Fundo"
      │  ├─ B → "Fundo"
      │  └─ H → "Valor Atual"
      ├─ Define Plano e Perfil (via cash_flow_info)
      ├─ Padroniza Cod Fundo (zfill(6))
      ├─ Normaliza nomes (upper, sem acentos)
      ├─ utils.py → executeFromTo()
      │  └─ Aplica mapeamento rename_datas
      └─ utils.py → mapear_classificacoes()
         └─ Busca em df_fundos → Classificacao CVM

SAÍDA (ETAPA 4):
┌────────────────────────────────────┐
│ current_wallet (DataFrame)         │
│ ────────────────────────────────── │
│ Colunas finais:                    │
│ ├─ Cod Fundo (6 dígitos)          │
│ ├─ Fundo (nome normalizado)       │
│ ├─ Valor Atual (float)            │
│ ├─ Plano (int)                    │
│ ├─ Perfil (int)                   │
│ └─ Classificacao (str - CVM)      │
│                                    │
│ Exemplo de linhas:                 │
│ ┌────────────────────────────────┐ │
│ │ Cod Fundo: 010134             │ │
│ │ Fundo: BRADESCO BD            │ │
│ │ Valor Atual: 1000000.00       │ │
│ │ Plano: 22                     │ │
│ │ Perfil: 3                     │ │
│ │ Classificacao: RENDA FIXA     │ │
│ └────────────────────────────────┘ │
└────────────────────────────────────┘
         ↓ (ETAPA 5 - Data Anterior)
PROCESSAMENTO: (Repetido para data anterior)

SAÍDA (ETAPA 5):
┌────────────────────────────────────┐
│ previous_wallet (DataFrame)        │
│ (mesma estrutura de current_wallet)│
│ (com dados do dia anterior)        │
└────────────────────────────────────┘
```

---

## ETAPA 6: Mapear Nomes de Fundos

```
ENTRADA:
┌─────────────────────────────────┐
│ 2 DataFrames:                   │
│                                 │
│ current_wallet:                 │
│ ├─ Cod Fundo: "010134"          │
│ └─ Fundo: "BRADESCO BD"         │
│                                 │
│ previous_wallet:                │
│ ├─ Cod Fundo: "010134"          │
│ └─ Fundo: "???" (a preencher)   │
└─────────────────────────────────┘
         ↓
PROCESSAMENTO:
└─ main.py → mapear_fundo()
   └─ utils.py
      ├─ Cria dicionário:
      │  {
      │    "010134": "BRADESCO BD",
      │    "011607": "BRADESCO PGA",
      │    ...
      │  }
      └─ Aplica ao previous_wallet
         └─ previous_wallet.map()

SAÍDA:
┌──────────────────────────────────┐
│ previous_wallet (atualizado)     │
│ ├─ Cod Fundo: "010134"           │
│ └─ Fundo: "BRADESCO BD" ✓        │
│    (agora preenchido!)           │
└──────────────────────────────────┘
```

---

## ETAPA 7: Gerar Relatório

```
ENTRADA:
┌─────────────────────────────────┐
│ 2 DataFrames:                   │
│                                 │
│ redemptions_applications_       │
│ provisions:                     │
│ ├─ Despesa: "RESGATE FUNDO X"  │
│ ├─ Valor: 50000                │
│ ├─ Plano: 22                   │
│ └─ Perfil: 3                   │
│                                 │
│ current_wallet:                 │
│ ├─ Fundo: "BRADESCO BD"        │
│ ├─ Valor Atual: 1000000        │
│ ├─ Plano: 22                   │
│ └─ Perfil: 3                   │
└─────────────────────────────────┘
         ↓
PROCESSAMENTO:
└─ gerarRelatorio()
   ├─ Processa dados
   └─ Gera arquivo de relatório

SAÍDA:
┌─────────────────────────────────┐
│ Arquivo de Relatório            │
│ (conforme implementação)        │
│ Contém resumo de provisões      │
└─────────────────────────────────┘
```

---

## ETAPA 8-9: Mesclar Carteiras com Provisões

```
ENTRADA:
┌─────────────────────────────────┐
│ ETAPA 8 - Data Atual:           │
│                                 │
│ current_wallet (antes merge):   │
│ ┌──────────────────────────────┐│
││ Fundo: "BRADESCO BD"          ││
││ Valor Atual: 1000000          ││
││ Plano: 22, Perfil: 3          ││
│└──────────────────────────────┘│
│                                 │
│ redemptions_applications_       │
│ provisions:                     │
│ ┌──────────────────────────────┐│
││ Despesa: "BRADESCO BD"        ││
││ Valor: 50000                  ││
││ Plano: 22, Perfil: 3          ││
│└──────────────────────────────┘│
└─────────────────────────────────┘
         ↓
PROCESSAMENTO:
└─ main.py → pd.merge()
   ├─ Junta por: Fundo=Despesa, Plano, Perfil
   ├─ Tipo: LEFT (mantém todas as linhas de wallet)
   └─ Soma: Valor Atual = Valor Atual + Valor

SAÍDA (ETAPA 8):
┌──────────────────────────────────┐
│ current_wallet (após merge):     │
│ ┌────────────────────────────────┐
│ │ Fundo: "BRADESCO BD"           │
│ │ Valor Atual: 1050000 ✓         │
│ │ (1000000 + 50000)              │
│ │ Plano: 22, Perfil: 3           │
│ └────────────────────────────────┘
└──────────────────────────────────┘
         ↓ (ETAPA 9)
PROCESSAMENTO: (Repetido para data anterior)

SAÍDA (ETAPA 9):
┌──────────────────────────────────┐
│ previous_wallet (após merge)     │
│ (mesma estrutura com dados ant.) │
└──────────────────────────────────┘
```

---

## ETAPA 10: Preparar Fluxo de Caixa

```
ENTRADA:
┌──────────────────────────────────┐
│ Arquivos XLSX (Demonstrativos)   │
│ ────────────────────────────────  │
│ BASE_PATH/demonstrativos/        │
│  ├─ 010134.xlsx                  │
│  ├─ 011607.xlsx                  │
│  └─ ... (todos os fundos)        │
│                                  │
│ Linhas do Excel: [7:]            │
│ ├─ Coluna A: Data (dd/mm/yyyy)  │
│ ├─ Coluna B: Historico           │
│ ├─ Coluna C: Entrada             │
│ └─ Coluna D: Saida               │
└──────────────────────────────────┘
         ↓
PROCESSAMENTO:
└─ main.py → prepare_cash_flow()
   └─ data_transforms.py
      ├─ Extrai 4 primeiras colunas
      ├─ Renomeia: Data, Historico, Entrada, Saida
      ├─ utils.py → filtrar_data_demonstrativo()
      │  ├─ Remove linhas com Historico = "Saldo"
      │  ├─ Busca linhas com Data = dt_cash_flow
      │  ├─ Extrai até próxima data (ou fim)
      │  ├─ Extrai Cod Fundo do campo Historico
      │  │  └─ Formato: "Fundo NOME [CODIGO]"
      │  └─ Extrai nome do fundo de Historico
      ├─ Define Plano e Perfil
      ├─ Normaliza Historico
      ├─ utils.py → executeFromTo()
      ├─ Padroniza Cod Fundo (zfill(6))
      └─ Remove coluna Data

SAÍDA:
┌──────────────────────────────────┐
│ cash_flow (DataFrame)            │
│ ────────────────────────────────  │
│ Colunas:                         │
│ ├─ Historico (fundo/taxa norm.) │
│ ├─ Entrada (float)               │
│ ├─ Saida (float)                 │
│ ├─ Plano (int)                   │
│ ├─ Perfil (int)                  │
│ └─ Cod Fundo (6 dígitos)         │
│                                  │
│ Exemplo:                         │
│ ┌────────────────────────────────┐
│ │ Historico: "FUNDO BRADESCO BD" │
│ │ Entrada: 100000                │
│ │ Saida: 0                       │
│ │ Plano: 22                      │
│ │ Perfil: 3                      │
│ │ Cod Fundo: "010134"            │
│ └────────────────────────────────┘
└──────────────────────────────────┘
```

---

## ETAPA 11: Processar Demonstrativos

```
ENTRADA:
┌──────────────────────────────────┐
│ cash_flow (DataFrame)            │
│ dt_referencia = "dd/mm/yyyy"     │
│ base_path = "caminho"            │
└──────────────────────────────────┘
         ↓
PROCESSAMENTO:
└─ gerarRelatorioDemonstrativo()
   └─ processarDemonstrativos()
      ├─ Valida dados
      ├─ Processa demonstrativos
      └─ Retorna True/False

SAÍDA:
┌──────────────────────────────────┐
│ resultado = True ✓               │
│ (ou False se erro)               │
└──────────────────────────────────┘
         ↓
SE FALSO:
└─ print("❌ Errors occurred...")
   └─ return (encerra função)
```

---

## ETAPA 12: Totalizar Entradas e Saídas

```
ENTRADA:
┌──────────────────────────────────┐
│ cash_flow (DataFrame)            │
│ Múltiplas linhas com:            │
│ ├─ Entrada: 100000              │
│ ├─ Saida: 0                     │
│ ├─ Fundo: "BRADESCO BD"         │
│ ├─ Cod Fundo: "010134"          │
│ ├─ Plano: 22, Perfil: 3         │
│ └─ Taxa?: "TAXA ADMIN" (ou não) │
└──────────────────────────────────┘
         ↓
PROCESSAMENTO:
└─ data_transforms.py → totalize_entries_exits()
   ├─ Para cada linha:
   │  ├─ Se contém taxa (em fees_info):
   │  │  └─ Chave única com taxa_count
   │  ├─ Senão:
   │  │  └─ Chave = cod_fundo_plano_perfil_direcao
   │  └─ Agrupa e soma Entrada/Saida
   └─ Reconstrói DataFrame consolidado

SAÍDA:
┌──────────────────────────────────┐
│ cash_flow (após totalize)        │
│ Colunas:                         │
│ ├─ Historico                     │
│ ├─ Entrada (somado)              │
│ ├─ Saida (somado)                │
│ ├─ Plano                         │
│ ├─ Perfil                        │
│ └─ Cod Fundo                     │
│                                  │
│ Exemplo:                         │
│ ┌────────────────────────────────┐
│ │ Historico: "BRADESCO BD"       │
│ │ Entrada: 200000 ✓ (agregado)  │
│ │ Saida: 0                       │
│ │ Plano: 22, Perfil: 3           │
│ │ Cod Fundo: "010134"            │
│ └────────────────────────────────┘
└──────────────────────────────────┘
```

---

## ETAPA 13: Gerar Diferença Entre Entradas e Saídas

```
ENTRADA:
┌──────────────────────────────────┐
│ cash_flow (totalized)            │
│ Exemplo de múltiplas linhas:     │
│                                  │
│ Linha 1:                         │
│ ├─ Cod Fundo: "010134"           │
│ ├─ Entrada: 200000               │
│ ├─ Saida: 0                      │
│ ├─ Plano: 22, Perfil: 3          │
│                                  │
│ Linha 2:                         │
│ ├─ Cod Fundo: "010134"           │
│ ├─ Entrada: 0                    │
│ ├─ Saida: 50000                  │
│ ├─ Plano: 22, Perfil: 3          │
└──────────────────────────────────┘
         ↓
PROCESSAMENTO:
└─ data_transforms.py → generate_entries_exits_difference()
   ├─ Agrupa por: cod_fundo_plano_perfil
   ├─ Para cada grupo:
   │  ├─ soma_entrada = 200000
   │  ├─ soma_saida = 50000
   │  ├─ diferenca = 200000 + (-50000) = 150000
   │  ├─ Se diferenca < 0:
   │  │  ├─ Entrada = 0
   │  │  └─ Saida = diferenca (negativo)
   │  └─ Se diferenca ≥ 0:
   │     ├─ Saida = 0
   │     └─ Entrada = diferenca
   └─ Reconstrói com 1 linha por fundo/plano/perfil

SAÍDA:
┌──────────────────────────────────┐
│ cash_flow_balance (DataFrame)    │
│ Uma linha por fundo/plano/perfil │
│                                  │
│ Exemplo:                         │
│ ┌────────────────────────────────┐
│ │ Cod Fundo: "010134"            │
│ │ Entrada: 150000 ✓ (saldo)     │
│ │ Saida: 0                       │
│ │ Plano: 22, Perfil: 3           │
│ │ Historico: "BRADESCO BD"       │
│ └────────────────────────────────┘
└──────────────────────────────────┘
```

---

## ETAPA 14: Filtrar Registros

```
ENTRADA:
┌──────────────────────────────────┐
│ cash_flow (DataFrame)            │
│ Múltiplas linhas com Historico:  │
│                                  │
│ Tipo 1: "FUNDO BRADESCO BD"     │
│ Tipo 2: "TAXA ADMINISTRACAO"    │
│ Tipo 3: "RESGATE DE COTAS"      │
│ Tipo 4: "AQUISICAO DE COTAS"    │
└──────────────────────────────────┘
         ↓
PROCESSAMENTO:
└─ data_transforms.py → filter_records()
   ├─ Itera cada linha:
   │  ├─ Se Historico contém taxa (em fees_info):
   │  │  └─ Adiciona a linhas_despesas
   │  ├─ Elif "RESGATE DE COTAS" ou "AQUISICAO DE COTAS":
   │  │  └─ Adiciona a linhas_resg_aquis
   │  └─ Else:
   │     └─ Adiciona a linhas_fundos
   └─ Reconstrói 3 DataFrames

SAÍDA:
┌──────────────────────────────────┐
│ 3 DataFrames retornados:         │
│                                  │
│ 1. linhas_resg_aquis             │
│    (acquisition_redemption)      │
│    Contém: RESGATE/AQUISICAO     │
│                                  │
│ 2. linhas_fundos                 │
│    (cash_flow_filtered)          │
│    Contém: Fundos normais        │
│                                  │
│ 3. linhas_despesas               │
│    (expenses)                    │
│    Contém: Taxas/despesas        │
└──────────────────────────────────┘
```

---

## ETAPA 15: Preparar Evolução Patrimonial

```
ENTRADA:
┌──────────────────────────────────┐
│ 3 DataFrames:                    │
│                                  │
│ 1. current_wallet (merged):      │
│    ├─ Fundo: "BRADESCO BD"      │
│    ├─ Valor Atual: 1050000      │
│    ├─ Cod Fundo: "010134"       │
│    └─ Plano: 22, Perfil: 3      │
│                                  │
│ 2. previous_wallet (merged):     │
│    ├─ Fundo: "BRADESCO BD"      │
│    ├─ Valor Atual: 1000000      │
│    ├─ Cod Fundo: "010134"       │
│    └─ Plano: 22, Perfil: 3      │
│                                  │
│ 3. cash_flow_balance:            │
│    ├─ Fundo: "BRADESCO BD"      │
│    ├─ Entrada: 150000            │
│    ├─ Saida: 0                  │
│    ├─ Cod Fundo: "010134"       │
│    └─ Plano: 22, Perfil: 3      │
└──────────────────────────────────┘
         ↓
PROCESSAMENTO:
└─ data_transforms.py → prepare_asset_evolution()
   ├─ Para cada fundo em current_wallet:
   │  ├─ Busca saldo anterior em previous_wallet
   │  │  └─ saldo_anterior = 1000000
   │  ├─ Busca fluxo em cash_flow_balance
   │  │  ├─ entrada = 150000
   │  │  └─ saida = 0
   │  └─ Calcula rendimento:
   │     ├─ Multiplica entrada/saida por -1
   │     └─ rendimento = Valor Atual - saldo_anterior - entrada - saida
   │        = 1050000 - 1000000 - (-150000) - 0
   │        = 200000
   └─ Cria DataFrame com listas

SAÍDA:
┌──────────────────────────────────┐
│ asset_evolution (DataFrame)      │
│ ────────────────────────────────  │
│ Colunas:                         │
│ ├─ Fundo                         │
│ ├─ Cod Fundo                     │
│ ├─ Plano                         │
│ ├─ Perfil                        │
│ ├─ Classificacao                 │
│ ├─ Saldo Anterior: 1000000       │
│ ├─ Entrada: -150000 (ajustado)  │
│ ├─ Saida: 0                      │
│ ├─ Saldo Atual: 1050000          │
│ └─ Rendimento: 200000 ✓          │
└──────────────────────────────────┘
```

---

## ETAPA 16-18: Contabilizações (3 tipos paralelos)

```
┌─────────────────────────────────────────────────────────────┐
│ ETAPA 16: CONTABILIZAR RENDIMENTOS                          │
├─────────────────────────────────────────────────────────────┤
│ ENTRADA:                                                    │
│ ├─ asset_evolution (Saldo Anterior, Rendimento)            │
│ └─ cash_flow_filtered (Entrada, Saida)                     │
│                                                             │
│ PROCESSAMENTO:                                              │
│ ├─ Parte 1: Rendimentos                                     │
│ │  ├─ Se Rendimento < 0:                                   │
│ │  │  ├─ D: Conta Rentabilidade Negativa                   │
│ │  │  └─ C: Conta Custo Atualizado                         │
│ │  └─ Se Rendimento > 0:                                   │
│ │     ├─ D: Conta Custo Atualizado                         │
│ │     └─ C: Conta Rentabilidade Positiva                   │
│ │                                                          │
│ ├─ Parte 2: Demonstrativos (Entrada/Saida)                 │
│ │  ├─ Se Entrada ≠ 0:                                      │
│ │  │  ├─ D: Conta Carteira                                 │
│ │  │  └─ C: Conta Aplicação                                │
│ │  └─ Se Saida ≠ 0:                                        │
│ │     ├─ D: Conta Resgate                                  │
│ │     └─ C: Conta Carteira                                 │
│ │                                                          │
│ SAÍDA:                                                      │
│ └─ income_accounting (DataFrame com lançamentos D/C)       │
│    Exemplo:                                                │
│    ┌──────────────────────────────────────────────────────┐
│    │ Conta: 20103100101000                                │
│    │ Valor: 200000                                        │
│    │ D/C: "D"                                             │
│    │ Historico: "RENDIMENTO - BRADESCO BD"               │
│    │ Plano: 22, Perfil: 3                                │
│    └──────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ ETAPA 17: CONTABILIZAR TAXAS/DESPESAS                       │
├─────────────────────────────────────────────────────────────┤
│ ENTRADA:                                                    │
│ └─ expenses (DataFrame com taxas/despesas)                 │
│    Exemplo:                                                │
│    ├─ Historico: "TAXA ADMINISTRACAO"                      │
│    ├─ Entrada: 1000 (ou Saida: 1000)                      │
│    ├─ Plano: 22, Perfil: 3                                 │
│    └─ Cod Fundo: "010134"                                  │
│                                                             │
│ PROCESSAMENTO:                                              │
│ ├─ Para cada taxa/despesa:                                 │
│ │  ├─ Identifica tipo em fees_info                         │
│ │  ├─ Busca contas em fees_accounts:                       │
│ │  │  {                                                    │
│ │  │    "TAXA ADMINISTRACAO": {                            │
│ │  │      "Plano": 20103100101000,                         │
│ │  │      "PGA": 20103100102000,                           │
│ │  │      "Despesa": 50298990100000                        │
│ │  │    }                                                  │
│ │  │  }                                                    │
│ │  ├─ Se Plano ∈ [987,19] ou [952,20]:                    │
│ │  │  └─ Usa conta PGA                                     │
│ │  └─ Senão:                                              │
│ │     └─ Usa conta Plano                                   │
│ │                                                          │
│ │  Casos especiais:                                        │
│ │  ├─ ESTORNO: Cria reversão                               │
│ │  ├─ IOF: Tratamento diferenciado                         │
│ │  ├─ (AJUSTE) TAXA/TARIFA: Ajustes                        │
│ │  └─ DESPESA B 10: Tarifa de liquidação                   │
│ │                                                          │
│ SAÍDA:                                                      │
│ └─ cash_flow_tax_accounting (DataFrame com lançamentos)    │
│    Cria 2 linhas por taxa (D/C)                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ ETAPA 18: CONTABILIZAR PROVISÕES                            │
├─────────────────────────────────────────────────────────────┤
│ ENTRADA:                                                    │
│ └─ provisions (DataFrame - ETAPA 2)                        │
│                                                             │
│ PROCESSAMENTO:                                              │
│ ├─ Se execute_provision == 'True':                         │
│ │  ├─ Para cada provisão:                                  │
│ │  │  ├─ Busca se contém taxa em fees_info                │
│ │  │  ├─ Se encontra:                                     │
│ │  │  │  ├─ Se Plano ∉ [987,19] e [952,20]:              │
│ │  │  │  │  ├─ D: Conta Despesa (de fees_accounts)       │
│ │  │  │  │  └─ C: Conta Plano                             │
│ │  │  │  └─ Senão (Planos especiais):                     │
│ │  │  │     ├─ D: Conta Despesa                           │
│ │  │  │     └─ C: Conta PGA                               │
│ │  │  └─ Adiciona 2 lançamentos (D/C)                      │
│ │  └─ Reconstrói DataFrame                                 │
│ └─ Senão:                                                  │
│    └─ provisions_accounting = DataFrame vazio              │
│                                                             │
│ SAÍDA:                                                      │
│ └─ provisions_accounting (DataFrame)                       │
│    ou DataFrame vazio se PROVISAO=False                    │
└─────────────────────────────────────────────────────────────┘
```

---

## ETAPA 19: Salvar Dados

```
ENTRADA:
┌──────────────────────────────────┐
│ 4 DataFrames:                    │
│                                  │
│ 1. asset_evolution               │
│ 2. income_accounting             │
│ 3. cash_flow_tax_accounting      │
│ 4. provisions_accounting         │
└──────────────────────────────────┘
         ↓
PROCESSAMENTO:
└─ utils.py → save_data()
   │
   ├─ Passo 1: Filtrar dados específicos
   │  ├─ Filtra APLICACAO de income_accounting
   │  ├─ Filtra RESGATE de income_accounting
   │  └─ Filtra RENDIMENTO de income_accounting
   │
   ├─ Passo 2: Criar diretório de saída
   │  └─ BASE_PATH/investimentos/
   │
   ├─ Passo 3: Salvar Excel 1 (Evolução Patrimonial)
   │  ├─ Nome: evolucao_patrimonial{day}-{mon}.xlsx
   │  ├─ Contém: asset_evolution
   │  └─ Colunas todas
   │
   ├─ Passo 4: Salvar CSV (Protheus)
   │  ├─ Nome: lancamentos_protheus{day}-{mon}.csv
   │  ├─ Contém: income_accounting + tax + provisions
   │  └─ Formato: ';' como separador, sem header
   │
   └─ Passo 5: Salvar Excel 2 (Segregado)
      ├─ Nome: lancamentos_segregados{day}-{mon}.xlsx
      ├─ Sheet 1 "Provisoes{day}_{mon}": provisions_accounting
      ├─ Sheet 2 "Despesas{day}_{mon}": cash_flow_tax_accounting
      ├─ Sheet 3 "Rentabilidade_{day}_{mon}": filtro_rent
      ├─ Sheet 4 "Aplicacao_{day}_{mon}": df_aplic
      └─ Sheet 5 "Resgate_{day}_{mon}": df_resg

SAÍDA (ARQUIVOS CRIADOS):
┌──────────────────────────────────────────────────┐
│ BASE_PATH/investimentos/                         │
│ ├─ evolucao_patrimonial28-02.xlsx                │
│ │  └─ 1 sheet com dados de evolução              │
│ ├─ lancamentos_protheus28-02.csv                 │
│ │  └─ Dados em formato CSV para Protheus        │
│ └─ lancamentos_segregados28-02.xlsx              │
│    ├─ Sheet: Provisoes28_02                      │
│    ├─ Sheet: Despesas28_02                       │
│    ├─ Sheet: Rentabilidade_28_02                 │
│    ├─ Sheet: Aplicacao_28_02                     │
│    └─ Sheet: Resgate_28_02                       │
└──────────────────────────────────────────────────┘
```

---

## ETAPA 20: Conclusão

```
SAÍDA FINAL:
└─ print("✅ Investment processing completed successfully!")
   
FIM DO PROCESSO ✓
```


