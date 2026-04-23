# Marina automations - loans/LoanInterestPosting.py (Módulo Lançamento de Juros de Empréstimos)

Este módulo automatiza a geração dos lançamentos contábeis referentes aos rendimentos de empréstimos, processando dados de planilhas e gerando arquivos prontos para importação no sistema Protheus. O objetivo é garantir padronização, rastreabilidade e agilidade no fechamento contábil dos rendimentos de empréstimos.

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

O script `LoanInterestPosting.py` centraliza o processamento dos rendimentos de empréstimos, realizando:
- Leitura e validação dos dados de rendimentos;
- Padronização e tratamento dos dados;
- Mapeamento de planos, perfis e contas contábeis;
- Geração dos lançamentos de débito e crédito conforme regras contábeis;
- Exportação do arquivo pronto para importação no Protheus.

Ideal para equipes de contabilidade e TI que buscam automação, rastreabilidade e redução de erros manuais no lançamento de rendimentos de empréstimos.

---

## Pré-requisitos
- **Python**: 3.8 ou superior
- **Bibliotecas Python**:
  - pandas
- **Instalação das dependências**:

```powershell
pip install pandas
```
- **Estrutura de diretórios**: conforme o projeto (veja abaixo)

---

## Configurações
- **Data de referência**: Definida diretamente no script (`date = "2026-01-01"`).
- **Nomes dos arquivos**: Gerados automaticamente a partir da data.
- **Mapeamentos**: Planos, perfis e contas definidos em dicionários internos.
- **Personalização**: Para adaptar a outros contextos, ajuste os dicionários de mapeamento e caminhos conforme necessário.

---

## Estrutura do Projeto
```
data_preprocessing/

├── Documents/
│   └── Consultas/
│       └── Rendimentos_01.2026.xlsx   ← Arquivo de entrada com os dados de rendimentos

└── loans/
    ├── LoanInterestPosting.py         ← Script principal responsável pelo processamento dos rendimentos de empréstimos
    │
    └── Documents/
        └── Rendimentos/
            └── rendimentoEmprestimos_protheus01-01.csv  ← Arquivo de saída com os lançamentos formatados para o Protheus
```

---

## Fluxo Completo de Execução

### Etapa 1 — Leitura do Arquivo de Rendimentos  
**Arquivo:** `LoanInterestPosting.py`  
**Função:** (bloco principal)
- Busca o arquivo Excel de rendimentos na pasta `Documents/Consultas/`.
- Valida a existência do arquivo e da data de referência.
- Exemplo de arquivo: `Rendimentos_01.2026.xlsx`

---

### Etapa 2 — Tratamento dos Dados  
**Arquivo:** `LoanInterestPosting.py`  
**Função:** (bloco principal)
- Ajusta tipos, remove espaços e filtra apenas as colunas necessárias.
- Exemplo de colunas tratadas: `Plano`, `Perfil`, `Valor do rendimento`, etc.

---

### Etapa 3 — Mapeamento de Planos e Perfis  
**Arquivo:** `LoanInterestPosting.py`  
**Função:** (bloco principal)
- Converte nomes de planos e perfis em códigos conforme os dicionários internos.
- Exemplo de mapeamento:
  - PREVISÃO → 51
  - VISÃO MULTI → 8
  - TELEFÔNICA BD → 22

---

### Etapa 4 — Geração dos Lançamentos Contábeis  
**Arquivo:** `LoanInterestPosting.py`  
**Função:** (bloco principal)
- Para cada rendimento, gera lançamentos de débito e crédito, considerando regras para valores negativos.
- Exemplo: Valor negativo inverte as contas de débito e crédito.

---

### Etapa 5 — Montagem do DataFrame Final  
**Arquivo:** `LoanInterestPosting.py`  
**Função:** (bloco principal)
- Organiza as colunas na ordem exigida pelo sistema contábil.
- Exemplo de colunas finais: `Data`, `Plano`, `Perfil`, `Conta Débito`, `Conta Crédito`, `Valor`, etc.

---

### Etapa 6 — Exportação do Arquivo  
**Arquivo:** `LoanInterestPosting.py`  
**Função:** (bloco principal)
- Salva o resultado em CSV, sem cabeçalho, separado por ponto e vírgula, em `Documents/Rendimentos/`.
- Exemplo de nome: `rendimentoEmprestimos_protheus01-01.csv`

---

## Detalhamento dos Módulos
- **LoanInterestPosting.py**: Script principal, responsável por todo o fluxo descrito acima.
- **Funções principais**: Leitura, tratamento, mapeamento, geração de lançamentos e exportação.
- **Dicionários de mapeamento**: Definem a lógica de conversão de nomes para códigos e contas contábeis.

---

## Arquivos de Entrada e Saída

### Entrada
- **Rendimentos_01.2026.xlsx** (em `Documents/Consultas/`):
  - Deve conter colunas como: `Plano`, `Perfil`, `Valor do rendimento`, etc.
    - Exemplo de linha:

    | Plano     | Perfil | Valor do rendimento |
    |-----------|--------|---------------------|
    | PREVISÃO  | 01     | 1500.00             |

### Saída
- **rendimentoEmprestimos_protheus01-01.csv** (em `Documents/Rendimentos/`):
  - Arquivo pronto para importação no Protheus.
  - Colunas típicas: `Data`, `Plano`, `Perfil`, `Conta Débito`, `Conta Crédito`, `Valor`, etc.

---

## Mapeamentos e Configuração
- **Planos:**
  - PREVISÃO: 51
  - VISÃO MULTI: 8
  - VISÃO TELEFÔNICA: 49
  - TELEFÔNICA BD: 22
- **Perfis:**
  - Definidos em dicionários aninhados, convertendo nomes em códigos conforme o plano.
- **Contas contábeis:**
  - Débito padrão: 10203080101010
  - Crédito padrão: 50108010100000
  - Para valores negativos, as contas são invertidas.
- **Personalização:**
  - Para adaptar a outros contextos, ajuste os dicionários de mapeamento e as regras de geração de lançamentos.

---

## Execução
1. Certifique-se de que o arquivo de entrada está no local correto e com o nome esperado.
2. Execute o script:
   ```powershell
   python loans/LoanInterestPosting.py
   ```
3. O arquivo de saída será gerado automaticamente na pasta `Documents/Rendimentos/`.

---

## FAQ e Troubleshooting
- **Erro: Arquivo não encontrado**
  - Verifique se o arquivo de entrada está no caminho correto e com o nome esperado.
- **Erro de coluna ausente**
  - Confirme se o arquivo de entrada possui todas as colunas obrigatórias.
- **Arquivo de saída vazio**
  - Certifique-se de que há registros para a data de referência definida.
- **Problemas de encoding**
  - Salve os arquivos Excel em UTF-8 ou padrão Excel.
- **Divergências nos lançamentos**
  - Revise os mapeamentos de planos, perfis e contas contábeis.

---

## Contato/Suporte
Para dúvidas, sugestões ou problemas, entre em contato com a equipe de desenvolvimento ou responsável pelo projeto Marina automations.

---

