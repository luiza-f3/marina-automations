import pandas as pd

from investiments.src.use_cases.replace_column import replace_column_values
from investiments.src.utils.data_loader import DataLoader
from investiments.src.utils.mappings.cash_flow_info import cash_flow_info
from investiments.src.utils.mappings.fees_info import fees_info
from investiments.src.utils.mappings.rename_data import fund_name_mapping
from investiments.src.utils.tools import filter_statement_by_date, define_profile_plan, normalize_text

# Classe responsável pelo processamento dos demonstrativos de fluxo de caixa
class cashFlow:

    # Extrai os códigos das carteiras usados para localizar os demonstrativos
    wallet_code = [item[0] for item in cash_flow_info]
    
    # Lista de padrões usados para identificar despesas e taxas
    fees_statement = fees_info

# prepare_cash_flow(): Consolida múltiplos demonstrativos demonstrativos de fluxo de caixa em um único DataFrame processado.
    @classmethod
    def prepare_cash_flow(cls, file_path, target_date):
        
        # CARREGAMENTO DOS DEMONSTRATIVOS (Busca arquivos pelos códigos definidos em wallet_code.)
        cash_flow_payloads = DataLoader.load_file_directory(file_path, cls.wallet_code, include_filename=True)
        if not cash_flow_payloads:
            return pd.DataFrame()
        missing_files = []
        cash_flow_data = {}

        # EXTRAÇÃO, PADRONIZAÇÃO E FILTRAGEM POR DATA
        for key, (df, file_name) in cash_flow_payloads.items():
            if df is None:
                continue
            df = df.iloc[7:, :4]
            df = pd.DataFrame(
                df.set_axis(['Data', 'Historico', 'Entrada', 'Saida'], axis='columns')
            )
            cash_flow_data[key] = filter_statement_by_date(
                df,
                target_date,
                missing_files=missing_files,
                source_name=file_name,
                verbose=False
            )

        if missing_files:
            unique_missing = sorted(set(missing_files))
            print("[AVISO] Data '%s' nao encontrada nos demonstrativos:" % target_date)
            print("        Arquivos: %s" % unique_missing)
            print("        Total: %d arquivos sem a data" % len(unique_missing))

        # ADIÇÃO DE PLANO E PERFIL
        for key, df in cash_flow_data.items():
            # Adiciona Plano e Perfil apenas para DataFrames com dados válidos
            if df is not None and not df.empty:
                # Relaciona o código da carteira ao respectivo Plano e Perfil
                cash_flow_data[key] = define_profile_plan(cash_flow_data[key], key, cash_flow_info)

        # CONSOLIDAÇÃO DOS DEMONSTRATIVOS
        combined_cash_flow = pd.concat(cash_flow_data).reset_index(drop=True)

        # NORMALIZAÇÃO E LIMPEZA DOS DADOS
        if not combined_cash_flow.empty:
            # Padroniza o histórico para maiúsculo e sem acentos
            combined_cash_flow['Historico'] = combined_cash_flow['Historico'].apply(normalize_text)

            # Padroniza nomes dos fundos utilizando fund_name_mapping para evitar divergências de cálculo
            combined_cash_flow = replace_column_values(combined_cash_flow, 'Historico', fund_name_mapping)
            combined_cash_flow['Cod Fundo'] = combined_cash_flow['Cod Fundo'].str.zfill(6) # zfill: Padroniza o código do fundo para 6 dígitos
            
            # Remove coluna Data (já utilizou para filtrar, não mais necessária)
            combined_cash_flow.drop('Data', axis=1, inplace=True)

            return combined_cash_flow

        return pd.DataFrame()

#totalize_cash_flow(): Agrega movimentações mantendo individualmente registros de despesas, aplicando regras específicas para garantir rastreabilidade e evitar duplicidade contábil.
    @classmethod
    def totalize_cash_flow(cls, statement):
        
        # Retorno antecipado se DataFrame vazio
        if statement.empty:
            return pd.DataFrame()

        aggregated_values = {}
        fee_counter = 0

        # CLASSIFICAÇÃO E AGRUPAMENTO DAS MOVIMENTAÇÕES
        for _, row in statement.iterrows():
            history = row['Historico']
            inflow = row['Entrada']
            outflow = row['Saida']
            plan = row['Plano']
            profile = row['Perfil']
            fund_code = row['Cod Fundo']

            # Define a direção da movimentação com base em entrada ou saída
            # Entrada > 0 = Pos (aplicação de caixa)
            # Saida > 0 = Neg (resgate do fundo)
            movement_type = "Pos" if inflow > 0 else "Neg"
            
            # Cria chave composta para agrupamento das movimentações
            composite_key = f"{fund_code}_{plan}_{profile}_{movement_type}"

            fee_found = False

            # IDENTIFICAÇÃO DE DESPESAS (Mantém taxas e despesas como registros individuais.)
            for fee in cls.fees_statement:
                if fee in history:
                    fee_key = f"{composite_key}_{fee_counter}"  # Cria chave única para manter a despesa individualizada

                    # Registra a despesa como movimentação individual
                    aggregated_values[fee_key] = {
                        'Historico': history,
                        'Entrada': inflow,
                        'Saida': outflow,
                        'Plano': plan,
                        'Perfil': profile,
                        'Cod Fundo': fund_code
                    }

                    fee_counter += 1
                    fee_found = True
                    break

            # Ignora a agregação quando o registro é uma despesa
            if fee_found:
                continue

            # AGREGAÇÃO DAS MOVIMENTAÇÕES (Soma valores de registros com a mesma chave.)
            if composite_key in aggregated_values:
                existing_entry = aggregated_values[composite_key]

                # Se ambos positivos, soma entrada
                if existing_entry['Entrada'] > 0 and inflow > 0:
                    existing_entry['Entrada'] += inflow

                # Se ambos negativos, soma saída
                elif existing_entry['Saida'] > 0 and outflow > 0:
                    existing_entry['Saida'] += outflow

                # Caso misto (entrada e saída simultâneas), soma ambas
                else:
                    existing_entry['Entrada'] += inflow
                    existing_entry['Saida'] += outflow

            # Se chave não existe, cria novo registro
            else:
                aggregated_values[composite_key] = {
                    'Historico': history,
                    'Entrada': inflow,
                    'Saida': outflow,
                    'Plano': plan,
                    'Perfil': profile,
                    'Cod Fundo': fund_code
                }

        # CONVERSÃO PARA DATAFRAME (Transforma os dados consolidados em DataFrame.)
        result_df = pd.DataFrame.from_dict(aggregated_values, orient='index').reset_index(drop=True)

        # Reordena colunas para padrão esperado
        result_df = result_df[
            ['Historico', 'Entrada', 'Saida', 'Plano', 'Perfil', 'Cod Fundo']
        ]

        return result_df

#generate_inflow_outflow_difference(): Normaliza balanço entrada/saída entre fundos para refletir o valor líquido da movimentação, mantendo despesas como registros individuais para rastreabilidade.
    @classmethod
    def generate_inflow_outflow_difference(cls, statement):

        # Retorno antecipado se DataFrame vazio
        if statement.empty:
            return pd.DataFrame()

        aggregated_values = {}

        # AGREGAÇÃO POR FUNDO (Agrupa movimentações por fundo, plano e perfil.)
        for _, row in statement.iterrows():
            history = row['Historico']
            fund_code = row['Cod Fundo']
            inflow = row['Entrada']
            outflow = row['Saida']
            plan = row['Plano']
            profile = row['Perfil']

            # Cria chave de agrupamento por fundo, plano e perfil
            composite_key = f"{fund_code}_{plan}_{profile}"

            # SOMA DAS ENTRADAS E SAÍDAS POR FUNDO
            if composite_key in aggregated_values:
                # Soma aos valores existentes para o mesmo fundo, plano e perfil
                aggregated_values[composite_key]['Entrada'] += inflow
                aggregated_values[composite_key]['Saida'] += outflow

                # NORMALIZAÇÃO DO SALDO LÍQUIDO (Aplica regra para manter apenas o valor líquido da movimentação.)
                current_entry = aggregated_values[composite_key]

                # Aplica regra apenas se ambos são modificados (não-zero)
                if current_entry['Entrada'] != 0 and current_entry['Saida'] != 0:
                    balance = current_entry['Entrada'] + current_entry['Saida']

                    # Se balance negativo, move para saída
                    if balance < 0:
                        current_entry['Entrada'] = 0
                        current_entry['Saida'] = balance

                    # Se balance positivo, move para entrada
                    else:
                        current_entry['Saida'] = 0
                        current_entry['Entrada'] = balance

            # Cria um novo registro quando a chave ainda não existe
            else:
                aggregated_values[composite_key] = {
                    'Historico': history,
                    'Cod Fundo': fund_code,
                    'Entrada': inflow,
                    'Saida': outflow,
                    'Plano': plan,
                    'Perfil': profile
                }

        # CONVERSÃO DOS DADOS PARA DATAFRAME (Transforma os dados consolidados em DataFrame.)
        result_df = pd.DataFrame.from_dict(aggregated_values, orient='index').reset_index(drop=True)

        # Reordena colunas para padrão esperado
        result_df = result_df[
            ['Historico', 'Cod Fundo', 'Entrada', 'Saida', 'Plano', 'Perfil']
        ]

        return result_df

#filter_records(): Classifica movimentações em categorias (despesas, resgates, investimentos)
    @classmethod
    def filter_records(cls, statement_df: pd.DataFrame):

        redemption_acquisition_rows = []
        expense_rows = []
        fund_rows = []

        # CLASSIFICAÇÃO DOS REGISTROS DO FLUXO DE CAIXA
        for _, row in statement_df.iterrows():
            history = str(row['Historico'])

            # CLASSIFICAÇÃO DE DESPESAS (Identifica registros com taxas ou despesas no histórico.)
            if any(keyword in history for keyword in cls.fees_statement):
                expense_rows.append(dict(row))

            # CLASSIFICAÇÃO DE MOVIMENTAÇÕES INTERNAS (Registros já refletidos no saldo do fundo.)
            elif 'RESGATE DE COTAS' in history or 'AQUISICAO DE COTAS' in history:
                redemption_acquisition_rows.append(dict(row))
            
            # REGISTROS DE FUNDOS (Mantém registros que não se encaixam nas categorias anteriores para análise posterior.)
            else:
                fund_rows.append(dict(row))

        # CONVERSÃO PARA DATAFRAME (Mantém a estrutura das colunas mesmo sem registros.)
        redemption_acquisition_df = pd.DataFrame(redemption_acquisition_rows)
        updated_statement_df = pd.DataFrame(fund_rows)
        expense_df = pd.DataFrame(expense_rows)

        if not expense_df.empty and 'Historico' in expense_df.columns:
            print(expense_df['Historico'].value_counts().head (20))

        return redemption_acquisition_df, updated_statement_df, expense_df
