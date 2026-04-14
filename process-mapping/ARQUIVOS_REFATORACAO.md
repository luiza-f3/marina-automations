# Sequência de Arquivos da Refatoração - Investimentos

## Ordem de Dependências e Processamento

### 1️⃣ Configurações e Dicionários
**Arquivo**: `investiments/src/config.py`
**Função**: Centraliza todos os dicionários de mapeamento e configurações
**Dependências**: 
- `investiments/src/utils/consultas/cash_flow_info.py`
- `investiments/src/utils/consultas/expenses_mapping.py`
- `investiments/src/utils/consultas/fees_accounts.py`
- `investiments/src/utils/consultas/fees_info.py`
- `investiments/src/utils/consultas/provisions_mapping.py`
- `investiments/src/utils/consultas/rename_data.py`

---

### 2️⃣ Funções Utilitárias
**Arquivo**: `investiments/src/utils.py`
**Função**: Consolida funções de carregamento, manipulação de texto e dados
**Dependências**: `config.py`
**Responsabilidades**:
- Carregar arquivos (CSV, XLSX, XLS)
- Normalizar texto
- Extrair valores de códigos de fundos
- Criar lançamentos contábeis
- Salvar dados processados

---

### 3️⃣ Transformações de Dados
**Arquivo**: `investiments/src/data_transforms.py`
**Função**: Prepara e transforma dados brutos em estruturas usáveis
**Dependências**: `config.py`, `utils.py`
**Responsabilidades**:
- `prepare_wallets()` - Prepara carteiras
- `prepare_provisions()` - Prepara provisões
- `prepare_cash_flow()` - Prepara fluxo de caixa
- `totalize_entries_exits()` - Totaliza entradas/saídas
- `generate_entries_exits_difference()` - Calcula diferenças
- `filter_records()` - Filtra registros
- `prepare_asset_evolution()` - Prepara evolução patrimonial

---

### 4️⃣ Contabilização
**Arquivo**: `investiments/src/accounting.py`
**Função**: Gera lançamentos contábeis
**Dependências**: `config.py`, `utils.py`
**Responsabilidades**:
- `process_income_accounting()` - Processa rendimentos
- `process_provision_accounting()` - Processa provisões
- `process_tax_accounting()` - Processa taxas e despesas

---

### 5️⃣ Filtros e Ordenação
**Arquivo**: `investiments/src/filters.py`
**Função**: Funções complementares de filtro
**Dependências**: Nenhuma externa (usa pandas nativo)
**Responsabilidades**:
- `filter_data()` - Filtra por palavras-chave
- `search_word()` - Busca por palavra
- `sort_columns()` - Ordena colunas

---

### 6️⃣ Orquestração Principal
**Arquivo**: `investiments/main.py`
**Função**: Executa todo o fluxo de processamento
**Dependências**: `config.py`, `utils.py`, `data_transforms.py`, `accounting.py`
**Fluxo**:
1. Carrega configurações do .env
2. Prepara provisões (data atual e anterior)
3. Prepara carteiras (data atual e anterior)
4. Mapeia nomes de fundos
5. Gera relatório
6. Mescla carteiras com provisões
7. Prepara fluxo de caixa
8. Processa demonstrativos
9. Totaliza entradas/saídas
10. Gera diferenças
11. Filtra registros
12. Prepara evolução patrimonial
13. Processa contabilizações (rendimento, taxas, provisões)
14. Salva dados em arquivos Excel/CSV

---

## Fluxo Completo de Execução

```
config.py (Lê configurações)
    ↓
utils.py (Funções auxiliares)
    ↓
data_transforms.py (Transforma dados brutos)
    ↓
accounting.py (Gera lançamentos)
    ↓
filters.py (Filtra dados) [opcional/complementar]
    ↓
main.py (Orquestra e executa tudo)
```

---

## Arquivos Existentes que Continuam Suportados

- `investiments/src/core/carteira/carteira.py` → Substituído por `data_transforms.prepare_wallets()` e `data_transforms.prepare_provisions()`
- `investiments/src/core/demonstrativo/fluxo_caixa.py` → Substituído por `data_transforms.prepare_cash_flow()` e funções relacionadas
- `investiments/src/core/usecases/prepararEvolucaoPatrimonial.py` → Substituído por `data_transforms.prepare_asset_evolution()`
- `investiments/src/core/usecases/prepararLancamentoContabil.py` → Substituído por `accounting.process_income_accounting()`
- `investiments/src/core/usecases/provisao_lancamento.py` → Substituído por `accounting.process_provision_accounting()`
- `investimentos/src/core/usecases/despesasTaxasDemonstrativo.py` → Substituído por `accounting.process_tax_accounting()`
- `investimentos/src/utils/tools.py` → Consolidado em `utils.py`
- `investimentos/src/utils/data_loader.py` → Consolidado em `utils.py`

---

## Resumo das Melhorias

| Aspecto | Antes | Depois |
|--------|-------|--------|
| Arquivos principais | 8+ dispersos | 6 centralizados |
| Linhas de código (main) | 98 | 90 (mais limpo) |
| Clareza | Classes com métodos complexos | Funções simples e nomeadas |
| Manutenção | Difícil rastrear dependências | Dependências explícitas |
| Reutilização | Baixa (métodos acoplados) | Alta (funções modulares) |
| Documentação | Mínima | Docstrings em todas as funções |

