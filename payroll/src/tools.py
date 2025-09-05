def criar_lancamento_contabil(conta, valor, d_c, historico, plano, perfil):
    return {
        'Conta contabil': conta,
        'Valor': valor,
        'D/C': d_c,
        'Historico de lancamento': historico,
        'CC': 2,
        'Plano': plano,
        'Perfil': perfil
    }