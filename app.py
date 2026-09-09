from flask import Flask, render_template, request

app = Flask(__name__)

EQUIPAMENTOS = {
    "BOMBA EP-90PRO": 2677.50,
    "BOMBA HP 60": 2142.00,
    "BOMBA EP-60C": 2142.00,
    "BOMBA MP-30A": 2142.00,
    "BOMBA MP-60A": 2142.00,
    "BOMBA HP30": 3060.00,
    "BOMBA HP30 NEO": 5355.00,
    "BOMBA HP TCI": 6120.00,
    "BOMBA AP-60": 4972.50,
    "BOMBA HP30 PCA": 4590.00,
    "HP 80": 1683.00
}

INSUMOS = {
    "E709E010 - Equipo EP 90 Bolsa": 12.62,
    "E503E000 - Equipo EP 90 Enfit": 7.27,
    "TS-1 - Equipo HP 60 Silicone": 14.15,
    "SXQ0.7 - Equipo HP 60 Transfusão": 10.33,
    "NPZ-D2 - Equipo HP 60 Filtro 0.2": 12.24,
    "E212E02 - Equipo EP 60C Bolsa": 10.10,
    "E112E - Equipo EP 60": 6.58
}

# Função para converter números para o formato financeiro brasileiro
def formatar_brl(valor, decimais=2):
    if valor is None:
        return "0,00"
    # Formata com padrão americano primeiro (ex: 1,234.56)
    v_str = f"{valor:,.{decimais}f}"
    # Troca as vírgulas e pontos para o padrão BR (ex: 1.234,56)
    return v_str.replace(',', 'X').replace('.', ',').replace('X', '.')

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    
    if request.method == 'POST':
        equipamentos_selecionados = request.form.getlist('equipamento[]')
        qtds_equipamentos = request.form.getlist('qtd_equipamentos[]')
        
        insumos_selecionados = request.form.getlist('insumo[]')
        qtds_insumos = request.form.getlist('qtd_insumos[]')
        
        # Converte para inteiro (remove o .0 visual)
        tempo_contrato = int(float(request.form['tempo_contrato']))
        # Margem pode ter decimal, mas formatamos para exibir bonito
        margem_lucro = float(request.form['margem_lucro'])
        
        # 1. Somando o custo de TODAS as bombas
        custo_total_equipamentos = 0
        for i in range(len(equipamentos_selecionados)):
            nome_eq = equipamentos_selecionados[i]
            # Quantidade forçada como Inteiro
            qtd_eq = int(float(qtds_equipamentos[i]))
            custo_total_equipamentos += (qtd_eq * EQUIPAMENTOS[nome_eq])
            
        custo_mensal_equipamentos = custo_total_equipamentos / tempo_contrato
        
        # 2. Somando a quantidade de TODOS os insumos para diluição (como inteiro)
        qtd_total_insumos = sum([int(float(qtd)) for qtd in qtds_insumos])
        
        # 3. Fator de Comodato (FC)
        fator_comodato = 0
        if qtd_total_insumos > 0:
            fator_comodato = custo_mensal_equipamentos / qtd_total_insumos
            
        # 4. Cálculo de Preços e Faturamentos
        detalhes_insumos = []
        faturamento_mensal_total = 0
        
        for i in range(len(insumos_selecionados)):
            nome_ins = insumos_selecionados[i]
            qtd_ins = int(float(qtds_insumos[i])) # Quantidade inteira
            custo_base = INSUMOS[nome_ins]
            
            preco_com_markup = custo_base * (1 + (margem_lucro / 100))
            preco_venda = preco_com_markup + fator_comodato
            
            faturamento_mensal_item = preco_venda * qtd_ins
            faturamento_mensal_total += faturamento_mensal_item
            
            detalhes_insumos.append({
                'nome': nome_ins,
                'qtd': qtd_ins,
                'custo_base': formatar_brl(custo_base),
                'preco_com_markup': formatar_brl(preco_com_markup),
                'preco_venda': formatar_brl(preco_venda),
                'faturamento_mensal': formatar_brl(faturamento_mensal_item)
            })
            
        faturamento_contrato_total = faturamento_mensal_total * tempo_contrato
        
        # Formatando % de lucro (tira o .0 se for inteiro)
        margem_exibicao = f"{margem_lucro:g}".replace('.', ',')
            
        resultado = {
            'custo_total_equipamentos': formatar_brl(custo_total_equipamentos),
            'custo_mensal_equipamentos': formatar_brl(custo_mensal_equipamentos),
            'qtd_total_insumos': qtd_total_insumos, # Inteiro limpo
            'fator_comodato': formatar_brl(fator_comodato, 4), # Mantém 4 casas no FC, mas com vírgula
            'detalhes_insumos': detalhes_insumos,
            'faturamento_mensal_total': formatar_brl(faturamento_mensal_total),
            'faturamento_contrato_total': formatar_brl(faturamento_contrato_total),
            'margem_lucro': margem_exibicao,
            'tempo_contrato': tempo_contrato
        }
        
    return render_template('index.html', equipamentos=EQUIPAMENTOS, insumos=INSUMOS, resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
