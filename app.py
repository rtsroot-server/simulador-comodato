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

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    
    if request.method == 'POST':
        equipamentos_selecionados = request.form.getlist('equipamento[]')
        qtds_equipamentos = request.form.getlist('qtd_equipamentos[]')
        
        insumos_selecionados = request.form.getlist('insumo[]')
        qtds_insumos = request.form.getlist('qtd_insumos[]')
        
        tempo_contrato = float(request.form['tempo_contrato'])
        margem_lucro = float(request.form['margem_lucro'])
        
        # 1. Somando o custo de TODAS as bombas
        custo_total_equipamentos = 0
        for i in range(len(equipamentos_selecionados)):
            nome_eq = equipamentos_selecionados[i]
            qtd_eq = float(qtds_equipamentos[i])
            custo_total_equipamentos += (qtd_eq * EQUIPAMENTOS[nome_eq])
            
        custo_mensal_equipamentos = custo_total_equipamentos / tempo_contrato
        
        # 2. Somando a quantidade de TODOS os insumos para diluição
        qtd_total_insumos = sum([float(qtd) for qtd in qtds_insumos])
        
        # 3. Fator de Comodato (FC)
        fator_comodato = 0
        if qtd_total_insumos > 0:
            fator_comodato = custo_mensal_equipamentos / qtd_total_insumos
            
        # 4. NOVA MATEMÁTICA: Markup apenas no Insumo!
        detalhes_insumos = []
        for i in range(len(insumos_selecionados)):
            nome_ins = insumos_selecionados[i]
            qtd_ins = float(qtds_insumos[i])
            custo_base = INSUMOS[nome_ins]
            
            # Aplica a margem SÓ no custo do equipo
            preco_com_markup = custo_base * (1 + (margem_lucro / 100))
            
            # Soma o Fator Comodato depois da margem (apenas repasse de custo)
            preco_venda = preco_com_markup + fator_comodato
            
            detalhes_insumos.append({
                'nome': nome_ins,
                'qtd': qtd_ins,
                'custo_base': custo_base,
                'preco_com_markup': round(preco_com_markup, 2),
                'preco_venda': round(preco_venda, 2)
            })
            
        resultado = {
            'custo_total_equipamentos': round(custo_total_equipamentos, 2),
            'custo_mensal_equipamentos': round(custo_mensal_equipamentos, 2),
            'qtd_total_insumos': round(qtd_total_insumos, 2),
            'fator_comodato': round(fator_comodato, 4),
            'detalhes_insumos': detalhes_insumos,
            'margem_lucro': margem_lucro,
            'tempo_contrato': tempo_contrato
        }
        
    return render_template('index.html', equipamentos=EQUIPAMENTOS, insumos=INSUMOS, resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
