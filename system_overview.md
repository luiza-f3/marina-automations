# Marina automations - System Overview

## Descrição do Sistema
O Marina automations é um sistema de automação contábil voltado para entidades de previdência, fundos e empresas que necessitam processar grandes volumes de dados financeiros de forma padronizada, segura e auditável. O sistema integra, trata e valida dados de diferentes fontes (planilhas, extratos, arquivos CNAB), automatizando a geração de lançamentos contábeis e relatórios prontos para importação em ERPs como o Protheus.

---

## Objetivo
- Automatizar processos contábeis rotineiros e complexos
- Reduzir erros manuais e retrabalho
- Padronizar a geração de arquivos de integração contábil (ex: Protheus)
- Garantir rastreabilidade, validação cruzada e consistência dos dados
- Facilitar auditorias e o fechamento contábil

---

## Módulos do Sistema

| Módulo      | Descrição                                 |
|-------------|-------------------------------------------|
| Investments | Processamento de carteiras e rendimentos  |
| Loans       | Processamento de rendimentos de empréstimos |
| Benefits    | Processamento da folha de benefícios      |

---

## Fluxo Geral do Sistema (Data Flow)

Entrada → Processamento → Saída

- **Entrada:** Arquivos Excel, planilhas, extratos bancários, arquivos CNAB
- **Processamento:** Módulos especializados (Investments, Loans, Benefits) realizam leitura, validação, tratamento, cálculo e geração de lançamentos
- **Saída:** Arquivos CSV/Excel padronizados para integração contábil (ex: Protheus), relatórios de apoio e logs de validação

---

## Fluxo detalhado

```text
1. Entrada de dados
   - Recebimento de arquivos de diferentes fontes:
     • Consultas: planilhas de referência, mapeamentos, extratos bancários
     • Carteiras: arquivos diários de posição de fundos (Excel)
     • Demonstrativos: extratos de caixa, relatórios de movimentação
     • Folha: planilhas de benefícios, empréstimos, deduções

        ↓

2. Módulo de Investimentos
   - Leitura e consolidação das carteiras diárias de fundos
   - Extração de provisões e movimentações pendentes
   - Processamento do fluxo de caixa (entradas, saídas, taxas, aplicações, resgates)
   - Cálculo da evolução patrimonial dos fundos
   - Geração de lançamentos contábeis de investimentos, aplicações, resgates e despesas
   - Produção de relatórios de apoio e arquivos para importação contábil

        ↓

3. Módulo de Empréstimos
   - Leitura dos arquivos de rendimentos de empréstimos
   - Mapeamento de planos, perfis e contas contábeis
   - Geração dos lançamentos de juros de empréstimos (débito/crédito)
   - Exportação de arquivos prontos para o sistema Protheus

        ↓

4. Módulo de Folha de Benefícios
   - Leitura e validação da folha de benefícios processada
   - Cruzamento com planilhas de consulta e regras de negócio
   - Processamento de deduções, provisões e empréstimos vinculados à folha
   - Consolidação e contabilização dos lançamentos de benefícios
   - Geração de relatórios e arquivos de integração contábil

        ↓

5. Geração de arquivos contábeis e relatórios
   - Arquivos CSV/Excel padronizados para importação no Protheus
   - Relatórios de conferência, logs de validação e rastreabilidade
```

---

## Observações
- O sistema é modular e pode ser expandido para outros tipos de processamento financeiro.
- Todos os módulos seguem padrões de validação e geração de arquivos compatíveis com sistemas de gestão contábil.
- A configuração é centralizada por variáveis de ambiente e arquivos de settings, facilitando a adaptação a diferentes ambientes e instituições.
