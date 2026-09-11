from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Dados oficiais com CÓDIGO + DESCRIÇÃO
EQUIPAMENTOS = {
    "AP-30 - BOMBA DE SERINGA AP-30 MEDCAPTAIN": 2926.51,
    "AP-60 - BOMBA DE INFUSÃO AP-60 MEDCAPTAIN": 2926.51,
    "EP-60C - BOMBA ENTERAL EP-60C MEDCAPTAIN": 1614.27,
    "EP-90PRO - BOMBA ENTERAL MEDCAPTAIN EP-90": 1984.77,
    "HP-30 - BOMBA DE SERINGA HP 30 MEDCAPTAIN": 2156.83,
    "HP-30 PCA - BOMBA DE SERINGA MEDCAPTAIN COM FUNÇÃO PCA": 2591.54,
    "HP-60 PRO - BOMBA DE INFUSAO MEDCAPTAIN HP-60 PRO": 2727.42,
    "HP-60C - BOMBA DE INFUSÃO 3 EM 1 HP 60 MEDCAPTAIN": 1733.79,
    "HP-TCI - BOMBA DE SERINGA HP TCI MEDCAPTAIN": 4630.98,
    "HP80B-CTO-08 - GABINETE PARA ESTACAO MEDCAPTAIN HP-80": 1298.77,
    "HP80C-CTO-02 - CONTROLADORA PARA ESTACAO HP-80": 1298.77,
    "MP-30A - BOMBA DE SERINGA MEDCAPTAIN MP-30A": 1546.24,
    "MP-60 - BOMBA DE INFUSÃO UNIVERSAL - MEDCAPTAIN": 2782.17,
    "MP-60A - BOMBA DE INFUSÃO UNIVERSAL - MEDCAPTAIN": 2252.51,
    "MP-80 - ESTAÇÃO DE TRABALHO PARA BOMBAS DE INFUSÃO MP-60": 2667.90,
    "S-140 - CARRINHO DE TRANSPORTE / SUPORTE MOVEL": 1337.32,
    "TP-100 - BOMBA TVP PADRAO COM 1 CABO DE ALIM E 2 CONJ DE PNEU": 2188.25,
    "VS-10S - VIDEOLARINGOSCOPIO MEDCAPTAIN": 4206.67
}

INSUMOS = {
    "BGP-FW-D2 - EQUIPO PARENTERAL DEDICADO FOTOSSENSIVEL HP-60 (MX50)": 10.85,
    "BGP-FW-S1 - EQUIPO PARENTERAL DEDICADO FOTO HP-60 (MX C/50)": 13.52,
    "BGP-FW-S2 - EQUIPO PARENTERAL DEDICADO FOTOSSENSIVEL HP-60 (MX C/50)": 6.03,
    "BPQ-Y - EQUIPO PARENTERAL MEDCAPTAIN  - BPQ-Y (MX C/50)": 3.36,
    "E112E - EQUIPO ENTERAL MEDCAPTAIN - E112E (MX30)": 6.52,
    "E212E02 - EQUIPO ENTERAL DEDICADO PARA EP-60C COM BOLSA 1.2L (MX30)": 8.51,
    "E212M01 - EQUIPO ENTERAL DEDICADO PARA BOMBA HP-60 (MX50)": 6.24,
    "E214M01 - EQUIPO ENTERAL DEDICADO PARA BOMBA HP-60 COM BOLSA 1L (MX50)": 9.82,
    "E502E000 - EQUIPO ENTERAL DEDICADO PARA BOMBA EP 90 LANCETA (Mx30)": 6.37,
    "E503E000 - EQUIPO ENTERAL DEDICADO PARA BOMBA EP 90 ENFIT (Mx30)": 6.37,
    "E709E010 - EQUIPO ENTERAL DEDICADO PARA BOMBA EP 90  C/ BOLSA (Mx30)": 11.06,
    "JMB-0.2 - EQUIPO PARENTERAL FOTOSSENSIVEL MEDCAPTAIN-JMB-0.2 (MX C/50)": 6.49,
    "M1 - LAMINA DESCARTAVEL TAMANHO 1 PARA VIDEOLARINGOSCOPIO VS-10S": 21.69,
    "M2 - LAMINA DESCARTAVEL TAMANHO 2 PARA VIDEOLARINGOSCOPIO VS-10S": 21.64,
    "M3 - LAMINA DESCARTAVEL TAMANHO 3 PARA VIDEOLARINGOSCOPIO VS-10S": 20.24,
    "M3D - LAMINA DESC. P/ INTUBAÇÃO DIFICIL PARA VIDEOLARINGOS VS-10S": 22.62,
    "M4 - LAMINA DESCARTAVEL TAMANHO 4 PARA VIDEOLARINGOSCOPIO VS-10S": 20.10,
    "MEDCAPT-SENSOR - SENSOR DE GOTAS PARA EQUIPO MEDCAPTAIN": 191.04,
    "NPZ-D2 - EQUIPO PARENTERAL DEDICADO DESCARTAVEL BOMBA HP-60 (MX50)": 10.36,
    "NPZ-F-S1 - EQUIPO PARENTERAL DEDICADO DESCARTAVEL BOMBA HP-60 (MX50)": 3.57,
    "NPZ-S1 - EQUIPO NPT DEDICADO DESCARTAVEL PARA BOMBA HP-60 (Mx50)": 10.05,
    "NPZ-W-S1 - EQUIPO PARENTERAL DEDICADO DESCARTAVEL BOMBA HP-60 (MX50)": 8.11,
    "NPZ-W-S2 - EQUIPO PARENTERAL DEDICADO DESCARTAVEL  BOMBA HP-60 (MX50)": 5.25,
    "NPZ-WP-D3 - EQUIPO BURETA DEDICADO DESCARTAVEL PARA BOMBA HP-60 (Mx50)": 16.87,
    "NPZ-WP-D4 - EQUIPO BURETA DEDICADO DESCARTAVEL BOMBA HP-60 (Mx50)": 14.27,
    "SXQ0.7 - EQUIPO DEDICADO PARA TRANFUSÃO PARA BOMBA HP-60 (MX50)": 8.75,
    "TPS011 - PERNEIRA PADRÃO PARA TVP COXA (TAM P)": 5105.86,
    "TPS012 - PERNEIRA PADRÃO PARA TVP COXA (TAM M)": 12764.78,
    "TPS014 - PERNEIRA PADRÃO PARA TVP COXA (TAM GG)": 5105.90,
    "TPS035 - PERNEIRA PADRAO PARA TVP PE (TAM UNICO)": 1945.07,
    "TPS111 - PERNEIRA REUTILIZAVEL PARA TVP COXA (TAM P)": 2127.49,
    "TPS112 - PERNEIRA REUTILIZAVEL PARA TVP COXA (TAM M)": 21274.67,
    "TPS114 - PERNEIRA REUTILIZAVEL PARA TVP COXA (TAM GG)": 9786.52,
    "TPS135 - PERNEIRA REUTILIZAVEL PARA TVP PE (TAM UNICO)": 1458.83,
    "TS-1 - EQUIPO PARENTERAL MEDCAPTAIN PVC FREE TS-1 MX/50": 12.81
}

# Atualizando Mapa de Vínculos com os novos Códigos
MAPA_VINCULOS = {}
for eq in EQUIPAMENTOS.keys():
    compatibilidade = []
    if 'HP-60' in eq or 'HP 60' in eq: kw = ['HP-60', 'HP 60', 'TS-1', 'JMB', 'BPQ', 'NPZ', 'SXQ']
    elif 'EP-90' in eq or 'EP 90' in eq: kw = ['EP-90', 'EP 90', 'E502', 'E503', 'E709']
    elif 'EP-60' in eq or 'EP 60' in eq: kw = ['EP-60', 'EP 60', 'E112', 'E212E02']
    elif 'VS-10' in eq or 'VIDEOLARINGO' in eq: kw = ['LAMINA', 'M1', 'M2', 'M3', 'M4']
    elif 'TVP' in eq: kw = ['PERNEIRA', 'TPS']
    else: kw = ['EQUIPO', 'SENSOR', 'E212', 'E214'] # Genéricos para MP/AP/Estações

    for ins in INSUMOS.keys():
        if any(k in ins for k in kw):
            compatibilidade.append(ins)
    MAPA_VINCULOS[eq] = compatibilidade if compatibilidade else list(INSUMOS.keys())

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
        
        tempo_depreciacao = int(float(request.form['tempo_depreciacao']))
        tempo_contrato = int(float(request.form['tempo_contrato']))
        margem_lucro = float(request.form['margem_lucro'])
        
        # 1. Custo das máquinas e Lista para Tabela
        custo_total_equipamentos = 0
        detalhes_equipamentos = []
        
        for i in range(len(equipamentos_selecionados)):
            nome_eq = equipamentos_selecionados[i]
            qtd_eq = int(float(qtds_equipamentos[i]))
            custo_total_equipamentos += (qtd_eq * EQUIPAMENTOS[nome_eq])
            
            # Adiciona o equipamento na lista de resumo
            detalhes_equipamentos.append({
                'nome': nome_eq,
                'qtd': qtd_eq
            })
            
        # 2. Diluição pelo tempo de DEPRECIAÇÃO
        custo_mensal_equipamentos = custo_total_equipamentos / tempo_depreciacao
        
        # 3. Fator Comodato (FC)
        qtd_total_insumos = sum([int(float(qtd)) for qtd in qtds_insumos])
        fator_comodato = custo_mensal_equipamentos / qtd_total_insumos if qtd_total_insumos > 0 else 0
            
        # 4. Faturamento Insumos
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
                'preco_venda': formatar_brl(preco_venda),
                'faturamento_mensal': formatar_brl(faturamento_mensal_item)
            })
            
        faturamento_contrato_total = faturamento_mensal_total * tempo_contrato
            
        resultado = {
            'detalhes_equipamentos': detalhes_equipamentos,
            'custo_total_equipamentos': formatar_brl(custo_total_equipamentos),
            'custo_mensal_equipamentos': formatar_brl(custo_mensal_equipamentos),
            'qtd_total_insumos': qtd_total_insumos,
            'fator_comodato': formatar_brl(fator_comodato, 4),
            'detalhes_insumos': detalhes_insumos,
            'faturamento_mensal_total': formatar_brl(faturamento_mensal_total),
            'faturamento_contrato_total': formatar_brl(faturamento_contrato_total),
            'margem_lucro': f"{margem_lucro:g}".replace('.', ','),
            'tempo_contrato': tempo_contrato,
            'tempo_depreciacao': tempo_depreciacao
        }
        
    return render_template('index.html', 
                           equipamentos=list(EQUIPAMENTOS.keys()), 
                           insumos=list(INSUMOS.keys()), 
                           mapa_vinculos=MAPA_VINCULOS, 
                           resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
