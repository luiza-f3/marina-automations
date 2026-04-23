# Marina automations - main.py (Módulo Folha de Benefícios)

Este módulo automatiza o processamento, validação e contabilização da folha de benefícios, integrando dados de empréstimos, provisões e deduções, e gerando relatórios contábeis detalhados. Ele foi desenvolvido para facilitar a rotina de fechamento contábil, garantindo padronização, rastreabilidade e validação cruzada dos dados.

---

## Sumário

- [Introdução](#introdução)
- [Pré-requisitos](#pré-requisitos)
- [Configurações](#configurações)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Fluxo Completo de Execução](#fluxo-completo-de-execução)
- [Detalhamento dos Módulos](#detalhamento-dos-módulos)
- [Arquivos de Entrada e Saída](#arquivos-de-entrada-e-saída)
- [Mapeamentos e Configuração](#mapeamentos-e-configuração)
- [Execução](#execução)
- [FAQ e Troubleshooting](#faq-e-troubleshooting)
- [Contato/Suporte](#contatosuporte)

---

## Introdução

O script `main.py` centraliza o processamento da folha de benefícios, realizando:
- Leitura e filtragem dos dados processados e de consulta;
- Padronização textual para evitar divergências;
- Processamento de empréstimos, provisões e deduções;
- Validação cruzada dos dados com a planilha de consulta;
- Consolidação e contabilização dos lançamentos;
- Geração de relatório contábil pronto para integração com sistemas financeiros.

Ideal para equipes de contabilidade, controladoria e TI que buscam automação, rastreabilidade e redução de erros manuais.

---

## Pré-requisitos

- **Python**: 3.12 ou superior
- **Bibliotecas Python**:
  - pandas
  - openpyxl
- **Instalação das dependências**:

```powershell
pip install pandas openpyxl
```

- **Sistema operacional**: Windows
- **Estrutura de diretórios**: conforme o projeto (veja abaixo)

---

## Configurações

- **Variável de data**: Edite a variável `payment_date` no início do `main.py` para a competência desejada, no formato `YYYY-MM-DD`.
- **Caminhos de arquivos**: Os caminhos são montados automaticamente, mas certifique-se de que os arquivos estejam nas pastas corretas.
- **Personalização**: Para adaptar a outros contextos, ajuste os nomes das colunas e caminhos conforme necessário.

---

## Estrutura do Projeto

```
data_preprocessing/
├── benefits_sheet/
│   ├── main.py                         ← Script principal responsável por orquestrar o processamento da folha de benefícios
│
│   ├── processed/
│   │   └── folha_beneficios_processado.csv  ← Arquivo de saída com os dados da folha já processados
│
│   ├── raw/
│   │   └── folha_beneficios.xls/.xlsx       ← Arquivo de entrada com os dados brutos da folha de benefícios
│
│   ├── src/
│   │   ├── BenefitsAccounting.py      ← Consolidação e contabilização dos dados da folha de benefícios
│   │   ├── DeductionAccounting.py    ← Processamento e contabilização das deduções
│   │   ├── LoanAccounting.py         ← Processamento e contabilização dos empréstimos
│   │   └── ProvisionAccounting.py   ← Processamento e contabilização das provisões
│
│   └── utils/
│       ├── AccountingAccount.py     ← Mapeamento das contas contábeis utilizadas no processamento
│       └── tools.py                ← Funções utilitárias (ex: normalização, tratamento de dados)
│
└── docs/
    └── Benefits - README.md        ← Manual e documentação do módulo de folha de benefícios
```

---

## Fluxo Completo de Execução

### Etapa 1 — Leitura dos Dados de Benefícios  
**Arquivo:** `main.py`  
**Função:** (bloco principal)
- Lê o arquivo `folha_beneficios_processado.csv` (dados processados da folha) e o arquivo `consulta_folha_beneficios.xlsx` (planilha de consulta, aba Planilha2).
- Utiliza `pandas.read_csv` e `pandas.read_excel`.
- Exemplo de dados lidos:

  | Data de pagamento | Tipo de beneficio | Item folha | Valor |
  |-------------------|-------------------|------------|-------|
  | 2025-07-29        | APOSENTADORIA     | 123        | 1000  |

---

### Etapa 2 — Filtragem por Data de Pagamento  
**Arquivo:** `main.py`  
**Função:** (bloco principal)
- Filtra o DataFrame para manter apenas registros com a data definida em `payment_date`.
- Exemplo: Se `payment_date = "2025-07-29"`, apenas linhas dessa data permanecem.

---

### Etapa 3 — Padronização de Valores  
**Arquivo:** `utils/tools.py`  
**Função:** `normalize_text()`
- Padroniza colunas como `Tipo de folha`, `Item folha`, `Grupo de beneficio`, `Tipo de beneficio` para evitar divergências de maiúsculas/minúsculas e espaços.
- Exemplo: “Aposentadoria” e “APOSENTADORIA” passam a ser tratados como iguais.

---

### Etapa 4 — Processamento dos Módulos  
**Arquivos/Funções:**
- `src/LoanAccounting.py` → `LoanAccounting.create_loans()`
- `src/ProvisionAccounting.py` → `ProvisionAccounting.create_provision()`
- `src/DeductionAccounting.py` → `DeductionAccounting.create_deduction()`
- Cada módulo processa o DataFrame filtrado para gerar DataFrames específicos:
  - **Empréstimos:** Identifica e consolida empréstimos.
  - **Provisões:** Calcula e organiza provisões.
  - **Deduções:** Processa deduções cruzando com a planilha de consulta.
- Exemplo de saída: DataFrames com colunas como `Tipo de beneficio`, `Item folha`, `Valor`, etc.

---

### Etapa 5 — Validação Cruzada  
**Arquivo:** `main.py`  
**Função:** (bloco principal)
- Para cada DataFrame (dedução, empréstimos, provisão), verifica se os valores das colunas obrigatórias (`Tipo de beneficio`, `Item folha`) existem na planilha de consulta.
- Imprime alertas para valores ausentes e confirma colunas validadas.
- Exemplo de alerta:

  ❌ DataFrame Deducao possui valores ausentes na coluna 'Tipo de beneficio':
  “PENSÃO” - Tipo de beneficio - Data = 29/07/2025

---

### Etapa 6 — Consolidação e Contabilização  
**Arquivos/Funções:**
- `src/BenefitsAccounting.py` → `BenefitsAccounting.account()`
- `utils/AccountingAccount.py` → `AccountingAccount.duplicate_postings_for_accounts()`
- Consolida os DataFrames de dedução, empréstimos e provisão.
- Remove lançamentos de valor zero.
- Duplica lançamentos conforme regras contábeis.
- Ajusta formatos de colunas (ex: zera à esquerda em patrocinadora, datas no padrão brasileiro).
- Exemplo de saída:

  | Plano  | Perfil | Valor | D/C | Data       | Patrocinadora |
  |--------|--------|-------|-----|------------|---------------|
  | 010134 | 01     | 1000  | D   | 29-07-2025 | 001           |

---

### Etapa 7 — Geração do Arquivo de Saída  
**Arquivo:** `main.py`  
**Função:** (bloco principal)
- Exporta o DataFrame final para Excel, nomeando como `folha_contabilizadaDD-MM-YYYY.xlsx` na pasta `Beneficios` do usuário.
- Exemplo de nome: `folha_contabilizada29-07-2025.xlsx`

---

## Detalhamento dos Módulos

- **LoanAccounting**: Processa e consolida informações de empréstimos presentes na folha.
- **ProvisionAccounting**: Calcula e organiza provisões a partir dos dados filtrados.
- **DeductionAccounting**: Processa deduções, cruzando com a planilha de consulta para garantir integridade.
- **BenefitsAccounting**: Consolida todos os dados processados, aplica regras de contabilização e prepara o DataFrame final.
- **AccountingAccount**: Responsável por mapear e duplicar lançamentos conforme regras contábeis específicas.
- **normalize_text**: Função utilitária para padronização textual de colunas, evitando erros por diferenças de formatação.

---

## Arquivos de Entrada e Saída

### Entrada

- **folha_beneficios_processado.csv** (em `processed/`):
  - Deve conter colunas como: `Data de pagamento`, `Tipo de beneficio`, `Item folha`, entre outras.
  - Exemplo de linha:
    | Data de pagamento | Tipo de beneficio | Item folha | Valor |
    |-------------------|-------------------|------------|-------|
    | 2025-07-29        | APOSENTADORIA     | 123        | 1000  |

- **consulta_folha_beneficios.xlsx** (em `Beneficios/`):
  - Usada para validação cruzada. Deve conter as colunas: `Tipo de folha`, `Item folha`, `Grupo de beneficio`, `Tipo de beneficio`.

### Saída

- **folha_contabilizadaDD-MM-YYYY.xlsx** (em `Beneficios/`):
  - Contém os lançamentos contábeis finais, prontos para integração.
  - Colunas típicas: `Plano`, `Perfil`, `Valor`, `D/C`, `Data`, `Patrocinadora`, etc.

---

## Mapeamentos e Configuração

- **Colunas obrigatórias para validação**: `Tipo de beneficio`, `Item folha`.
- **Datas e competências**: Extraídas da variável `payment_date`.
- **Mapeamento de contas contábeis**: Realizado via `AccountingAccount.py`, que pode ser customizado conforme as regras da instituição.
- **Personalização**: Para adaptar a outros contextos, ajuste as funções de processamento e os mapeamentos conforme necessário.

---

## Execução

1. Ajuste a variável `payment_date` no início do `main.py` para a competência desejada.
2. Certifique-se de que os arquivos de entrada estejam nas pastas corretas.
3. Execute o script principal:

```powershell
python benefits_sheet/main.py
```

4. O arquivo de saída será gerado na pasta `Beneficios` do diretório do usuário, com nome `folha_contabilizadaDD-MM-YYYY.xlsx`.

---

## FAQ e Troubleshooting

- **Erro: Arquivo não encontrado**
  - Verifique se os arquivos de entrada estão nos caminhos corretos.
- **Erro de coluna ausente**
  - Confirme se os arquivos possuem todas as colunas obrigatórias.
- **Arquivo de saída vazio**
  - Certifique-se de que há registros para a data informada em `payment_date`.
- **Problemas de encoding**
  - Salve os arquivos CSV em UTF-8.
- **Divergências na validação cruzada**
  - Revise os valores e padronize os textos nas planilhas de entrada.

---
