from flask import Flask, render_template, request

app = Flask(__name__)

# Dados extraídos da planilha oficial "planilha_precos (2).xlsx"
EQUIPAMENTOS = {
    "BOMBA DE SERINGA AP-30 MEDCAPTAIN": 2926.51,
    "BOMBA DE INFUSÃO AP-60 MEDCAPTAIN": 2926.51,
    "BOMBA ENTERAL EP-60C MEDCAPTAIN": 1614.27,
    "BOMBA ENTERAL MEDCAPTAIN EP-90": 1984.77,
    "BOMBA DE SERINGA HP 30 MEDCAPTAIN": 2156.83,
    "BOMBA DE SERINGA MEDCAPTAIN COM FUNÇÃO PCA": 2591.54,
    "BOMBA DE INFUSAO MEDCAPTAIN HP-60 PRO": 2727.42,
    "BOMBA DE INFUSÃO 3 EM 1 HP 60 MEDCAPTAIN": 1733.79,
    "BOMBA DE SERINGA HP TCI MEDCAPTAIN": 4630.98,
    "GABINETE PARA ESTACAO MEDCAPTAIN HP-80": 1298.77,
    "CONTROLADORA PARA ESTACAO HP-80": 1298.77,
    "BOMBA DE SERINGA MEDCAPTAIN MP-30A": 1546.24,
    "BOMBA DE INFUSÃO UNIVERSAL - MEDCAPTAIN (MP-60)": 2782.17,
    "BOMBA DE INFUSÃO UNIVERSAL - MEDCAPTAIN (MP-60A)": 2252.51,
    "ESTAÇÃO DE TRABALHO PARA BOMBAS DE INFUSÃO MP-60": 2667.90,
    "CARRINHO DE TRANSPORTE / SUPORTE MOVEL": 1337.32,
    "BOMBA TVP PADRAO COM 1 CABO DE ALIM E 2 CONJ DE PNEU": 2188.25,
    "VIDEOLARINGOSCOPIO MEDCAPTAIN": 4206.67
}

INSUMOS = {
    "EQUIPO PARENTERAL DEDICADO FOTOSSENSIVEL HP-60 (MX50)": 10.85,
    "EQUIPO PARENTERAL DEDICADO FOTO HP-60 (MX C/50)": 13.52,
    "EQUIPO PARENTERAL DEDICADO FOTOSSENSIVEL HP-60 (MX C/50)": 6.03,
    "EQUIPO PARENTERAL MEDCAPTAIN - BPQ-Y (MX C/50)": 3.36,
    "EQUIPO ENTERAL MEDCAPTAIN - E112E (MX30)": 6.52,
    "EQUIPO ENTERAL DEDICADO PARA EP-60C COM BOLSA 1.2L (MX30)": 8.51,
    "EQUIPO ENTERAL DEDICADO PARA BOMBA HP-60 (MX50)": 6.24,
    "EQUIPO ENTERAL DEDICADO PARA BOMBA HP-60 COM BOLSA 1L (MX50)": 9.82,
    "EQUIPO ENTERAL DEDICADO PARA BOMBA EP 90 LANCETA (Mx30)": 6.37,
    "EQUIPO ENTERAL DEDICADO PARA BOMBA EP 90 ENFIT (Mx30)": 6.37,
    "EQUIPO ENTERAL DEDICADO PARA BOMBA EP 90 C/ BOLSA (Mx30)": 11.06,
    "EQUIPO PARENTERAL FOTOSSENSIVEL MEDCAPTAIN-JMB-0.2 (MX C/50)": 6.49,
    "LAMINA DESCARTAVEL TAMANHO 1 PARA VIDEOLARINGOSCOPIO VS-10S": 21.69,
    "LAMINA DESCARTAVEL TAMANHO 2 PARA VIDEOLARINGOSCOPIO VS-10S": 21.64,
    "LAMINA DESCARTAVEL TAMANHO 3 PARA VIDEOLARINGOSCOPIO VS-10S": 20.24,
    "LAMINA DESC. P/ INTUBAÇÃO DIFICIL PARA VIDEOLARINGOS VS-10S": 22.62,
    "LAMINA DESCARTAVEL TAMANHO 4 PARA VIDEOLARINGOSCOPIO VS-10S": 20.10,
    "SENSOR DE GOTAS PARA EQUIPO MEDCAPTAIN": 191.04,
    "EQUIPO PARENTERAL DEDICADO DESCARTAVEL BOMBA HP-60 (MX50) (NPZ-D2)": 10.36,
    "EQUIPO PARENTERAL DEDICADO DESCARTAVEL BOMBA HP-60 (MX50) (NPZ-F-S1)": 3.57,
    "EQUIPO NPT DEDICADO DESCARTAVEL PARA BOMBA HP-60 (Mx50)": 10.05,
    "EQUIPO PARENTERAL DEDICADO DESCARTAVEL BOMBA HP-60 (MX50) (NPZ-W-S1)": 8.11,
    "EQUIPO PARENTERAL DEDICADO DESCARTAVEL BOMBA HP-60 (MX50) (NPZ-W-S2)": 5.25,
    "EQUIPO BURETA DEDICADO DESCARTAVEL PARA BOMBA HP-60 (Mx50)": 16.87,
    "EQUIPO BURETA DEDICADO DESCARTAVEL BOMBA HP-60 (Mx50)": 14.27,
    "EQUIPO DEDICADO PARA TRANFUSÃO PARA BOMBA HP-60 (MX50)": 8.75,
    "PERNEIRA PADRÃO PARA TVP COXA (TAM P)": 5105.86,
    "PERNEIRA PADRÃO PARA TVP COXA (TAM M)": 12764.78,
    "PERNEIRA PADRÃO PARA TVP COXA (TAM GG)": 5105.90,
    "PERNEIRA PADRAO PARA TVP PE (TAM UNICO)": 1945.07,
    "PERNEIRA REUTILIZAVEL PARA TVP COXA (TAM P)": 2127.49,
    "PERNEIRA REUTILIZAVEL PARA TVP COXA (TAM M)": 21274.67,
    "PERNEIRA REUTILIZAVEL PARA TVP COXA (TAM GG)": 9786.52,
    "PERNEIRA REUTILIZAVEL PARA TVP PE (TAM UNICO)": 1458.83,
    "EQUIPO PARENTERAL MEDCAPTAIN PVC FREE TS-1 MX/50": 12.81
}

def formatar_brl(valor, decimais=2):
    if valor is None:
        return "0,00"
    v_str = f"{valor:,.{decimais}f}"
    return v_str.replace(',', 'X').replace('.', ',').replace('X', '.')

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    
    if request.method == 'POST':
        equipamentos_selecionados = request.form.getlist('equipamento[]')
        qtds_equipamentos = request.form.getlist('qtd_equipamentos[]')
        
        insumos_selecionados = request.form.getlist('insumo[]')
        qtds_insumos = request.form.getlist('qtd_insumos[]')
        
        tempo_contrato = int(float(request.form['tempo_contrato']))
        margem_lucro = float(request.form['margem_lucro'])
        
        custo_total_equipamentos = 0
        for i in range(len(equipamentos_selecionados)):
            nome_eq = equipamentos_selecionados[i]
            qtd_eq = int(float(qtds_equipamentos[i]))
            custo_total_equipamentos += (qtd_eq * EQUIPAMENTOS[nome_eq])
            
        custo_mensal_equipamentos = custo_total_equipamentos / tempo_contrato
        qtd_total_insumos = sum([int(float(qtd)) for qtd in qtds_insumos])
        
        fator_comodato = 0
        if qtd_total_insumos > 0:
            fator_comodato = custo_mensal_equipamentos / qtd_total_insumos
            
        detalhes_insumos = []
        faturamento_mensal_total = 0
        
        for i in range(len(insumos_selecionados)):
            nome_ins = insumos_selecionados[i]
            qtd_ins = int(float(qtds_insumos[i]))
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
        margem_exibicao = f"{margem_lucro:g}".replace('.', ',')
            
        resultado = {
            'custo_total_equipamentos': formatar_brl(custo_total_equipamentos),
            'custo_mensal_equipamentos': formatar_brl(custo_mensal_equipamentos),
            'qtd_total_insumos': qtd_total_insumos,
            'fator_comodato': formatar_brl(fator_comodato, 4),
            'detalhes_insumos': detalhes_insumos,
            'faturamento_mensal_total': formatar_brl(faturamento_mensal_total),
            'faturamento_contrato_total': formatar_brl(faturamento_contrato_total),
            'margem_lucro': margem_exibicao,
            'tempo_contrato': tempo_contrato
        }
        
    return render_template('index.html', equipamentos=EQUIPAMENTOS, insumos=INSUMOS, resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
