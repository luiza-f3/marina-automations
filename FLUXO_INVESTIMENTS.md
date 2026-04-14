# Fluxo do Projeto "Investiments"

## Visão Geral
O projeto "Investiments" é um sistema de processamento de dados financeiros focado na contabilização de investimentos, geração de relatórios demonstrativos e evolução patrimonial. Ele automatiza a coleta, transformação e análise de dados de carteiras de investimento, demonstrativos de fluxo de caixa e provisões, gerando relatórios contábeis e financeiros consolidados.

## Arquivo de Início
O ponto de entrada do sistema é o arquivo `main.py`, localizado na raiz do projeto. Este arquivo importa a classe `InvestimentosService` do módulo `src/services/investiments_service.py` e executa o método `prepararInvestimentos()`.

```python
from investiments.src.services.investiments_service import InvestimentosService

if __name__ == "__main__":
    InvestimentosService.prepararInvestimentos()
```

## Fluxo de Execução Principal
O método `prepararInvestimentos()` orquestra todo o processamento em etapas sequenciais:

### 1. Preparação de Provisões e Carteiras
- **Arquivo**: `src/core/carteira/carteira.py`
- **Tratamento**: Carrega arquivos de carteiras de investimento (Excel) para datas atuais e anteriores.
- **Forma**: 
  - `preparar_provisao()`: Extrai provisões, resgates e aplicações do rodapé das planilhas.
  - `preparar_carteiras()`: Junta todas as carteiras em um DataFrame único, adicionando colunas de plano e perfil.
- **Resultado**: DataFrames com carteiras consolidadas e provisões separadas.

### 2. Geração de Relatório Inicial
- **Arquivo**: `src/core/usecases/reports/gerarRelatorio.py`
- **Tratamento**: Cria um relatório básico com resgates, aplicações e provisões.
- **Forma**: Função `gerarRelatorio()` combina dados de provisões com carteiras atuais.
- **Resultado**: Relatório inicial salvo em arquivo.

### 3. Preparação do Fluxo de Caixa
- **Arquivo**: `src/core/demonstrativo/fluxo_caixa.py`
- **Tratamento**: Carrega demonstrativos de fluxo de caixa (Excel) filtrados por data.
- **Forma**: 
  - `preparar_fluxo_caixa()`: Extrai dados de entradas e saídas, adiciona plano e perfil.
  - `totalizar_entrada_saida()`: Agrupa valores por fundos/taxas.
  - `gerar_diferenca_entradas_saidas()`: Calcula diferenças entre entradas e saídas.
  - `filtrar_registros()`: Separa aquisições/resgates, fluxo de caixa e despesas.
- **Resultado**: DataFrames com fluxo de caixa processado, diferenças e registros filtrados.

### 4. Processamento de Demonstrativos
- **Arquivo**: `src/core/usecases/reports/gerarRelatorioDemonstrativo.py`
- **Tratamento**: Gera relatório consolidado de demonstrativos de caixa.
- **Forma**: 
  - `gerarRelatorioDemonstrativo()`: Formata DataFrame com colunas padronizadas (Data, Plano, Perfil, Histórico, Código do Fundo, Entrada, Saída).
  - `salvarRelatorioConsolidado()`: Salva em CSV com auto-incremento de registros.
  - `processarDemonstrativos()`: Orquestra geração e salvamento.
- **Resultado**: Arquivo CSV `RELATORIO_DEMONSTRATIVOS.csv` na pasta `relatorios`.

### 5. Preparação da Evolução Patrimonial
- **Arquivo**: `src/core/usecases/prepararEvolucaoPatrimonial.py`
- **Tratamento**: Calcula evolução diária do patrimônio por fundo.
- **Forma**: Função `prepararEvolucaoPatrimonial()` compara carteiras atual e anterior, incorporando diferenças do fluxo de caixa.
- **Resultado**: DataFrame com evolução patrimonial (fundo, plano, perfil, saldos, entradas, saídas, rendimento).

### 6. Contabilização
- **Arquivo**: `src/core/usecases/prepararLancamentoContabil.py`
- **Tratamento**: Prepara lançamentos contábeis para balanço patrimonial.
- **Forma**: Função `processarLancamentoContabil()` gera registros de rentabilidade baseados na evolução patrimonial e fluxo de caixa.
- **Resultado**: DataFrame com lançamentos contábeis de rendimento.

### 7. Processamento de Despesas e Taxas
- **Arquivo**: `src/core/usecases/despesasTaxasDemonstrativo.py`
- **Tratamento**: Contabiliza despesas e taxas do demonstrativo.
- **Forma**: Função `despesas_taxas_demonstrativo()` mapeia e classifica despesas.
- **Resultado**: DataFrame com contabilização de taxas e despesas.

### 8. Processamento de Provisões (Condicional)
- **Arquivo**: `src/core/usecases/provisao_lancamento.py`
- **Tratamento**: Gera lançamentos contábeis para provisões se habilitado.
- **Forma**: Função `provisao_lancamento()` processa provisões quando `PROVISAO=True` no .env.
- **Resultado**: DataFrame com lançamentos de provisões (se aplicável).

### 9. Salvamento Final dos Dados
- **Arquivo**: `src/utils/tools.py`
- **Tratamento**: Salva todos os DataFrames processados em arquivos Excel.
- **Forma**: Função `save_data()` exporta evolução patrimonial, contabilização de rendimento, taxas/despesas e provisões.
- **Resultado**: Arquivos Excel na pasta base com dados consolidados.

## Dependências e Utilitários
- **DataLoader**: `src/utils/data_loader.py` - Carrega arquivos Excel de diretórios.
- **Ferramentas**: `src/utils/tools.py` - Funções auxiliares (mapeamento, normalização, salvamento).
- **Consultas**: Pasta `src/utils/consultas/` - Mapeamentos e informações de fundos, taxas, etc.
- **ExecuteFromTo**: `src/core/usecases/executeFromTo.py` - Processa renomeações e mapeamentos.

## Entradas e Saídas
### Entradas
- Arquivos Excel de carteiras (pasta `Carteiras`).
- Arquivos Excel de demonstrativos (pasta `demonstrativos`).
- Arquivo de consulta de fundos (definido em .env).
- Variáveis de ambiente (.env): datas, caminhos, flags.

### Saídas
- Relatório inicial de resgates/aplicações/provisões.
- Relatório consolidado de demonstrativos (`RELATORIO_DEMONSTRATIVOS.csv`).
- Arquivos Excel com evolução patrimonial, contabilização, taxas e provisões.
- Logs no console com status do processamento.

## Pontos de Atenção
- Dependência de estrutura específica dos arquivos Excel de entrada.
- Necessidade de configuração correta das variáveis de ambiente.
- Possível falha se arquivos de entrada estiverem corrompidos ou ausentes.
- Processamento condicional de provisões baseado em flag do .env.

## Melhorias Futuras
- Adicionar validação mais robusta de arquivos de entrada.
- Implementar logging estruturado em arquivo.
- Criar interface para configuração de parâmetros.
- Adicionar testes unitários para funções críticas.
- Otimizar performance para grandes volumes de dados.

## Explicação Zero Técnica do Fluxo
O sistema funciona como uma linha de produção financeira: primeiro, coleta dados brutos de carteiras e movimentações; depois, limpa e organiza essas informações; calcula diferenças e evoluções; finalmente, gera relatórios contábeis prontos para uso em sistemas de gestão financeira. É como transformar dados dispersos em um balanço patrimonial completo e atualizado diariamente.</content>
<parameter name="filePath">C:\Users\LuizaMoreira\Documents\code\data_preprocessing\FLUXO_INVESTIMENTS.md
