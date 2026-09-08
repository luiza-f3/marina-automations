fund_name_mapping = {
    # Taxas
    r'^TX DE CONTROLADORIA.*$': 'TAXA DE CONTROLADORIA',
    r'^TAXA DE CONTROL.? S/ TX.*$': 'TAXA DE CONTROLADORIA',
    r'^Tx de Controladoria s/ Tx de Admin. [BBDC] Bruta.*$': 'TAXA DE CONTROLADORIA',

    r'^TAXA DE CUSTODIA A PAGAR.*$': 'TAXA DE ADMINISTRACAO',

    r'^TX CUSTODIA BRUTA.*$': 'TAXA DE CUSTODIA',
    r'^TAXA DE CUSTODIA BRUTA$': 'TAXA DE CUSTODIA',
    r'^TAXA DE CUSTODIA APROPRIADA$': 'TAXA DE CUSTODIA',

    # Despesas
    r'^DESPESA DE CUSTO CETIP.*$': 'CUSTO CETIP',
    r'^CUSTO CETIP.*$': 'CUSTO CETIP',

    r'^DESPESA DE B 10 - TARIFA DE LIQUIDACAO FINANCEIRA.*$': 'TARIFA DE LIQUIDACAO FINANCEIRA (DESPESA B 10)',
    r'^APLICACAO - TARIFA DE LIQUIDACAO FINANCEIRA$': 'TARIFA DE LIQUIDACAO FINANCEIRA (DESPESA B 10)',
    r'^TARIFA DE LIQUIDACAO FINANCEIRA$': 'TARIFA DE LIQUIDACAO FINANCEIRA (DESPESA B 10)',

    # Ajustes
    r'^AJUSTE DE TARIFA DE LIQUIDACAO FINANCEIRA$': 'TARIFA DE LIQUIDACAO FINANCEIRA (AJUSTE)',

    r'^AJUSTE DE TAXA CETIP$': 'TAXA CETIP (AJUSTE)',
    r'^AJUSTE TAXA CETIP.*$': 'TAXA CETIP (AJUSTE)',

    # Fundos
    r'^ALTERNATIVOS MIR FIM$': 'ALTERNATIVOS MIRANTE FICM',
    r'^BB ACOES GLOBAIS FIA$': 'BB ACOES GL HEDGE IE',
    r'^FIC DE FI ACOES IBRX$': 'FIC DE FI ACOES IBRX',

    # IOF
    r'^IOF .*$': 'IOF',
    r'^17760$': '017760',

    # Controladoria - REMUNERACAO VARIAVEL
    r'(?i)^controladoria - remuneracao variavel - 1 tri26$': 'TAXA DE CONTROLADORIA (REMUNERACAO VARIAVEL)',
    r'(?i)^controladoria - remuneracao variavel - 3 tri26$': 'TAXA DE CONTROLADORIA (REMUNERACAO VARIAVEL)',
    r'(?i)^controladoria - remuneracao variavel - 4 tri26$': 'TAXA DE CONTROLADORIA (REMUNERACAO VARIAVEL)',

    # Custodia - REMUNERACAO VARIAVEL
    r'(?i)^custodia - remuneracao variavel - 1 tri 2026$': 'TAXA DE CUSTODIA (REMUNERACAO VARIAVEL)',
    r'(?i)^custodia - remuneracao variavel - 3 tri 2026$': 'TAXA DE CUSTODIA (REMUNERACAO VARIAVEL)',
    r'(?i)^custodia - remuneracao variavel - 4 tri 2026$': 'TAXA DE CUSTODIA (REMUNERACAO VARIAVEL)',
}