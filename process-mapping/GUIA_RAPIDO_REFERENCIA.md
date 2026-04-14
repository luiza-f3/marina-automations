# 📚 GUIA RÁPIDO DE REFERÊNCIA - FLUXO INVESTIMENTOS

## 🚀 INÍCIO RÁPIDO

**Arquivo de Entrada**: `investiments/main.py`
**Função Principal**: `main()`
**Configuração**: `.env` (variáveis de ambiente)

```python
if __name__ == "__main__":
    main()
```

---

## 📍 20 ETAPAS EM SEQUÊNCIA

| # | O Quê | De Onde | Para Onde | Função |
|---|-------|---------|-----------|---------|
| 1 | Carrega config | .env | Variáveis Python | load_dotenv() |
| 2 | Provisões (atual) | Carteiras/{day}_{mon} | redemptions_applications_provisions | prepare_provisions() |
| 3 | Provisões (anterior) | Carteiras/{day_pre}_{mon_pre} | redemptions_applications_provisions_pre | prepare_provisions() |
| 4 | Carteiras (atual) | Carteiras/{day}_{mon} | current_wallet | prepare_wallets() |
| 5 | Carteiras (anterior) | Carteiras/{day_pre}_{mon_pre} | previous_wallet | prepare_wallets() |
| 6 | Mapear fundos | current_wallet | previous_wallet | mapear_fundo() |
| 7 | Relatório | redemptions_applications_provisions | Arquivo | gerarRelatorio() |
| 8 | Merge cart+prov (atual) | current_wallet + provisions | current_wallet | pd.merge() |
| 9 | Merge cart+prov (anterior) | previous_wallet + provisions_pre | previous_wallet | pd.merge() |
| 10 | Fluxo de caixa | demonstrativos | cash_flow | prepare_cash_flow() |
| 11 | Validar | cash_flow | resultado True/False | processarDemonstrativos() |
| 12 | Totalizar | cash_flow | cash_flow | totalize_entries_exits() |
| 13 | Diferenciar | cash_flow | cash_flow_balance | generate_entries_exits_difference() |
| 14 | Filtrar | cash_flow | 3 DataFrames | filter_records() |
| 15 | Evolução | wallets + balance | asset_evolution | prepare_asset_evolution() |
| 16 | Rendimentos | asset_evolution + cash_flow_filtered | income_accounting | process_income_accounting() |
| 17 | Taxas | expenses | cash_flow_tax_accounting | process_tax_accounting() |
| 18 | Provisões | provisions | provisions_accounting | process_provision_accounting() |
| 19 | Salvar | 4 DataFrames | 3 Arquivos | save_data() |
| 20 | Fim | - | Print sucesso | print() |

---

## 📂 MAPEAMENTO DE ARQUIVOS PRINCIPAIS

### Entrada (Dados Brutos)

```
BASE_PATH/
├─ Carteiras/
│  ├─ {day}_{mon}/
│  │  ├─ 010134.xlsx (BRADESCO BD)
│  │  ├─ 011607.xlsx (BRADESCO PGA)
│  │  ├─ ... (todos os fundos)
│  │
│  └─ {day_pre}_{mon_pre}/
│     └─ (idem acima, data anterior)
│
└─ demonstrativos/
   ├─ 010134.xlsx
   ├─ 011607.xlsx
   └─ ... (idem)
```

### Saída (Dados Processados)

```
BASE_PATH/investimentos/
├─ evolucao_patrimonial{day}-{mon}.xlsx
│  └─ Sheet único: Evolução patrimonial completa
│
├─ lancamentos_protheus{day}-{mon}.csv
│  └─ Formato: ; separado, sem header
│
└─ lancamentos_segregados{day}-{mon}.xlsx
   ├─ Sheet: Provisoes{day}_{mon}
   ├─ Sheet: Despesas{day}_{mon}
   ├─ Sheet: Rentabilidade_{day}_{mon}
   ├─ Sheet: Aplicacao_{day}_{mon}
   └─ Sheet: Resgate_{day}_{mon}
```

---

## 🔑 PRINCIPAIS VARIÁVEIS

### De Configuração (do .env)

| Variável | Exemplo | Tipo |
|----------|---------|------|
| BASE_PATH | /home/user/data | str |
| DATA_ATUAL | 2024-02-28 | str (yyyy-mm-dd) |
| DATA_ANTERIOR | 2024-02-27 | str (yyyy-mm-dd) |
| PROVISAO | True | str ('True'/'False') |
| CONSULTA_FUNDOS | /path/to/fundos.xlsx | str |

### De Processamento (DataFrames)

| Variável | Colunas | Origem | Uso |
|----------|---------|--------|-----|
| current_wallet | Fundo, Valor Atual, Plano, Perfil, Classificacao, Cod Fundo | ETAPA 4 | ETAPA 15 |
| previous_wallet | (idem) | ETAPA 5 | ETAPA 15 |
| cash_flow | Historico, Entrada, Saida, Plano, Perfil, Cod Fundo | ETAPA 10 | ETAPA 12 |
| cash_flow_balance | (idem) | ETAPA 13 | ETAPA 15 |
| asset_evolution | Fundo, Saldo Anterior, Entrada, Saida, Saldo Atual, Rendimento | ETAPA 15 | ETAPA 16, Saída |
| income_accounting | Conta, Valor, D/C, Historico, Plano, Perfil | ETAPA 16 | Saída |
| cash_flow_tax_accounting | (idem) | ETAPA 17 | Saída |
| provisions_accounting | (idem) | ETAPA 18 | Saída |

---

## 🔄 FLUXOS CONDICIONAIS

### Se PROVISAO = 'True'

```
ETAPA 18:
├─ provisions_accounting = process_provision_accounting(provisions)
└─ Retorna DataFrame com lançamentos
```

### Se PROVISAO ≠ 'True'

```
ETAPA 18:
├─ provisions_accounting = pd.DataFrame()
└─ Retorna DataFrame vazio
```

### Se processarDemonstrativos() retorna False

```
ETAPA 11:
├─ print("❌ Errors occurred...")
├─ return (encerra main())
└─ Não continua para ETAPA 12+
```

---

## 📊 TRANSFORMAÇÕES PRINCIPAIS

### prepare_provisions()

```
Entrada:  Arquivo XLS com colunas [Despesa, Valor]
Processo: Filtra, define plano/perfil, normaliza, aplica depara
Saída:    2 DataFrames
          - redemptions_applications_provisions (RESGATE/APLICACAO)
          - provisions (outras)
```

### prepare_wallets()

```
Entrada:  Arquivo XLS com colunas [Cod Fundo, Fundo, Valor Atual]
Processo: Remove Total, define plano/perfil, normaliza, mapeia CVM
Saída:    1 DataFrame com 6 colunas
```

### prepare_cash_flow()

```
Entrada:  Arquivo XLS com [Data, Historico, Entrada, Saida]
Processo: Filtra data, extrai cod_fundo e nome, define plano/perfil
Saída:    1 DataFrame com 6 colunas
```

### prepare_asset_evolution()

```
Entrada:  3 DataFrames (current, previous, balance)
Processo: Busca saldos, calcula: rendimento = valor - saldo - entrada - saida
Saída:    1 DataFrame com 10 colunas (+ Rendimento)
```

### process_income_accounting()

```
Entrada:  2 DataFrames (asset_evolution, cash_flow_filtered)
Processo: Cria 2 lançamentos D/C por linha (rendimento/entrada/saida)
Saída:    1 DataFrame com colunas: Conta, Valor, D/C, Historico, Plano, Perfil
```

### process_tax_accounting()

```
Entrada:  1 DataFrame (expenses)
Processo: Busca contas por taxa, cria lançamentos D/C
         Diferencia por plano/perfil (PGA vs Plano)
         Casos especiais: ESTORNO, IOF, AJUSTE
Saída:    1 DataFrame (idem acima)
```

### process_provision_accounting()

```
Entrada:  1 DataFrame (provisions)
Processo: Idem process_tax_accounting() mas com lógica de provisão
Saída:    1 DataFrame (vazio se execute_provision = False)
```

---

## 🎯 RESUMO FUNÇÃO POR ARQUIVO

### main.py
```
├─ main() - Orquestração principal (107 linhas)
│  └─ Coordena todo o fluxo, chama todas as funções
```

### config.py
```
├─ cash_flow_info - Mapeamento de carteiras
├─ fees_info - Tipos de taxas
├─ fees_accounts - Contas de taxas
├─ expenses_mapping - Mapeamento de despesas
├─ provisions_mapping - Mapeamento de provisões
├─ rename_datas - Depara geral
└─ df_fundos - Leitura de CONSULTA_FUNDOS.xlsx
```

### utils.py
```
├─ load_data() - Carrega CSV/XLSX
├─ list_files() - Lista e filtra arquivos
├─ load_file_directory() - Carrega múltiplos arquivos
├─ define_profile_plan() - Define Plano e Perfil
├─ filtrar_data_demonstrativo() - Filtra por data
├─ extrair_valor() - Extrai nome do fundo de string
├─ extrair_cod_fundo() - Extrai código do fundo de string
├─ mapear_classificacoes() - Mapeia CVM
├─ normalize_text() - Normaliza (upper + unidecode)
├─ executeFromTo() - Aplica depara/rename
├─ procurar_palavra() - Busca palavra em coluna
├─ criar_lancamento_contabil() - Cria dict de lançamento
├─ ordenar_coluna() - Ordena por colunas
├─ filtrar_dados() - Filtra por lista de palavras
├─ mapear_fundo() - Mapeia nomes de fundos
└─ save_data() - Salva 3 arquivos de saída
```

### data_transforms.py
```
├─ prepare_wallets() - Prepara carteiras
├─ prepare_provisions() - Prepara provisões
├─ prepare_cash_flow() - Prepara fluxo de caixa
├─ totalize_entries_exits() - Totaliza entrada/saída
├─ generate_entries_exits_difference() - Gera diferença
├─ filter_records() - Filtra em 3 categorias
└─ prepare_asset_evolution() - Calcula evolução
```

### accounting.py
```
├─ process_income_accounting() - Contabiliza rendimentos
├─ process_tax_accounting() - Contabiliza taxas
└─ process_provision_accounting() - Contabiliza provisões
```

### filters.py
```
├─ filter_data() - Filtra por palavras-chave
├─ search_word() - Busca por palavra
└─ sort_columns() - Ordena colunas
```

---

## 🚨 PONTOS CRÍTICOS

1. **Validação de Data**: 
   - ETAPA 11 valida se data existe nos demonstrativos
   - Se falhar → interrompe processamento

2. **Mapeamento de Plano/Perfil**: 
   - Obrigatório via cash_flow_info
   - Se código não encontrado → erro

3. **Conta Contábil**:
   - Buscada em df_fundos ou fees_accounts
   - Diferencia por plano/perfil
   - Especiais: Plano 987,19 e 952,20 usam PGA

4. **Filtro de Taxas**:
   - fees_info lista todas as taxas
   - Usa `.contains()` para identificar
   - Ordem importa (alguns parciais)

5. **Cálculo de Rendimento**:
   - rendimento = Valor Atual - Saldo Anterior - Entrada - Saida
   - Entrada/Saida multiplicadas por -1 antes
   - Resultado pode ser positivo ou negativo

---

## 💾 DEPENDÊNCIAS EXTERNAS

```
Obrigatórias:
├─ pandas - Manipulação de dados
├─ openpyxl - Leitura/escrita XLSX
├─ python-dotenv - Carregamento .env
└─ unidecode - Normalização de texto

Dados:
├─ .env - Configuração
├─ CONSULTA_FUNDOS.xlsx - Leitura de fundos
└─ Estrutura de pasta BASE_PATH
```

---

## 📋 CHECKLIST DE EXECUÇÃO

```
☐ Verificar .env com caminhos corretos
☐ Verificar DATA_ATUAL e DATA_ANTERIOR existem em Carteiras/demonstrativos
☐ Verificar CONSULTA_FUNDOS.xlsx acessível
☐ Executar: python -m investimentos.main
☐ Verificar se lancamentos_*.xlsx criados
☐ Verificar planilhas segregadas têm dados
☐ Conferir valor de Rendimento = Saldo - Anterior - Entrada - Saida
☐ Validar lançamentos em D/C (saldo deve fechar)
```

---

## 🔗 RELACIONAMENTOS DE DADOS

```
Carteiras ←→ Provisões (merge por Fundo + Plano + Perfil)
    ↓
Carteira Mesclada
    ↓
Fluxo de Caixa ←→ Mescladas (busca por Cod Fundo + Plano + Perfil)
    ↓
Evolução Patrimonial
    ↓
Lançamentos (Rendimento/Entrada/Saida/Taxas/Provisões)
    ↓
Arquivos de Saída (3 tipos)
```

---

## 📞 REFERÊNCIA RÁPIDA: O QUE FAZER SE...

| Problema | Solução |
|----------|---------|
| Erro de arquivo não encontrado | Verificar DATA_ATUAL/ANTERIOR existem em Carteiras/{dia}_{mês} |
| Rendimento = 0 para todos | Verificar cash_flow_balance está sendo preenchido em ETAPA 13 |
| Lançamentos não balanceando | Verificar processo_income_accounting() está criando pares D/C |
| Taxa não reconhecida | Verificar se taxa está em fees_info (utils/consultas/fees_info.py) |
| Valores muito altos/baixos | Verificar se não está multiplicando/dividindo duas vezes |
| Plano/Perfil NULL | Verificar cash_flow_info e mapeamento de códigos |
| Arquivo CSV sem dados | Verificar se provisions_accounting está vazio (PROVISAO=False?) |


