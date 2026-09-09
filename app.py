from flask import Flask, render_template, request

app = Flask(__name__)

# Nosso "Mini Banco de Dados" com os custos reais (seguros no backend)
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
        # 1. Puxando os NOMES que o vendedor selecionou na tela
        nome_equipamento = request.form['equipamento']
        nome_insumo = request.form['insumo']
        
        # 2. Buscando automaticamente os CUSTOS no nosso "banco de dados" acima
        custo_equipamento = EQUIPAMENTOS[nome_equipamento]
        custo_insumo = INSUMOS[nome_insumo]
        
        # 3. Puxando as quantidades digitadas
        qtd_equipamentos = float(request.form['qtd_equipamentos'])
        tempo_contrato = float(request.form['tempo_contrato'])
        qtd_insumos = float(request.form['qtd_insumos'])
        margem_lucro = float(request.form['margem_lucro'])
        
        # 4. Fazendo a matemática da diluição
        custo_total_equipamentos = qtd_equipamentos * custo_equipamento
        custo_mensal_equipamentos = custo_total_equipamentos / tempo_contrato
        
        fator_comodato = custo_mensal_equipamentos / qtd_insumos
        custo_com_fc = custo_insumo + fator_comodato
        preco_venda_final = custo_com_fc * (1 + (margem_lucro / 100))
        
        # 5. Organizando o resultado para mandar para a tela
        resultado = {
            'equipamento_escolhido': nome_equipamento,
            'insumo_escolhido': nome_insumo,
            'custo_equip_oculto': custo_equipamento,
            'custo_insumo_oculto': custo_insumo,
            'fator_comodato': round(fator_comodato, 4),
            'custo_com_fc': round(custo_com_fc, 2),
            'preco_venda_final': round(preco_venda_final, 2)
        }
        
    return render_template('index.html', equipamentos=EQUIPAMENTOS, insumos=INSUMOS, resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)