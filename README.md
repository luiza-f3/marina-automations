# Documentação Técnica: Projeto `data_preprocessing`

## Visão Geral
O projeto `data_preprocessing` é um sistema de pré-processamento de dados contábeis, dividido em módulos especializados para benefícios, investimentos, folha de pagamento e pré-processamento geral. Cada módulo automatiza a extração, transformação e carregamento (ETL) de dados de fontes como Excel e CSV, gerando relatórios contábeis padronizados. O propósito é resolver problemas de inconsistência e manualidade em relatórios financeiros, assegurando lançamentos contábeis precisos para balanços patrimoniais, demonstrativos de resultados e provisões.

---

## 1. Módulo `benefits_sheet`

### 1.1 Visão Geral
- **Propósito**: Processa dados de benefícios (emprestimos, provisões, deduções) para gerar lançamentos contábeis em partida dobrada (débitos e créditos).
- **Problema Contábil Resolvido**: Padroniza e valida dados de benefícios contra uma planilha de consulta, evitando erros em lançamentos de débitos/créditos e garantindo conformidade com regras contábeis específicas (ex.: pagamentos dentro ou fora do mês).

### 1.2 Funcionalidades
- **Criação de Emprestimos**: Filtra itens de empréstimo (ex.: "41-EMPRESTIMO", "45-QUITACAODEEMPRESTIMO") e descontos específicos, considerando competência.
- **Criação de Provisões**: Filtra itens de provisão (ex.: deduções base tributável, baixas de estoque isento) e valores não-negativos.
- **Criação de Deduções**: Filtra itens dedutivos com contas de crédito válidas na consulta.
- **Contabilização**: Gera lançamentos contábeis para deduções, empréstimos e provisões, mapeando contas via consulta, aplicando regras de data e duplicando lançamentos para contas específicas.
- **Validação**: Verifica presença de valores em colunas contra a planilha de consulta, reportando ausências.
- **Salvamento**: Salva folha contabilizada em Excel, ordenada por plano, perfil, valor e D/C.

### 1.3 Estrutura do Código
- **Script Principal**: `main.py` orquestra o processamento, carregando dados, criando objetos de classes, validando e salvando.
- **Classes em `src/`**:
  - `Emprestimos`: Filtra empréstimos com base em itens folha e competência.
  - `Provisao`: Filtra provisões por itens específicos e valores.
  - `Deducao`: Filtra deduções com contas válidas.
  - `ContabilizarBeneficios`: Classe central com métodos `contabilizarDeducao`, `contabilizarEmprestimos`, `contabilizarProvisao` para gerar lançamentos.
- **Utilitários em `utils/`**:
  - `AccountingAccount`: Duplica lançamentos para contas específicas (ex.: de 10203080101020 para 10203080101010).
  - `tools`: Funções como `limparTexto` (remove acentos/espaços), `layoutLancamentoBeneficios` (cria DataFrame de lançamento), `extrair_rubrica`/`extrair_folha` (extração de textos).

### 1.4 Fluxo de Execução
1. Carrega CSV processado (`folha_beneficios_processado.csv`) e Excel de consulta (`consulta_folha_beneficios.xlsx`).
2. Filtra dados por data de pagamento.
3. Limpa texto em colunas da consulta.
4. Cria DataFrames via `Emprestimos.criarEmprestimos()`, `Provisao.criarProvisao()`, `Deducao.criarDeducao()`.
5. Valida colunas contra consulta, reportando ausências.
6. Contabiliza via `ContabilizarBeneficios.contabilizar()`, gerando lançamentos para cada categoria.
7. Filtra valores não-zero, duplica lançamentos via `AccountingAccount.duplicar_lancamentos_para_conta()`.
8. Formata datas/valores, ordena e salva em Excel.

### 1.5 Dependências
- **pandas**: Manipulação de DataFrames, filtros, concatenações.
- **os, datetime**: Caminhos e formatação de datas.
- **unidecode**: Remoção de acentos em `limparTexto`.
- Módulos locais: Classes em `src/`, utilitários em `utils/`.

### 1.6 Entradas e Saídas
- **Entradas**: CSV `folha_beneficios_processado.csv` (dados processados), Excel `consulta_folha_beneficios.xlsx` (regras de contas).
- **Saídas**: Excel `folha_contabilizada{data}.xlsx` com colunas ['Data', 'Conta contabil', 'Valor', 'D/C', 'Descricao', 'CC', 'Plano', 'Perfil', 'Patrocinadora'].

### 1.7 Exemplos de Uso
```python
from benefits_sheet.src.ContabilizarBeneficios import ContabilizarBeneficios

# Exemplo de contabilização
deducao_df = Deducao(df, competencia, consulta).criarDeducao()
emprestimos_df = Emprestimos(df, competencia).criarEmprestimos()
provisao_df = Provisao(df, competencia).criarProvisao()
contabilizado = ContabilizarBeneficios(deducao_df, emprestimos_df, provisao_df, consulta, data_pagamento, competencia).contabilizar()
print(contabilizado.head())
# Saída: DataFrame com lançamentos, ex.:
#   Data  Conta contabil  Valor  D/C  Descricao  CC  Plano  Perfil  Patrocinadora
# 0 29/07/2025  20101010100000  100.0  D    DESCONTO...  3   Plano1  Perfil1  001
```

### 1.8 Pontos de Atenção
- **Arquivos Ausentes**: Falha se CSV/Excel não existirem.
- **Dados Inválidos**: Filtros podem falhar se colunas não corresponderem; valores NaN em contas causam erros.
- **Performance**: Loops em DataFrames grandes podem ser lentos; validação sequencial.
- **Limitações**: Regras hardcoded (ex.: contas fixas); assume formatos específicos de data/item.
- **Erros**: Retorna strings de erro se DataFrames inválidos.

### 1.9 Melhorias Futuras
- Adicionar validações de entrada (ex.: verificar tipos de colunas).
- Implementar logging para rastrear execuções.
- Paralelizar processamento de grandes DataFrames.
- Tornar contas configuráveis via arquivo.
- Adicionar testes unitários para métodos de filtro/contabilização.

### 1.10 Comentários no Código
Adicione docstrings detalhadas:
- Em `ContabilizarBeneficios.contabilizarDeducao()`: `"""Gera lançamentos de débito/crédito para deduções, mapeando contas via consulta e aplicando regras de data."""`
- Em `Emprestimos.filtroEmprestimos()`: `"""Filtra empréstimos baseados em itens folha e competência, incluindo condições para pagamentos fora do mês."""`
- Comentários inline: ex. `# Verifica se filtro retorna resultados` antes de acessar `.iloc[0]`.

---

## 2. Módulo `investiments`

### 2.1 Visão Geral
- **Propósito**: Processa investimentos, carteiras, fluxos de caixa e gera demonstrativos financeiros com lançamentos contábeis em partida dobrada.
- **Problema Contábil Resolvido**: Automatiza a consolidação de carteiras de investimentos, cálculo de rentabilidades, geração de evoluções patrimoniais e contabilização de entradas/saídas de caixa, evitando inconsistências manuais em relatórios de investimentos.

### 2.2 Funcionalidades
- **Preparação de Carteiras**: Carrega múltiplos arquivos Excel de carteiras, extrai dados padronizados (código fundo, nome, valor atual), adiciona perfil/plano, formata códigos e mapeia classificações.
- **Preparação de Provisões**: Filtra resgates/aplicações e provisões de carteiras, separando-as em dois DataFrames distintos.
- **Processamento de Fluxo de Caixa**: Carrega demonstrativos de caixa, filtra por data específica, consolida entradas/saídas de fundos, normaliza textos e mapeia códigos de fundo.
- **Cálculo de Evolução Patrimonial**: Compara carteiras atuais/anteriores, calcula rentabilidades, saldos anteriores, entradas e saídas por fundo/perfil/plano.
- **Contabilização de Rentabilidades**: Gera lançamentos de débito/crédito para rendimentos positivos/negativos, mapeando contas contábeis.
- **Contabilização de Demonstrativos**: Cria lançamentos para aplicações e resgates, integrando com carteira.
- **Contabilização de Despesas/Taxas**: Processa despesas de gestão e taxas administrativas.
- **Validação e Salvamento**: Gera relatórios consolidados em CSV e Excel, com verificações de integridade.

### 2.3 Estrutura do Código
- **Script Principal**: `main.py` orquestra a execução, chamando `InvestimentosService.prepararInvestimentos()`.
- **Serviço Central**: `investiments_service.py` com classe `InvestimentosService` que orquestra todo o fluxo.
- **Módulos em `src/core/`**:
  - **`carteira/carteira.py`**: Classe `Carteira` com métodos `preparar_carteiras()` e `preparar_provisao()`.
  - **`demonstrativo/fluxo_caixa.py`**: Classe `FluxoDeCaixa` com métodos para preparação, totalização e filtragem de fluxos de caixa.
  - **`usecases/`**: Funções e classes para transformações específicas:
    - `prepararEvolucaoPatrimonial()`: Calcula evolução patrimonial comparando carteiras.
    - `prepararLancamentoContabil()`: Gera lançamentos contábeis para rentabilidades e demonstrativos.
    - `despesasTaxasDemonstrativo()`: Processa despesas e taxas.
    - `provisao_lancamento()`: Contabiliza provisões.
    - `executeFromTo()`: Renomeia valores em DataFrames via regex (ex.: "FUNDO (001-002)" → "FUNDO").
  - **`reports/`**: Geração de relatórios:
    - `gerarRelatorio()`: Relatório básico de carteira.
    - `gerarRelatorioDemonstrativo()`: Relatório consolidado de demonstrativos.
- **Utilitários em `src/utils/`**:
  - `tools.py`: Funções como `define_profile_plan()`, `normalize_text()`, `extrair_valor()`, `mapear_classificacoes()`.
  - `data_loader.py`: Carrega múltiplos arquivos de diretório.
  - `consultas/`: Mapeamentos (ex.: `cash_flow_info`, `expenses_mapping`, `fees_info`).

### 2.4 Fluxo de Execução
1. **Inicialização**: Carrega variáveis de ambiente (`.env`) com caminhos, datas atuais/anteriores.
2. **Carregamento de Provisões**: 
   - Executa `Carteira.preparar_provisao()` para datas atuais e anteriores.
   - Retorna resgates/aplicações e provisões em separado.
3. **Carregamento de Carteiras**:
   - Executa `Carteira.preparar_carteiras()` para datas atuais e anteriores.
   - Mapeia fundos entre carteiras para consistência.
4. **Geração de Relatório Inicial**: `gerarRelatorio()` com resgates/aplicações e carteira atual.
5. **Merge com Provisões**: Mescla resgates/aplicações com carteiras, ajustando valores atuais.
6. **Processamento de Fluxo de Caixa**:
   - Carrega demonstrativos via `FluxoDeCaixa.preparar_fluxo_caixa()`.
   - Processa com `processarDemonstrativos()`.
   - Totaliza entradas/saídas via `FluxoDeCaixa.totalizar_entrada_saida()`.
   - Calcula diferenças via `FluxoDeCaixa.gerar_diferenca_entradas_saidas()`.
   - Filtra registros de aquisição, demonstrativos e despesas.
7. **Cálculo de Evolução Patrimonial**: `prepararEvolucaoPatrimonial()` compara carteiras e calcula rentabilidades.
8. **Contabilização**:
   - Rentabilidades: `processarLancamentoContabil()`.
   - Despesas/Taxas: `despesas_taxas_demonstrativo()`.
   - Provisões: `provisao_lancamento()` (condicional).
9. **Salvamento**: `save_data()` salva DataFrames em arquivos (Excel/CSV).

### 2.5 Dependências
- **pandas**: Manipulação extensiva de DataFrames (leitura, merge, concat, filtros).
- **os, dotenv**: Caminhos e variáveis de ambiente.
- **unidecode**: Normalização de textos (remoção de acentos).
- **datetime**: Manipulação de datas.
- Módulos locais: `Carteira`, `FluxoDeCaixa`, funções em `usecases/` e `utils/`.

### 2.6 Entradas e Saídas
- **Entradas**:
  - Arquivos Excel de carteiras em `Carteiras/{dia}_{mes}/` (múltiplos arquivos por código de carteira).
  - Demonstrativos de caixa em `demonstrativos/` (arquivos Excel com movimentações).
  - Excel de consulta (`CONSULTA_FUNDOS`) com classificações, contas contábeis, planos e perfis.
- **Saídas**:
  - Arquivos salvos em `base_path` (via `save_data`):
    - `evolucao_patrimonial_{data}.xlsx`: Evolução patrimonial com rentabilidades.
    - `lancamentos_contabeis_{data}.xlsx`: Lançamentos em partida dobrada.
    - `despesas_taxas_{data}.xlsx`: Contabilização de despesas.
    - `provisoes_{data}.xlsx`: Provisões (condicional).
  - Relatórios gerados em memória e no terminal.

### 2.7 Exemplos de Uso
```python
# Exemplo 1: Executar processamento completo
from investiments.src.services.investiments_service import InvestimentosService

InvestimentosService.prepararInvestimentos()
# Saída: Arquivos salvos em base_path com evolução, lançamentos e despesas

# Exemplo 2: Carregar carteira manualmente
from investiments.src.core.carteira.carteira import Carteira

carteira_atual = Carteira.preparar_carteiras('/caminho/para/carteiras/26_03')
print(carteira_atual.head())
# Saída: DataFrame com colunas ['Cod Fundo', 'Fundo', 'Valor Atual', 'Plano', 'Perfil', 'Classificacao']

# Exemplo 3: Processar fluxo de caixa
from investimentos.src.core.demonstrativo.fluxo_caixa import FluxoDeCaixa

cash_flow = FluxoDeCaixa.preparar_fluxo_caixa('/caminho/para/demonstrativos', '26/03/2025')
print(cash_flow.head())
# Saída: DataFrame com colunas ['Historico', 'Entrada', 'Saida', 'Cod Fundo', 'Plano', 'Perfil']

# Exemplo 4: Gerar relatório de demonstrativos
from investimentos.src.core.usecases.reports.gerarRelatorioDemonstrativo import gerarRelatorioDemonstrativo

relatorio = gerarRelatorioDemonstrativo(cash_flow, '26/03/2025')
print(relatorio.head())
# Saída: DataFrame com colunas ['Data', 'Plano', 'Perfil', 'Histórico', 'Código do Fundo', 'Entrada', 'Saida']
```

### 2.8 Pontos de Atenção
- **Arquivos Ausentes**: Falha se diretórios de carteiras/demonstrativos não existirem ou `CONSULTA_FUNDOS` não estiver configurado.
- **Dados Inválidos**: Valores NaN em colunas críticas causam erros em merges; códigos de fundo inconsistentes provocam não-matches.
- **Performance**: Loops em DataFrames grandes (múltiplas carteiras) podem ser lentos; sem otimizações para volumes altos.
- **Limitações**:
  - Contas contábeis e filtros hardcoded (ex.: padrões em `executeFromTo`).
  - Assume estrutura fixa de arquivos Excel (ex.: dados a partir da linha 7/10).
  - Método `prepararContabilizacaoInvestimentos()` incompleto.
- **Erros Silenciosos**: Algumas falhas retornam strings de erro em vez de lançar exceções.

### 2.9 Melhorias Futuras
- Adicionar validações robustas (verificar tipos de colunas, valores NaN).
- Implementar logging detalhado em cada etapa do processamento.
- Paralelizar carregamento de múltiplos arquivos de carteira.
- Tornar contas contábeis e filtros configuráveis via arquivo.
- Adicionar testes unitários para métodos críticos.
- Tratar erros consistentemente (exceptions vs. strings).
- Implementar cache para consulta de fundos (lê uma vez, reutiliza).
- Adicionar opcionalidade para processamento incremental (apenas novos dados).

### 2.10 Comentários no Código
Adicione docstrings detalhadas:
- Em `Carteira.preparar_carteiras()`: `"""Carrega arquivos Excel de carteiras, extrai colunas críticas, formata códigos, adiciona plano/perfil e mapeia classificações."""`
- Em `FluxoDeCaixa.preparar_fluxo_caixa()`: `"""Carrega demonstrativos, filtra movimentações por data, normaliza textos e adiciona plano/perfil."""`
- Em `prepararEvolucaoPatrimonial()`: `"""Calcula evolução patrimonial comparando carteiras atuais/anteriores e fluxo de caixa, gerando rentabilidades por fundo/plano/perfil."""`
- Comentários inline em loops críticos: ex. `# Mescla valores por chave composta (fundo_plano_perfil)` em `totalizar_entrada_saida()`.
- Documente assumências: ex. `# Assume que códigos de fundo têm 6 dígitos, preenche com zeros` em `preparar_carteiras()`.

---

## 3. Módulo `payroll`

### 3.1 Visão Geral
- **Propósito**: Processa dados de folha de pagamento para gerar lançamentos contábeis em partida dobrada, com múltiplas visões contábeis por percentual de alocação.
- **Problema Contábil Resolvido**: Automatiza a contabilização de folha de pagamento, dividindo valores entre múltiplas visões contábeis (Multi, BD, Telefônica, Previsão) por percentual, mapeando rubricas para contas de débito/crédito e gerando lançamentos em partida dobrada com históricos padronizados.

### 3.2 Funcionalidades
- **Carregamento de Dados**: Lê CSV de folha de pagamento e Excel de consulta de rubricas.
- **Padronização de Tipos**: Converte rubricas e folhas para strings para garantir correspondência em merges.
- **Busca de Contas Contábeis**: Localiza contas de débito/crédito, descrição e centro de custo via merge com planilha de consulta.
- **Lançamentos Multi-Visão**: Cria lançamentos para 4 visões contábeis distintas (Multi, BD, Telefônica, Previsão) aplicando percentuais diferentes.
- **Geração de Lançamentos**: Produz lançamentos de débito/crédito com históricos padronizados (ex.: "FOLHA SALARIO 26/2025 1001 SALARIO BASE").
- **Formatação de Saída**: Ordena colunas e retorna DataFrame com lançamentos consolidados.

### 3.3 Estrutura do Código
- **Script Principal**: `main.py` orquestra o processamento, carregando CSV, removendo colunas desnecessárias e executando contabilização.
- **Classe em `src/`**:
  - **`ContabilizarPayroll`**: Classe central com métodos:
    - `__init__()`: Carrega payroll CSV e consulta Excel.
    - `contabilizar()`: Orquestra todo o processamento.
    - `encontrarContaContabil()`: Realiza merge com consulta para mapear contas.
    - `lancamento()`: Gera lançamentos para uma visão contábil específica.
- **Utilitários em `src/`**:
  - `tools.py`: Função `criar_lancamento_contabil()` para criar dicionários de lançamento (não utilizada atualmente, possível melhoria).

### 3.4 Fluxo de Execução
1. Carrega variáveis de ambiente (caminhos, percentuais de visões, data).
2. Lê CSV de payroll (`path_payroll`).
3. Remove colunas desnecessárias (`DataApropriacao`, `DataVencimento`).
4. Inicializa `ContabilizarPayroll` com DataFrame de payroll.
5. Executa `contabilizar()`:
   - Padroniza tipos de dados (rubricas/folhas para string).
   - Carrega consulta Excel de rubricas com contas contábeis.
   - Padroniza tipos na consulta.
   - Executa `encontrarContaContabil()` para fazer merge e mapear contas.
   - Para cada visão (Multi, BD, Telefônica, Previsão):
     - Executa `lancamento()` com plano e percentual específicos.
     - Gera lançamentos de débito/crédito para cada linha de payroll.
     - Formata histórico, conta, valor e CC.
   - Concatena lançamentos de todas as visões.
6. Imprime DataFrame consolidado (possível melhoria: salvar em arquivo).

### 3.5 Dependências
- **pandas**: Manipulação de DataFrames (leitura CSV, merge, concat).
- **os, dotenv**: Caminhos e variáveis de ambiente (percentuais, caminhos de arquivos).
- **unidecode**: Normalização de históricos (remoção de acentos/caracteres especiais).
- Módulos locais: `ContabilizarPayroll`, utilitários em `tools.py`.

### 3.6 Entradas e Saídas
- **Entradas**:
  - CSV de payroll (carregado via `PAYROLL` env): Colunas como 'Rubrica', 'Folha', 'DataEmissao', 'ValorLiquido', etc.
  - Excel de consulta (`CONSULT_PAYROLL` env): Colunas 'Rubrica', 'Folha', 'Conta debito', 'Conta credito', 'Descricao', 'CC'.
  - Variáveis de ambiente: `VISAO_MULTI_PERCENTUAL`, `BD_PERCENTUAL`, `VISAO_TELEFONICA_PERCENTUAL`, `PREVISAO_PERCENTUAL`.
- **Saídas**:
  - DataFrame impresso no terminal com colunas ['Conta contabil', 'Valor', 'D/C', 'Historico', 'CC', 'Plano', 'Perfil'].
  - Sem arquivo salvo (possível melhoria: salvar em Excel/CSV).

### 3.7 Exemplos de Uso
```python
# Exemplo 1: Executar contabilização completa
from payroll.src.ContabilizarPayroll import ContabilizarPayroll
import pandas as pd

payroll = pd.read_csv('/caminho/para/payroll.csv')
payroll.drop(columns=['DataApropriacao', 'DataVencimento'], inplace=True)

payroll_contabilizado = ContabilizarPayroll(payroll).contabilizar()
print(payroll_contabilizado.head())
# Saída: DataFrame com colunas ['Conta contabil', 'Valor', 'D/C', 'Historico', 'CC', 'Plano', 'Perfil']
# Exemplo de linha:
#   Conta contabil  Valor  D/C  Historico             CC  Plano  Perfil
# 0 6100100       1000.0  D    FOLHA SALARIO 26/2025 1001 0908   19
# 1 2100200       1000.0  C    FOLHA SALARIO 26/2025 1001 0908   19

# Exemplo 2: Acessar DataFrame de consulta
payroll_obj = ContabilizarPayroll(payroll)
consulta = payroll_obj.consult_payroll
print(consulta.head())
# Saída: Consulta com rubricas, folhas e contas contábeis

# Exemplo 3: Processar uma única visão (simulado)
df_contabil = payroll_obj.encontrarContaContabil()
multi_accounting = payroll_obj.lancamento(df_contabil, 908, 25.0)  # 25% para Multi
print(multi_accounting)
# Saída: DataFrame com lançamentos para visão Multi (plano 908)
```

### 3.8 Pontos de Atenção
- **Arquivos Ausentes**: Falha se CSV de payroll ou Excel de consulta não existirem.
- **Dados Inválidos**: Rubricas/folhas sem correspondência na consulta resultam em NaN para contas; merge pode gerar linhas com valores nulos.
- **Performance**: Loops iterativos em grande volume de payroll podem ser lentos; sem vetorização.
- **Limitações**:
  - Plano e Perfil hardcoded por visão (ex.: plano 908 para Multi, perfil 19 fixo).
  - Assume estrutura fixa de arquivo Excel de consulta.
  - Data extraída do formato "dia-mês-ano" em `DataEmissao` (brittle).
  - Percentuais carregados como strings de ambiente (requerem conversão).
- **Erros Silenciosos**: Merge com `how='left'` gera NaN em contas não encontradas, mas não levanta erro.
- **Sem Salvamento**: DataFrame apenas impresso, sem persistência em arquivo.

### 3.9 Melhorias Futuras
- Adicionar validações de entrada (verificar colunas obrigatórias, tipos, valores NaN).
- Implementar salvamento automático em Excel/CSV com nome parametrizado.
- Paralelizar processamento de visões (threadpool para as 4 visões).
- Tornar planos/perfis configuráveis via arquivo ou env.
- Substituir loops por operações vetorizadas (apply/groupby).
- Implementar logging detalhado para rastrear merges e erros.
- Adicionar tratamento de erros para rubricas não encontradas (alertas/relatório).
- Criar testes unitários para métodos de merge e lançamento.
- Normalizar formato de data de entrada (usar parser de data robusto).

### 3.10 Comentários no Código
Adicione docstrings detalhadas:
- Em `ContabilizarPayroll.__init__()`: `"""Inicializa com DataFrame de payroll e carrega consulta de rubricas/contas."""`
- Em `ContabilizarPayroll.contabilizar()`: `"""Orquestra contabilização, criando lançamentos para 4 visões contábeis com percentuais distintos."""`
- Em `encontrarContaContabil()`: `"""Realiza merge entre payroll e consulta de rubricas para mapear contas de débito/crédito."""`
- Em `lancamento()`: `"""Gera lançamentos de débito/crédito em partida dobrada para uma visão contábil, aplicando percentual ao valor."""`
- Comentários inline:
  - `# Converte para string para garantir match no merge` antes de conversão de tipos.
  - `# Aplica percentual à visão contábil` em `lancamento()`.
  - `# Remove pontuação da conta contábil (ex.: "6100.1.00" → "6100")` na extração de contas.

---

## 4. Módulo `pre_processing`

### 4.1 Visão Geral
- **Propósito**: Executa pipeline ETL (Extract, Transform, Load) para múltiplas fontes de dados financeiros, padronizando dados brutos em formatos processados para uso em outros módulos (benefits_sheet, investiments, payroll).
- **Problema Contábil Resolvido**: Centraliza e padroniza a extração de dados de múltiplas fontes (folha de benefícios, folha de pagamento, reservas, arrecadação), aplicando transformações consistentes (normalização de texto, mapeamento de valores, tipagem de dados) para garantir qualidade de dados e compatibilidade com módulos de contabilização downstream.

### 4.2 Funcionalidades
- **Download de Arquivos**: Copia arquivos de fontes (ex.: Google Drive, pastas compartilhadas) para diretório local `data/raw/`.
- **Extração de Dados (Extract)**: Lê arquivos Excel/XLS, extrai colunas específicas, define esquema de tipos e realiza limpeza básica de dados.
- **Transformação de Dados (Transform)**: Normaliza texto (remoção de acentos, espaços extras), mapeia valores (ex.: nomes de planos para códigos), extrai informações estruturadas (ex.: rubrica de histórico).
- **Salvamento Processado (Load)**: Salva DataFrames transformados como CSV em `data/processed/` para consumo por outros módulos.
- **Suporte Multi-Fonte**: Integra dados de 5 fontes: Autopatrocinado, Reservas, Folha de Benefícios, Folha de Pagamento, Arrecadação (atualmente apenas Folha de Benefícios ativa).

### 4.3 Estrutura do Código
- **Script Principal**: `main.py` orquestra o pipeline, coordenando downloads, extrações, transformações e salvamentos.
- **Configuração**: `config/settings.py` centraliza caminhos, variáveis de ambiente e constantes.
- **Módulos em `scripts/`**:
  - **`download/download.py`**: Funções para copiar arquivos:
    - `download_autopatrocinado()`: Copia arquivo autopatrocinado.
    - `download_reservas()`: Copia arquivo de reservas.
    - `download_folha_beneficios()`: Copia arquivo de folha de benefícios.
    - `download_folha_pagamentos()`: Copia arquivo de folha de pagamento.
    - `download_arrecadacao()`: Copia arquivo de arrecadação.
    - `copy_file()`: Função auxiliar para copiar com tratamento de erros.
  - **`extract/`**: Funções para extração e limpeza:
    - `extract_folha_beneficios()`: Lê XLS, extrai 9 colunas, remove linhas vazias, tipifica e ajusta datas.
    - `extract_folha_pagamento()`: Lê Excel, extrai rubrica/folha de histórico, tipifica.
    - `extract_reservas()`: Extração de dados de reservas (não analisado em detalhes).
    - `extract_autopatrocinado()`: Extração de autopatrocinado (não analisado).
    - `extract_arrecadacao()`: Extração de arrecadação (não analisado).
  - **`transform/`**: Funções para transformação:
    - `transform_folha_beneficios()`: Remove espaços, normaliza acentos, mapeia planos/perfis, usa dicionário de portfolio.
    - `transform_folha_pagamento()`: Remove espaços, normaliza acentos, trata valores.
    - Outras transformações (não analisadas).
  - **`load/load_data.py`**: Funções para carregar em banco de dados (atualmente comentadas, não implementadas).
- **Utilitários em `utils/`**:
  - `benefits/portfolio_dictionary.py`: Dicionário mapeando nomes de empregadores para códigos de patrocinadora.
  - Funções em `benefits_sheet/utils/tools.py`: `extrair_folha()`, `extrair_rubrica()` para parsing de históricos.

### 4.4 Fluxo de Execução
1. **Inicialização**: Carrega variáveis de ambiente via `config/settings.py`.
2. **Download** (opcional):
   - Executa `download.download_folha_beneficios()` para copiar arquivo fonte.
   - Cria estrutura de diretórios `data/raw/` se não existir.
3. **Loop sobre Sheets**:
   - Para cada sheet ativo (ex.: "folha_beneficios"):
     - Lista arquivos em `data/raw/`.
     - Para cada arquivo:
       - **Extração**: Se nome do arquivo corresponde ao sheet:
         - Executa função extract apropriada (ex.: `extract_folha_beneficios()`).
         - Lê Excel, define schema de tipos, remove NaN/linhas vazias.
       - **Transformação**: 
         - Executa função transform (ex.: `transform_folha_beneficios()`).
         - Remove espaços, normaliza acentos.
         - Mapeia planos (ex.: "VISAO MULTI" → 8).
         - Mapeia perfis (extrai número de string).
         - Mapeia patrocinadora via dicionário.
       - **Salvamento**:
         - Cria `data/processed/` se não existir.
         - Salva DataFrame como CSV com nome `{sheet}_processado.csv`.
4. **Retorno**: Completa o pipeline (sem persistência em BD, apenas arquivos).

### 4.5 Dependências
- **pandas**: Leitura Excel, manipulação DataFrames, tipagem de dados.
- **os, shutil**: Caminhos, criação de diretórios, cópia de arquivos.
- **dotenv**: Carregamento de variáveis de ambiente.
- **unidecode**: Normalização de texto (remoção de acentos).
- **re**: Expressões regulares para parsing (ex.: extrair rubrica de histórico).
- Módulos locais: Funções em `scripts/`, utilitários, dicionários.

### 4.6 Entradas e Saídas
- **Entradas**:
  - Arquivos de origem (via variáveis de ambiente):
    - `PATH_FOLHA_BENEFICIOS`: XLS com colunas "Tipo de folha", "Data de pagamento", "Plano", etc.
    - `PATH_RESERVAS`: Excel com dados de reservas.
    - `PATH_AUTOPATROCINADO`: Arquivo de autopatrocinado.
    - Etc.
  - Copiados para `data/raw/{sheet_name}.{extensão}`.
- **Saídas**:
  - CSV processados em `data/processed/`:
    - `folha_beneficios_processado.csv`: Schema tipificado, planos/perfis mapeados.
    - `folha_pagamento_processado.csv`: Rubricas e folhas extraídas.
    - Etc.
  - Logs de cópia e processamento no terminal.

### 4.7 Exemplos de Uso
```python
# Exemplo 1: Executar pipeline ETL completo
from pre_processing.main import process_and_load

process_and_load()
# Saída: Arquivos CSV salvos em data/processed/ com dados transformados

# Exemplo 2: Extrair manualmente folha de benefícios
from pre_processing.scripts.extract import extract_folha_beneficios

df = extract_folha_beneficios('/caminho/para/folha_beneficios.xls')
print(df.head())
# Saída: DataFrame com 9 colunas tipificadas, NaN removidos

# Exemplo 3: Transformar folha de benefícios
from pre_processing.scripts.transform import transform_folha_beneficios

df_transformado = transform_folha_beneficios(df)
print(df_transformado.head())
# Saída: Planos mapeados (ex.: "VISAO MULTI" → 8), perfis numéricos, acentos removidos

# Exemplo 4: Download de arquivo específico
from pre_processing.scripts.download import download

download.download_folha_beneficios()
# Saída: Arquivo copiado para data/raw/folha_beneficios.xls
```

### 4.8 Pontos de Atenção
- **Dependências de Variáveis de Ambiente**: Falha se caminhos não configurados em `.env`.
- **Arquivos Ausentes**: Se arquivo fonte não existir, `FileNotFoundError` levantado.
- **Estrutura de Arquivo Fixa**: Assume colunas específicas no Excel (ex.: "Tipo de folha" para benefícios); mudanças causam falhas.
- **Limitações**:
  - Apenas "folha_beneficios" ativa no `main.py` (outros sheets comentados).
  - Funções `load_data` não implementadas (comentadas).
  - Suporta apenas Excel/XLS (sem CSV input direto).
  - Nenhuma validação de integridade de dados após transformação.
- **Dados Inválidos**: Linhas com colunas-chave vazias removidas sem relatório; datas inválidas retornam `NaT`.
- **Performance**: Sem otimizações para arquivos grandes; loops sequenciais.

### 4.9 Melhorias Futuras
- Descomentar e integrar todos os sheets (Autopatrocinado, Reservas, Arrecadação, Folha de Pagamento).
- Implementar funcionalidade de Load em banco de dados (usar `load_data.py`).
- Adicionar logging detalhado para rastrear cada etapa (download, extract, transform).
- Implementar validações de integridade (schema checking, row counts, null counts).
- Adicionar suporte a múltiplos formatos de entrada (CSV, Parquet, JSON).
- Paralelizar processamento de múltiplos arquivos.
- Implementar detecção automática de schema (inferência de tipos).
- Adicionar testes unitários para extract e transform.
- Criar relatório de qualidade de dados (ex.: linhas removidas, valores NaN).
- Tornar caminhos e mapeamentos configuráveis via arquivo (YAML/JSON).

### 4.10 Comentários no Código
Adicione docstrings detalhadas:
- Em `process_and_load()`: `"""Orquestra pipeline ETL, baixando, extraindo, transformando e salvando dados de múltiplas fontes."""`
- Em `download_folha_beneficios()`: `"""Copia arquivo de folha de benefícios da origem para data/raw/, criando diretório se necessário."""`
- Em `extract_folha_beneficios()`: `"""Lê XLS, extrai 9 colunas, define schema de tipos, remove NaN e ajusta formato de datas."""`
- Em `transform_folha_beneficios()`: `"""Normaliza texto (acentos, espaços), mapeia planos a códigos e extrai perfis numéricos."""`
- Comentários inline:
  - `# Remove linhas com colunas-chave vazias ou NaN` no extract.
  - `# Mapeia nome de plano para código numérico (ex.: "VISAO MULTI" → 8)` em transform.
  - `# Usa dicionário para converter nome de empregador para código de patrocinadora` em transform.
  - `# Salva em data/processed/ com nome {sheet}_processado.csv` em load.

---
