# 📊 Manual Completo do Processo de Geração de Relatórios de Investimentos

## 📋 Índice
1. [Visão Geral](#visao-geral)
2. [Propósito do Sistema](#propósito-do-sistema)
3. [Fluxo Geral do Processo](#fluxo-geral-do-processo)
4. [Estrutura do Código](#estrutura-do-código)
5. [Dependências](#dependências)
6. [Entradas e Saídas](#entradas-e-saídas)
7. [Guia Passo a Passo](#guia-passo-a-passo)
8. [Exemplos Práticos](#exemplos-práticos)
9. [Pontos de Atenção](#pontos-de-atenção)
10. [Melhorias Futuras](#melhorias-futuras)
11. [11. Explicação em linguagem não técnica](#explicação-em-linguagem-nao-tecnica)
---

## 🎯 Visão Geral

### Propósito do Sistema

O sistema de investimentos é uma solução de automação contábil para:

- **Processar dados de carteiras de investimento** de fundos de investimento
- **Gerar relatórios contábeis** em formato Excel com movimentações segregadas
- **Criar lançamentos contábeis** (débito/crédito) para o sistema Protheus
- **Calcular rendimentos** de investimentos com base em entradas, saídas e variações
- **Registrar taxas e provisões** de custodia, CETIP, liquidação financeira, etc.
- **Conciliar saldos** entre datas consecutivas de carteira

### Problema Contábil Resolvido

A gestão manual de investimentos em planos de previdência é complexa por envolver:
- Múltiplos fundos de diferentes classes (Renda Fixa, Ações, Exterior, Multimercado)
- Diversos planos e perfis de risco com regras contábeis específicas
- Entradas, saídas e rendimentos que precisam ser segregados
- Taxas administrativas, de custodia e liquidação que impactam o resultado
- Sincronização com o sistema contábil (Protheus)

Este sistema **automatiza completamente** esse processo, garantindo precisão e conformidade.

---

## 🔄 Fluxo Geral do Processo

```
┌─────────────────────────────────────────────────────────────────┐
│                    INÍCIO DO PROCESSAMENTO                      │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────┐
        │  1. LEITURA DOS ARQUIVOS DE ENTRADA  │
        │  - Carteiras (Excel)                 │
        │  - Demonstrativos de Caixa (Excel)   │
        │  - Despesas (Excel)  -REMOVER        │
        │  - Consulta de Fundos (Excel)        │
        └──────────────────────┬───────────────┘
                               │
                               ▼
        ┌──────────────────────────────────────┐
        │  2. TRANSFORMAÇÃO DOS DADOS          │
        │  - Padronização de colunas           │
        │  - Conversão de tipos                │
        │  - Limpeza de dados nulos            │
        └──────────────────────┬───────────────┘
                               │
                               ▼
        ┌──────────────────────────────────────┐
        │  3. SEGREGAÇÃO DE OPERAÇÕES          │
        │  - Resgates e Aquisições             │
        │  - Despesas e Taxas                  │
        │  - Rendimentos                       │
        └──────────────────────┬───────────────┘
                               │
                               ▼
        ┌──────────────────────────────────────┐
        │  4. CÁLCULO DE RENDIMENTOS           │
        │  - Comparação com saldo anterior     │
        │  - Descontando entradas e saídas     │
        │  - Identificando ganhos/perdas       │ -Identificação de rentabilidade pos./neg.
        └──────────────────────┬───────────────┘
                               │
                               ▼
        ┌──────────────────────────────────────┐
        │  5. GERAÇÃO LANÇAMENTOS CONTÁBEIS    │
        │  - Débitos e Créditos                │
        │  - Associação de contas cantábeis por tipo de operação │
        │  - Vinculação a planos/perfis        │
        └──────────────────────┬───────────────┘
                               │
                               ▼
        ┌──────────────────────────────────────┐
        │  6. EXPORTAÇÃO DOS RESULTADOS        │
        │  - Excel com lançamentos de aplicação resgate/rendimento         │
        │  - CSV para importação Protheus      │
        │  - Relatório de Evolução Patrimonial            │
        └──────────────────────┬───────────────┘
                               │
                               ▼
        ┌──────────────────────────────────────┐
        │         FIM DO PROCESSAMENTO         │
        └──────────────────────────────────────┘
```

---

## 🏗️ Estrutura do Código

### Organização de Diretórios

```
investimentos_process.py (887 linhas)
├── 📍 Dicionários de Configuração
│   ├── fundos_dict - Mapeamento de CNPJs para nomes de fundos
│   ├── planilhas_info - Carteiras com planos e perfis
│   ├── provisao_dict - Códigos de provisão
│   ├── taxas_demonstrativo - Tipos de taxas
│   └── contaPagarReceber - Mapeamento contábil de contas
│
├── 🔧 Funções Utilitárias
│   ├── extrair_valor() - Extração de valores do texto
│   ├── substituir_nome() - Normalização de nomes
│   └── ordenar_coluna() - Ordenação de DataFrames
│
├── 📊 Funções de Transformação
│   ├── prepararDemonstrativos() - Leitura e estruturação de demonstrativos
│   ├── prepararCarteiras() - Leitura e estruturação de carteiras
│   ├── prepararDespesas() - Leitura e estruturação de despesas
│   └── mapear_classificacoes() - Mapeamento de classificações CVM
│
├── 💹 Funções de Cálculo
│   ├── pesquisar_dados_por_data() - Busca de movimentações por data
│   ├── levantar_entrada_saida() - Levantamento de fluxo de caixa
│   ├── somar_entrada_saida() - Consolidação de valores
│   └── criar_rendimentos() - Cálculo de rendimentos
│
├── 📝 Funções de Contabilidade
│   ├── criar_lancamento_contabil() - Criação de lançamentos (D/C)
│   ├── processar_lancamento_contabil() - Processamento de rendimentos
│   ├── processar_taxa() - Processamento de taxas
│   └── despesas_taxas_demonstrativo() - Tratamento de despesas especiais
│
├── 🔍 Funções de Filtro
│   ├── filtrar_resgates_aquisicoes_despesas() - Segregação de operações
│   ├── procurar_palavra() - Busca por palavra-chave
│   └── filtrar_dados() - Filtro por lista de palavras
│
└── 🚀 Função Principal
    └── main() - Orquestração do processo completo
```

---

## 📦 Dependências

| Biblioteca | Versão | Utilidade |
|-----------|--------|----------|
| `pandas` | ≥1.0 | Manipulação de dados em DataFrames |
| `openpyxl` | ≥3.0 | Leitura/escrita de arquivos Excel (.xlsx) |
| `os` | Built-in | Operações do sistema de arquivos |
| `datetime` | Built-in | Manipulação de datas |
| `re` | Built-in | Expressões regulares |
| `math` | Built-in | Operações matemáticas |

### Instalação de Dependências

```bash
pip install pandas openpyxl
```

---

## 📥📤 Entradas e Saídas

### 📥 Dados de Entrada

O sistema lê dados de múltiplas fontes:

#### 1. **Carteiras** (Excel - diariamente)
- **Localização**: `~/Documentos/Carteiras/{dia}_{mes}/`
- **Padrão de nome**: `{codigo_carteira}_carteira.xlsx`
- **Colunas lidas**: 
  - Coluna A: Código do Fundo
  - Coluna B: Nome do Fundo
  - Coluna H: Valor Atual
- **Processamento**: Linhas até "Total"
- **Exemplo**:
```
Cod Fundo | Fundo | ... | Valor Atual
010134    | BRADESCO BD | ... | 1,500,000.00
```

#### 2. **Demonstrativos** (Excel - diariamente)
- **Localização**: `~/Documentos/demonstrativos/`
- **Padrão de nome**: `{codigo_carteira}_demonstrativo.xlsx`
- **Colunas lidas**: A:D
- **Cabeçalho**: Linha 8 (skiprows=8)
- **Colunas**: Data | Histórico | Entrada | Saída
- **Exemplo**:
```
Data | Histórico | Entrada | Saída
31/01/2025 | Aquisição de Cotas [BRAD FI RF MIRANTE] | 50,000.00 | -
```

#### 3. **Despesas/Provisões** (Excel - mensalmente)
- **Localização**: `~/Documentos/Carteiras/{dia}_{mes}/`
- **Padrão de nome**: `{codigo_carteira}_despesas.xlsx`
- **Filtro**: Entre "Descrição" e "TOTAL"
- **Colunas**: Descrição | Valor
- **Exemplo**:
```
Descrição | Valor
Taxa de Custodia | 5,000.00
Resgate do [FUNDO] | -10,000.00
```

#### 4. **Consulta de Fundos** (Excel - referência)
- **Localização**: `~/Documentos/consulta_fundo.xlsx`
- **Aba**: "para"
- **Colunas necessárias**:
  - Nome do Fundo
  - Classificacao CVM
  - Rentabilidade Positiva (conta contábil)
  - Rentabilidade Negativa (conta contábil)
  - Custo Atualizado (conta contábil)
  - Investimentos (conta contábil)
  - Aplicacao (conta contábil)
  - Resgate (conta contábil)
  - Plano
  - Perfil

### 📤 Dados de Saída

O sistema gera 4 arquivos principais:

#### 1. **Lançamentos Segregados** (Excel)
- **Arquivo**: `lancamentos_segregado{dia}-{mes}.xlsx`
- **Abas**:
  - `Despesas_{dia}_{mes}_{ano}` - IOF, Taxas
  - `Rentabilidade_{dia}_{mes}_{ano}` - Ganhos/Perdas
  - `Aplicacao_{dia}_{mes}_{ano}` - Aportes
  - `Resgate_{dia}_{mes}_{ano}` - Resgates
- **Colunas**:
  ```
  Conta contabil | Valor | D/C | Historico | CC | Plano | Perfil
  ```

#### 2. **Evolução Patrimonial** (Excel)
- **Arquivo**: `evolucao_patrimonial{dia}-{mes}.xlsx`
- **Colunas**:
  ```
  Fundo | Plano | Perfil | Classificacao | 
  Saldo Anterior | Entrada | Saida | Saldo Atual | Rendimento
  ```
- **Propósito**: Demonstrativo de variação do patrimônio

#### 3. **Lançamentos Protheus** (CSV)
- **Arquivo**: `lancamentos_protheus{dia}-{mes}.csv`
- **Separador**: `;` (ponto-e-vírgula)
- **Colunas**:
  ```
  Conta contabil;Valor;D/C;Historico;CC;Plano;Perfil
  ```
- **Propósito**: Importação direto no ERP Protheus

#### 4. **Relatório de Provisão** (Excel - opcional)
- **Arquivo**: `relatorio_provisao_{dia_ant}-{mes_ant}.xlsx`
- **Gerado apenas em**: Não mencionado (condicional)
- **Colunas**:
  ```
  Plano | Perfil | Dia | Total liquido | Total contas a receber | Total
  ```

---

## 🔍 Guia Passo a Passo

### **ETAPA 1: Leitura e Preparação dos Dados**

#### Passo 1.1: Preparar Demonstrativos

```python
def prepararDemonstrativos(info, path_demonstrativo, data_demonstrativo, titulos_demonstrativo):
    """
    Lê os arquivos de demonstrativo de um determinado dia
    
    Parâmetros:
    - info: Tupla (codigo_carteira, nome_sheet, plano, perfil)
    - path_demonstrativo: Lista de arquivos em ~/Documentos/demonstrativos/
    - data_demonstrativo: Data formatada (ex: "31/01/2025")
    - titulos_demonstrativo: ['Data', 'Historico', 'Entrada', 'Saida']
    
    Retorna:
    - DataFrame com colunas: Historico, Entrada, Saida, Plano, Perfil, Data
    """
```

**O que acontece aqui:**
1. Procura arquivo com `codigo_carteira` no nome (ex: "010134_demonstrativo.xlsx")
2. Lê linhas 8+ (pulando cabeçalho)
3. Extrai colunas A:D
4. Adiciona plano, perfil e data
5. Filtra apenas dados da data processada usando `pesquisar_dados_por_data()`

**Resultado esperado:**
```
Historico                              | Entrada | Saida | Plano | Perfil | Data
Fundo BRAD FI RF MIRANTE               | 50000   | -     | 22    | 3      | 31/01/2025
Taxa de Custodia                       | -       | 100   | 22    | 3      | 31/01/2025
Aquisicao de Cotas                     | 25000   | -     | 22    | 3      | 31/01/2025
```

#### Passo 1.2: Preparar Carteiras (Atual e Anterior)

```python
def prepararCarteiras(info, path, arquivos_carteira, titulos_carteira):
    """
    Lê a posição atual de fundos em cada carteira
    
    Retorna:
    - DataFrame com: Cod Fundo, Fundo, Valor Atual, Plano, Perfil
    """
```

**O que acontece:**
1. Lê arquivo de carteira (skiprows=11)
2. Extrai colunas: A (Cod Fundo), B (Fundo), H (Valor Atual)
3. Remove linhas até "Total"
4. Adiciona Plano e Perfil

**Processa:**
- Carteira atual (data = 31/01/2025)
- Carteira anterior (data = 30/01/2025)

**Resultado esperado:**
```
Cod Fundo | Fundo | Valor Atual | Plano | Perfil
010134    | BRADESCO BD | 1,500,000.00 | 22 | 3
...
```

#### Passo 1.3: Preparar Despesas

```python
def prepararDespesas(info, path, arquivos_despesas):
    """
    Lê as despesas e provisões da carteira
    
    Retorna:
    - DataFrame com: Despesa, Valor, Plano, Perfil
    """
```

**O que acontece:**
1. Lê arquivo de carteira (procura pelas despesas no rodapé)
2. Filtra entre "Descrição" e "TOTAL"
3. Extrai nome da despesa e valor
4. Adiciona Plano e Perfil

---

### **ETAPA 2: Transformação e Normalização**

#### Passo 2.1: Substituição de Nomes

```python
demonstrativos = substituir_nome(demonstrativos, 'Historico', 
                                 'FIC DE FI AÇÕES IBRX', 
                                 'FIC DE FI ACOES IBRX')
```

**Normaliza inconsistências nos nomes dos fundos:**
- Acentuação inconsistente
- Variações de escrita
- Padrão esperado vs. arquivo

**Exemplos de substituições:**
| Original | Normalizado |
|----------|------------|
| LIQUIDAÃ‡ÃƒO FINANCEIRA | LIQUIDACAO FINANCEIRA |
| Aquisição de Cotas | Aquisicao de Cotas |
| ALTERNA MIRANTE FICM | ALTERNATIVOS MIR FIM |

#### Passo 2.2: Levantamento de Entrada/Saída

```python
demonstrativos = levantar_entrada_saida(demonstrativos, taxas_demonstrativo)
```

**Processa:**
1. Identifica se cada linha é uma TAXA ou movimentação de fundo
2. Cria chave composta: `{fundo}_{plano}_{perfil}_{'Pos'|'Neg'}`
3. Agrupa movimentações similares
4. Consolida valores

**Exemplo:**
```
Antes:
| Historico | Entrada | Saida | Plano | Perfil |
| BRAD FI RF MIRANTE | 50000 | 0 | 22 | 3 |
| BRAD FI RF MIRANTE | 0 | 100 | 22 | 3 |

Depois (consolidado):
| Historico | Entrada | Saida | Plano | Perfil |
| BRAD FI RF MIRANTE | 50000 | 100 | 22 | 3 |
```

#### Passo 2.3: Somar Entrada/Saída

```python
entrada_saida_rendimento = somar_entrada_saida(demonstrativos)
```

**Consolida completamente:**
- Se há entrada E saída no mesmo fundo → calcula líquido
- Agrupa por `{fundo}_{plano}_{perfil}`
- Resultado: 1 linha por fundo/plano/perfil

---

### **ETAPA 3: Segregação de Operações**

#### Passo 3.1: Separar Resgates, Aquisições e Despesas

```python
linhas_aquis_resg, demonstrativos, linhas_desp_demonstrativo = \
    filtrar_resgates_aquisicoes_despesas(demonstrativos, taxas_demonstrativo)
```

**Resultado: 3 DataFrames diferentes**

| Tipo | Contém | Contabilização |
|------|--------|----------------|
| `linhas_aquis_resg` | Aquisição/Resgate de Cotas | Aplicação/Resgate no Fundo |
| `linhas_desp_demonstrativo` | Taxas e Provisões | Despesa vs. Conta a Pagar |
| `demonstrativos` | Tudo o resto | Invertido para cálculo |

**Exemplo:**
```
Entrada original:
| Historico | Entrada | Saida |
| Aquisicao de Cotas | 50000 | 0 |
| Taxa CETIP | 0 | 150 |
| Fundo ABC | 100 | 0 |

Resultado:
linhas_aquis_resg:
| Aquisicao de Cotas | 50000 | 0 |

linhas_desp_demonstrativo:
| Taxa CETIP | 0 | 150 |

demonstrativos:
| Fundo ABC | 100 | 0 |
```

#### Passo 3.2: Mapear Classificações CVM

```python
carteira_atual = mapear_classificacoes(carteira_atual, df_fundos)
```

**Adiciona coluna de classificação CVM:**
- Consulta `consulta_fundo.xlsx`
- Busca por `Cod Fundo` (normalizado para 6 dígitos)
- Retorna `Classificacao CVM`

**Classificações possíveis:**
- FUNDO INVESTIMENTO RENDA FIXA
- FUNDO INVESTIMENTO ACOES
- FUNDO INVESTIMENTO EXTERIOR
- MULTIMERCADO ESTRUTURADO
- FUNDO INVESTIMENTO DIREITOS CREDITORIOS

---

### **ETAPA 4: Cálculo de Rendimentos**

#### Passo 4.1: Criar Matriz de Rendimentos

```python
rendimento = criar_rendimentos(carteira_atual, carteira_anterior, entrada_saida_rendimento)
```

**Fórmula:**
```
Rendimento = Saldo Atual - Saldo Anterior - Entrada - Saída
```

**Passo a passo:**
1. Busca Saldo Anterior (carteira dia anterior)
2. Busca Entrada/Saída (demonstrativo do dia)
3. Calcula: `1.500.000 - 1.400.000 - 50.000 - 0 = 50.000`
4. Resultado: Rendimento positivo de 50.000

**Resultado esperado:**
```
| Fundo | Plano | Perfil | Classificacao | Saldo Anterior | Entrada | Saida | Saldo Atual | Rendimento |
| BRAD FI RF MIRANTE | 22 | 3 | FIRF | 1.400.000 | 50.000 | 0 | 1.500.000 | 50.000 |
| ICATU MIRANTE | 22 | 3 | FIRF | 800.000 | -25.000 | 0 | 770.000 | -5.000 |
```

---

### **ETAPA 5: Geração de Lançamentos Contábeis**

#### Passo 5.1: Lançamentos de Rentabilidade

```python
df_rentabilidade = processar_lancamento_contabil(rendimento, demonstrativos, df_fundos)
```

**Cria 2 lançamentos por rendimento:**

**Se Rendimento > 0 (Ganho):**
```
DÉBITO:   Custo Atualizado
CRÉDITO:  Rentabilidade Positiva
```

**Se Rendimento < 0 (Perda):**
```
DÉBITO:   Rentabilidade Negativa
CRÉDITO:  Custo Atualizado
```

**Exemplo de saída:**
```
| Conta contabil | Valor | D/C | Historico de lancamento | CC | Plano | Perfil |
| 11203010101 | 50.000,00 | D | Rent. positiva BRAD FI RF MIRANTE | 2 | 22 | 3 |
| 51301010105 | 50.000,00 | C | Rent. positiva BRAD FI RF MIRANTE | 2 | 22 | 3 |
```

#### Passo 5.2: Lançamentos de Resgates/Aquisições

```python
# Busca em linhas_aquis_resg
```

**Estrutura:**

**Para Aquisição (Aplicação no Fundo):**
```
DÉBITO:   Investimentos (carteira geral)
CRÉDITO:  Aplicação (do fundo específico)
```

**Para Resgate:**
```
DÉBITO:   Resgate (do fundo específico)
CRÉDITO:  Investimentos (carteira geral)
```

#### Passo 5.3: Lançamentos de Taxas/Provisões

```python
df_resultado_taxas = despesas_taxas_demonstrativo(linhas_desp_demonstrativo, df_fundos, taxas_demonstrativo)
```

**Processa 5 tipos de taxa:**

| Taxa | Regra |
|------|-------|
| Taxa CUSTODIA | Despesa: 50298990100000 |
| Taxa CETIP | Despesa: 50298990300000 |
| Tarifa de liquidação | Despesa: 50298999900000 |
| Tx de Controladoria | Despesa: 50298990200000 |
| Despesa SELIC | Despesa: 50298990300000 |

**Conta a Pagar (Plano Normal):**
```
Débito: Conta de Despesa
Crédito: 20103100101000 (CP - Plano) ou 20103100102000 (CP - PGA)
```

---

### **ETAPA 6: Agregação e Exportação**

#### Passo 6.1: Concatenar Todos os Lançamentos

```python
df_protheus = pd.concat([df_resultado_taxas, df_rentabilidade, df_resultado_provisao], 
                         axis=0, ignore_index=True)
```

**Consolida todos os lançamentos em 1 DataFrame:**
- Lançamentos de taxas
- Lançamentos de rendimento
- Lançamentos de provisão (condicional)

**Total de linhas:** (Rendimentos × 2) + (Taxas × 2) + (Resgates/Aquisições × 2)

#### Passo 6.2: Criar Filtros por Tipo

```python
df_aplic = procurar_palavra(df_protheus, 'Historico de lancamento', 'Aplic. no')
df_resg = procurar_palavra(df_protheus, 'Historico de lancamento', 'Resg. no')
filtro_rent = filtrar_dados(df_protheus, ['Rent. positiva', 'Rent. negativa'])
filtro_desp = filtrar_dados(df_protheus, taxas_demonstrativo)
```

**Separa os lançamentos em 4 categorias:**
1. **Aplicações** - Aportes em fundos
2. **Resgates** - Saques de fundos
3. **Rentabilidade** - Ganhos/Perdas
4. **Despesas** - Taxas e custos

#### Passo 6.3: Exportar em Excel (Segregado)

```python
with pd.ExcelWriter(path_lancamentos_segregado) as writer:
    filtro_desp.to_excel(writer, sheet_name=f'Despesas_{dia}_{mes}_{ano}', index=False)
    filtro_rent.to_excel(writer, sheet_name=f'Rentabilidade_{dia}_{mes}_{ano}', index=False)
    df_aplic.to_excel(writer, sheet_name=f'Aplicacao_{dia}_{mes}_{ano}', index=False)
    df_resg.to_excel(writer, sheet_name=f'Resgate_{dia}_{mes}_{ano}', index=False)
```

**Arquivo**: `lancamentos_segregado31-01.xlsx`

#### Passo 6.4: Exportar Evolução Patrimonial

```python
rendimento.to_excel(path_evolucao_patrimonial, index=False)
```

**Arquivo**: `evolucao_patrimonial31-01.xlsx`

**Contém:**
- Posição de cada fundo
- Variação de um dia para outro
- Rendimento obtido

#### Passo 6.5: Exportar para Protheus (CSV)

```python
df_protheus.to_csv(path_lancamentos_protheus, header=None, index=False, sep=';')
```

**Arquivo**: `lancamentos_protheus31-01.csv`

**Formato:**
```
11203010101;50000;D;Rent. positiva BRAD FI RF MIRANTE;2;22;3
51301010105;50000;C;Rent. positiva BRAD FI RF MIRANTE;2;22;3
...
```

---

## 💡 Exemplos Práticos

### Exemplo 1: Processamento de um Aporte

**Cenário:** Um investidor faz aporte de R$ 100.000 no fundo BRAD FI RF MIRANTE, plano 22, perfil 3.

**Dados de Entrada:**
- Demonstrativo: `Aquisicao de Cotas [BRAD FI RF MIRANTE] | 100.000 | 0`
- Saldo anterior: R$ 1.000.000
- Saldo atual: R$ 1.100.000

**Processamento:**

1. **Extração:**
   ```
   Historico: BRAD FI RF MIRANTE
   Entrada: 100.000
   Saida: 0
   Plano: 22
   Perfil: 3
   ```

2. **Segregação:** Identifica como "Aquisicao de Cotas"

3. **Rendimento:**
   ```
   Rendimento = 1.100.000 - 1.000.000 - 100.000 - 0 = 0
   (Sem rendimento, apenas aporte)
   ```

4. **Lançamentos Gerados:**
   ```
   1ª Linha (Aplicação):
   | 20103100101000 | 100.000 | D | Resg. no BRAD FI RF MIRANTE | 2 | 22 | 3 |
   
   2ª Linha (Resgate/Aplicação):
   | 31901040101000 | 100.000 | C | Resg. no BRAD FI RF MIRANTE | 2 | 22 | 3 |
   ```

---

### Exemplo 2: Processamento de Rendimento Positivo

**Cenário:** Fundo rende R$ 5.000 em um dia.

**Dados de Entrada:**
- Saldo anterior: R$ 1.000.000
- Saldo atual: R$ 1.005.000
- Entrada/Saída: R$ 0

**Processamento:**

1. **Cálculo:**
   ```
   Rendimento = 1.005.000 - 1.000.000 - 0 - 0 = 5.000
   ```

2. **Lançamentos Gerados (Ganho):**
   ```
   1ª Linha (Débito - Custo):
   | 11203010101 | 5.000 | D | Rent. positiva BRAD FI RF MIRANTE | 2 | 22 | 3 |
   
   2ª Linha (Crédito - Rentabilidade):
   | 51301010105 | 5.000 | C | Rent. positiva BRAD FI RF MIRANTE | 2 | 22 | 3 |
   ```

---

### Exemplo 3: Processamento de Taxa de Custodia

**Cenário:** Taxa de custodia de R$ 150 é debitada do fundo.

**Dados de Entrada:**
- Demonstrativo: `Taxa CUSTODIA | 0 | 150`
- Plano: 22, Perfil: 3 (não é PGA)

**Processamento:**

1. **Identificação:**
   ```
   Fundo: Taxa CUSTODIA
   Entrada: 0
   Saida: 150
   ```

2. **Lançamentos Gerados:**
   ```
   1ª Linha (Despesa - Débito):
   | 50298990100000 | 150 | D | Taxa CUSTODIA | 2 | 22 | 3 |
   
   2ª Linha (CP - Crédito - Plano Normal):
   | 20103100101000 | 150 | C | Taxa CUSTODIA | 2 | 22 | 3 |
   ```

---

### Exemplo 4: PGA (Plano/Perfil 987/19)

**Cenário:** Mesmo cenário, mas plano 987, perfil 19 (PGA)

**Processamento:**

**Diferença:** A conta de CP muda para PGA:
```
1ª Linha (Despesa - Débito):
| 50298990100000 | 150 | D | Taxa CUSTODIA | 2 | 987 | 19 |

2ª Linha (CP - Crédito - PGA):
| 20103100102000 | 150 | C | Taxa CUSTODIA | 2 | 987 | 19 |
                                             ↑
                                    102000 em vez de 101000
```

---

## ⚠️ Pontos de Atenção

### 1. **Consistência de Datas**

**Problema:** Arquivos com datas inconsistentes podem não ser processados.

**Solução:**
```python
data = '2025-01-31'  # YYYY-MM-DD OBRIGATORIAMENTE
data_ant = '2025-01-30'  # Dia anterior obrigatório
```

**Verificar:**
- Ambos os diretórios devem existir
- `~/Documentos/Carteiras/31_01/` e `~/Documentos/Carteiras/30_01/`

---

### 2. **Codificação de Fundos**

**Problema:** Fundos não encontrados na consulta.

**Verificações:**
```python
# fundos_dict deve conter todos os CNPJs esperados
'36518029000107': {'fundo': 'WESTERN MIRAN FIRFCP', ...}

# Verificar se o nome no demonstrativo bate com a consulta
```

**Ação:**
- Atualizar `fundos_dict` se houver novo fundo
- Verificar capitalização e acentuação

---

### 3. **Mapeamento de Contas Contábeis**

**Problema:** Lançamentos com contas inválidas.

**Verificar:**
```python
contaPagarReceber = {
    'Taxa CUSTODIA': {'Plano': 20103100101000, ...}
}
```

**Se taxa não está mapeada:**
- Adicionar em `contaPagarReceber`
- Consultar plano de contas

---

### 4. **Valores Nulos ou Inválidos**

**Problemas comuns:**
- Valores que não são numéricos
- DataFrames vazios (sem dados no período)
- Fundos sem correspondência entre carteiras

**Tratamento:**
```python
df_despesas['Valor'] = pd.to_numeric(df_despesas['Valor'], errors='coerce')
# errors='coerce' converte inválidos para NaN

df = df.dropna(thresh=df.shape[1] - 2 + 1)
# Remove linhas com muitos NaNs
```

---

### 5. **Performance com Grandes Volumes**

**Limitações:**
- Processar mais de 5.000 movimentações pode ser lento
- Concatenação de muitos DataFrames é custosa

**Otimizações:**
```python
# Evitar múltiplas concatenações
df_list = []
for ... in ...:
    df_list.append(df)
result = pd.concat(df_list, ignore_index=True)
```

---

### 6. **Planos Especiais (PGA e MAIS VISÃO)**

**Regra especial:**
```python
if (plano, perfil) == (987, 19) or (plano, perfil) == (952, 20):
    # Usa conta PGA em vez de Plano normal
    lancamento2 = criar_lancamento_contabil(..., contaPagarReceber[taxa]['PGA'], ...)
```

**Validar:**
- PGA: Plano 987, Perfil 19
- MAIS VISÃO PGA: Plano 952, Perfil 20

---

### 7. **Exclusão de "Resgate do" nas Despesas

```python
df_despesas = df_despesas.loc[~df_despesas['Despesa'].str.contains('Resgate do', case=False, na=False)]
```

**Por quê?**
- "Resgate do [FUNDO]" é provisão, não despesa
- Será processado separadamente em `provisao_retiradas`

---

## 🚀 Melhorias Futuras

### 1. **Adição de Logs Estruturados**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'processamento_{data}.log'),
        logging.StreamHandler()
    ]
)
```

**Benefícios:**
- Rastreabilidade de processamento
- Detecção de erros
- Auditoria

---

### 2. **Validação de Integridade**

```python
def validar_integridade():
    """
    - Verificar se DataFrames vazios
    - Validar somas (débito = crédito)
    - Confirmar existência de arquivos
    - Validar contas contábeis
    """
```

---

### 3. **Tratamento de Erros Robusto**

```python
try:
    main()
except Exception as e:
    logging.error(f"Erro crítico: {e}")
    enviar_alerta_email(e)
finally:
    limpar_arquivos_temporarios()
```

---

### 4. **Processamento Incremental**

**Atual:** Processa tudo do zero todos os dias
**Proposto:** Carregar últimas 30 dias e processar apenas delta

---

### 5. **Dashboard de Monitoramento**

```python
# Criar dashboard com:
# - Quantidade de lançamentos por tipo
# - Somatório de entradas/saídas
# - Rendimento consolidado
# - Reconciliação com dia anterior
```

---

### 6. **Testes Unitários**

```python
def test_criar_rendimentos():
    # Arrange
    df_carteira_atual = ...
    df_carteira_anterior = ...
    
    # Act
    resultado = criar_rendimentos(...)
    
    # Assert
    assert resultado['Rendimento'].sum() == esperado
```

---

### 7. **Suporte a Múltiplas Moedas**

**Atual:** Assume BRL
**Proposto:** Suportar USD, EUR com conversão automática

---

### 8. **API REST para Consultas**

```python
from flask import Flask

@app.route('/api/rendimento/<fundo>/<data>')
def get_rendimento(fundo, data):
    return jsonify(rendimento_do_dia)
```

---

## 📝 Comentários Sugeridos no Código

### Em `levantar_entrada_saida()`

```python
def levantar_entrada_saida(demonstrativo, taxas_demonstrativo):
    """
    Agrupa movimentações de um mesmo fundo, separando taxas de movimentações normais.
    
    Lógica:
    - Se é TAXA (em taxas_demonstrativo), cria entrada separada com índice único
    - Se não é taxa, agrupa por (fundo, plano, perfil, Pos/Neg)
    - Consolida valores de entrada e saída
    
    Retorna DataFrame com uma linha por fundo/taxa/combinação
    """
```

---

### Em `criar_rendimentos()`

```python
def criar_rendimentos(df_carteira, df_saldo_anterior, demonstrativos_entrada_saida):
    """
    FÓRMULA CRÍTICA:
    Rendimento = Saldo Atual - Saldo Anterior - Entrada - Saída
    
    Entradas/Saídas são de demonstrativo (fluxo do dia)
    Se não há demonstrativo, assume 0 (reinvestimento automático)
    
    Positivo = ganho do dia
    Negativo = perda do dia
    """
```

---

### Em `processar_lancamento_contabil()`

```python
def processar_lancamento_contabil(df_rendimentos, demonstrativos, df_fundos):
    """
    Cria lançamentos D/C por rendimento.
    
    Para GANHO (rendimento > 0):
        D - Custo Atualizado (ativo)
        C - Rentabilidade Positiva (receita)
    
    Para PERDA (rendimento < 0):
        D - Rentabilidade Negativa (despesa)
        C - Custo Atualizado (ativo)
    
    Cada rendimento gera 2 linhas (sempre equilibrado em débito/crédito)
    """
```

---

### Em `despesas_taxas_demonstrativo()`

```python
def despesas_taxas_demonstrativo(df_despesas, df_fundos, taxaDemonstrativo):
    """
    Processamento diferenciado para planos PGA (987/19 e 952/20).
    
    PLANO NORMAL (ex: 22/3):
    D - Investimentos
    C - Conta a Pagar Plano (20103100101000)
    
    PGA (987/19 ou 952/20):
    D - Investimentos
    C - Conta a Pagar PGA (20103100102000)
    
    Isso permite rastreamento separado por tipo de plano na contabilidade
    """
```

---

## 🔗 Referências e Estrutura de Dados

### Estrutura `planilhas_info`
```python
planilhas_info = [
    (codigo_carteira, nome_sheet, plano, perfil),
    ('010134', 'BRADESCO BD', 22, 3),
    ...
]
```

### Estrutura `fundos_dict`
```python
fundos_dict = {
    'CNPJ': {
        'fundo': 'Nome do Fundo',
        'fluxo_caixa': 'Nome reduzido',
        'classe': 'Classificação CVM'
    }
}
```

### Colunas do Demonstrativo
```
Data | Historico | Entrada | Saida | Plano | Perfil
31/01/2025 | BRAD FI RF MIRANTE | 50000 | 0 | 22 | 3
```

### Colunas de Saída (Protheus)
```
Conta contabil | Valor | D/C | Historico | CC | Plano | Perfil
11203010101 | 50000 | D | Rent. positiva | 2 | 22 | 3
```

---

## 📞 Suporte e Dúvidas

### Erros Comuns e Soluções

| Erro | Causa | Solução |
|------|-------|--------|
| FileNotFoundError | Arquivo não existe | Verificar pasta e nome arquivo |
| KeyError: 'Fundo' | Coluna não existe | Validar skiprows e header |
| ValueError: setting with copy | Pandas warning | Usar `.copy()` antes de modificar |
| NaN em Rendimento | Carteira anterior vazia | Garantir carteira dia anterior existe |

---

## 📝 11. Explicação em linguagem não técnica 

### Para Quem Deseja Entender o Sistema sem Conhecimento Especializado

Esta seção apresenta o funcionamento do sistema de forma clara e simples, utilizando conceitos do dia a dia para facilitar a compreensão. Se você não é contador e deseja aprender rapidamente o que esse sistema faz, este é o local apropriado.

---

## O Sistema Explicado de Forma Acessível

### Contexto Introdutório

Imagine que você seja o gerente de um banco responsável por administrar investimentos de diversos clientes. Esses clientes, denominados Planos, investem seu dinheiro em fundos de investimento. Cada um desses clientes pode escolher um nível de risco para seus investimentos, determinando o tipo de retorno esperado.

Os níveis de risco estão assim organizados:

Conservador: apresenta pouco risco de perda, mas também proporciona ganhos menores.

Moderado: representa um nível intermediário, com risco e ganho médios.

Agressivo: possui maior risco de perda, porém oferece potencial de ganhos superiores.

Esses "níveis de risco" são chamados de Perfis no sistema.

---

### Fluxo Diário de Operações

O sistema funciona de maneira estruturada ao longo de cada dia. A seguir, apresentamos as principais etapas:

**Etapa 1: Recebimento de Dados**

O sistema recebe os seguintes arquivos e informações:

- Saldo atual do cliente hoje, 
- Saldo do cliente no dia anterior, 
- Movimentações do período, (ex: depositos no fundo)
- Custos operacionais. (ex: cobranças de taxa.)

Em resumo, o sistema sabe quanto havia antes, quanto foi adicionado, quanto foi cobrado e quanto há agora.

---

**Etapa 2: Cálculo de Resultados**

O sistema realiza um cálculo fundamental para determinar o rendimento do fundo. A questão central é: de onde veio o crescimento no saldo?

A fórmula aplicada é:

Saldo do dia anterior: R$ 1.400.000
Adicionado depósito: R$ 50.000
Subtraído taxa: R$ 100
Resultado esperado: R$ 1.449.900

Saldo real do dia: R$ 1.500.000
Menos resultado esperado: R$ 1.449.900
Diferença: R$ 50.100

Essa diferença de R$ 50.100 representa o ganho do fundo neste dia. Esse valor indica que o dinheiro investido cresceu organicamente por estar aplicado no mercado financeiro.

---

**Etapa 3: Registro Contábil**

Após calcular os valores, o sistema precisa registrá-los em um livro de contabilidade. Este registro é fundamental para manter histórico e conformidade legal.

Os registros são estruturados da seguinte forma:

- Registro de entrada de dinheiro, 
- Registro de saída de dinheiro, 
- Registro de ganho/rendimento.

Cada registro contém informações essenciais:

- De qual conta específica saiu ou entrou o dinheiro, seguindo a estrutura contábil da instituição. 
- O valor exato da movimentação, sendo R$ 50.000, R$ 100, etc. 
- A razão da movimentação: depósito, taxa, rendimento ou outra operação. 
- A identificação do cliente: Plano BRADESCO, Perfil Conservador, ou outra combinação.

---

**Etapa 4: Geração de Relatório**

Ao final do dia, o sistema gera um relatório consolidado com todas as operações:

- Demonstração de aportes: Lista todo o dinheiro que entrou. 
- Demonstração de resgates: Lista todo o dinheiro que saiu (quando aplicável). Se não houve resgates, aparece vazio. 
- Demonstração de ganhos: Lista todos os rendimentos obtidos. 
- Demonstração de custos: Lista todas as taxas cobradas conforme aplicável.

Saldo final consolidado: BRADESCO BD termina o dia com R$ 1.500.000 registrado e verificado.

---

### Comparação: Processo Manual versus Sistema Automático

O que uma pessoa faria manualmente levaria várias horas de trabalho. O sistema realiza todas essas operações automaticamente em segundos.

Passo 1 - Leitura de arquivos: O sistema localiza e abre os quatro arquivos necessários. Extrai as informações relevantes. Valida o formato dos dados.

Passo 2 - Leitura de movimentações: O sistema localiza todos os demonstrativos do dia. Identifica depósitos, resgates e taxas. Organiza essas informações por cliente e perfil.

Passo 3 - Cálculo de valores: O sistema aplica a fórmula de rendimento para cada fundo. Verifica se há inconsistências. Consolida valores por tipo de operação.

Passo 4 - Registro contábil: O sistema prepara os lançamentos de débito e crédito. Associa cada lançamento à conta contábil apropriada. Valida que débitos e créditos estão equilibrados.

Passo 5 - Geração de arquivos: O sistema cria arquivo Excel com abas segregadas. Cria arquivo CSV para importação no Protheus. Valida a integridade dos dados gerados.

Passo 6 - Conclusão: Os arquivos estão prontos para uso. Gerentes consultam os relatórios. Contadores importam os dados no sistema contábil.

---

### Tratamento de Situações Excepcionais

Nem sempre tudo funciona perfeitamente. O sistema possui validações para identificar problemas:

Erro: "Arquivo de carteira não encontrado". Significa que o arquivo de saldo anterior não está no local esperado. Solução: Verificar se o arquivo foi salvo na pasta correta. Colocar o arquivo na pasta e executar novamente.

Erro: "Fundo não reconhecido". Significa que o nome do fundo nos demonstrativos não corresponde ao nome registrado no cadastro. Solução: Verificar se o nome do fundo está correto. Atualizar o cadastro de fundos se necessário.

Erro: "Valor negativo em rendimento". Significa que o fundo perdeu dinheiro neste período. Solução: Isto é esperado em períodos de volatilidade do mercado. O sistema registra corretamente a perda.

Erro: "DataFrame vazio". Significa que não existem movimentações registradas para o período. Solução: Verificar se há dados de entrada. Se não houver movimentações, o dia pode ser ignorado.

---

## GUIA PRÁTICO POR PERFIL DE USUÁRIO

### Gerentes e Diretores

Este perfil tem interesse em questões estratégicas e de resultado. As principais perguntas são:
O sistema gera relatórios automaticamente todos os dias? Resposta: Sim, o processamento é totalmente automático.
Quanto cada cliente ganhou ou perdeu em determinado período? Resposta: Consulte o arquivo "evolucao_patrimonial", que consolida ganhos e perdas.
Quanto foi cobrado em taxas e qual o impacto no resultado? Resposta: O arquivo "lancamentos_segregado" possui aba específica de despesas com todas as taxas.
Para maiores detalhes técnicos, consulte a seção "Entradas e Saídas" deste manual.

---

### Contadores e Analistas de Contabilidade

Este perfil tem interesse em procedimentos contábeis e conformidade. As principais questões são:
Como são estruturados os lançamentos de débito e crédito? Resposta: Consulte a seção "ETAPA 5: Geração de Lançamentos Contábeis".
Quais contas contábeis são utilizadas e como são definidas? Resposta: O mapeamento de contas está documentado na seção "Estrutura do Código", na variável contaPagarReceber.
Como o sistema segregua rendimentos, taxas e resgates? Resposta: A seção "ETAPA 3: Segregação de Operações" detalha o processo completo.

---

### Profissionais de Tecnologia

Este perfil tem interesse em implementação, manutenção e evolução. As principais questões são:
Como o código está organizado e qual é a função de cada módulo? Resposta: Consulte a seção "Estrutura do Código".
Como processar novos tipos de dados ou fundos? Resposta: Consulte a seção "ETAPA 1: Leitura e Preparação dos Dados".
Quais são as dependências externas necessárias? Resposta: Consulte a seção "Dependências".

---

### Usuários do Sistema Protheus

Este perfil tem interesse prático em importação de dados e integração. As principais questões são:
Qual arquivo devo utilizar para importação? Resposta: O arquivo "lancamentos_protheus31-01.csv" contém todos os lançamentos prontos para importação.
Qual é o formato esperado pelos arquivos de entrada? Resposta: Consulte a seção "Entradas e Saídas" para ver exemplos de estrutura.
Como validar se os dados foram importados corretamente? Resposta: Compare totalizadores de débito e crédito. A soma deve estar equilibrada.

---

## FLUXO VISUAL DO MOVIMENTO DE VALORES

O diagrama a seguir ilustra de forma esquemática como os valores se movem através do sistema:

Situação anterior: Banco possui R$ 1.400.000 em BRADESCO BD.

Situação atual: Banco possui R$ 1.500.000 em BRADESCO BD.

A pergunta fundamental: Onde veio esse aumento?

A resposta está dividida em três componentes:

Entrada (Depósito): R$ 50.000. O cliente realizou um aporte de recursos.

Ganho do Fundo (Rendimento): R$ 50.100. O fundo cresceu por estar investido.

Taxa Cobrada (Custo): -R$ 100. O banco cobrou taxa por administração.

Consolidação: A soma de todas as partes resulta no novo saldo de R$ 1.500.000.

Registro: Todas essas operações são registradas no livro de contabilidade usando lançamentos de débito e crédito.

---

## CENÁRIO DO MUNDO CORPORATIVO

Na prática de uma segunda-feira de manhã em uma instituição financeira, o fluxo ocorre assim:

Recebimento de dados: A equipe recebe ou o sistema automaticamente coleta quatro conjuntos de informações: saldo de carteira de hoje, saldo de carteira de ontem, movimentações do dia, taxas cobradas.

Processamento automático: O sistema executa a lógica de processamento internamente. Compara valores antigos com novos. Calcula a diferença resultante. Determina se é ganho ou perda. Registra todas as operações.

Geração de resultados: O sistema produz três arquivos prontos para uso. Um arquivo Excel com abas segregadas para análise. Um arquivo CSV para importação no sistema contábil. Um relatório consolidado para gerentes.

Disponibilidade de informações: Os gerentes consultam o relatório Excel para decisões estratégicas. Os contadores usam o arquivo CSV para registrar no Protheus. Os analistas validam os números em relação ao dia anterior.

Tempo total de execução: Aproximadamente 2 minutos, sendo o processamento totalmente automático e sem erros humanos.

---

## RESUMO CONSOLIDADO DAS ETAPAS

As operações do sistema podem ser consolidadas em cinco etapas principais:

Etapa 1 - Leitura de Dados: O sistema localiza e abre os arquivos necessários. Tempo estimado: 5 segundos.

Etapa 2 - Comparação com Período Anterior: O sistema compara valores antigos e novos. Tempo estimado: 5 segundos.

Etapa 3 - Cálculo de Rendimentos: O sistema aplica fórmulas de cálculo. Tempo estimado: 10 segundos.

Etapa 4 - Registro Contábil: O sistema prepara lançamentos de débito e crédito. Tempo estimado: 5 segundos.

Etapa 5 - Geração de Relatórios: O sistema cria arquivos Excel e CSV. Tempo estimado: 5 segundos.

Tempo total de execução: Aproximadamente 30 segundos.

---


**Versão do Manual:** 1.2

**Data:** 13/04/2026

**Responsável:** Documentação Técnica


