from flask import Flask, render_template, jsonify, request
import json
import random
from datetime import datetime

app = Flask(__name__)

# Variável global para armazenar o resultado do último sorteio
ultimo_resultado = None
historico_sorteios = []

def carregar_dados():
    """Carrega os dados dos arquivos JSON"""
    with open('vagas.json', 'r', encoding='utf-8') as f:
        vagas = json.load(f)
    
    with open('apartamentos.json', 'r', encoding='utf-8') as f:
        apartamentos = json.load(f)
    
    return vagas.copy(), apartamentos.copy()

def realizar_sorteio():
    """Executa a lógica completa de sorteio"""
    vagas, apartamentos = carregar_dados()
    resultado_final = {}
    
    # 1º SORTEIO: VAGAS PCD
    aps_pcd = [ap for ap in apartamentos if ap.get("pcd") is True]
    vagas_pcd = [v for v in vagas if v.get("PCD") is True]
    random.shuffle(vagas_pcd)
    
    sorteio_pcd = []
    for ap in aps_pcd:
        if vagas_pcd:
            vaga_sorteada = vagas_pcd.pop(0)
            resultado_final[ap["ap"]] = vaga_sorteada
            sorteio_pcd.append({
                "apartamento": ap["ap"],
                "vaga": vaga_sorteada,
                "bloco": ap["bloco"]
            })
            apartamentos.remove(ap)
            vagas.remove(vaga_sorteada)
    
    # 2º SORTEIO: VAGAS DESCOBERTAS
    vagas_descobertas = [v for v in vagas if v.get("coberta") is False]
    random.shuffle(vagas_descobertas)
    
    aps_para_descobertas = [ap for ap in apartamentos if ap.get("tipo") == "vaga descoberta"]
    random.shuffle(aps_para_descobertas)
    
    sorteio_descobertas = []
    for ap in aps_para_descobertas:
        if vagas_descobertas:
            vaga_sorteada = vagas_descobertas.pop(0)
            resultado_final[ap["ap"]] = vaga_sorteada
            sorteio_descobertas.append({
                "apartamento": ap["ap"],
                "vaga": vaga_sorteada,
                "bloco": ap["bloco"]
            })
            apartamentos.remove(ap)
            vagas.remove(vaga_sorteada)
    
    # 3º SORTEIO: BLOCOS (SS2 / SS3) & AMPLA CONCORRÊNCIA
    vagas_bloco_A = [v for v in vagas if v["loca"] in ["SS2", "SS3"] and v["Facil_acesso"] == "A"]
    vagas_bloco_B = [v for v in vagas if v["loca"] in ["SS2", "SS3"] and v["Facil_acesso"] == "B"]
    vagas_ampla = [v for v in vagas if v["Facil_acesso"] == "Ampla concorencia" or v["loca"] in ["SS1", "SS4"]]
    
    aps_bloco_A = [ap for ap in apartamentos if ap["bloco"] == "A"]
    aps_bloco_B = [ap for ap in apartamentos if ap["bloco"] == "B"]
    
    random.shuffle(vagas_bloco_A)
    random.shuffle(vagas_bloco_B)
    
    sorteio_bloco_a = []
    for ap in list(aps_bloco_A):
        if vagas_bloco_A:
            vaga_sorteada = vagas_bloco_A.pop(0)
            resultado_final[ap["ap"]] = vaga_sorteada
            sorteio_bloco_a.append({
                "apartamento": ap["ap"],
                "vaga": vaga_sorteada,
                "bloco": ap["bloco"]
            })
            aps_bloco_A.remove(ap)
            vagas.remove(vaga_sorteada)
    
    sorteio_bloco_b = []
    for ap in list(aps_bloco_B):
        if vagas_bloco_B:
            vaga_sorteada = vagas_bloco_B.pop(0)
            resultado_final[ap["ap"]] = vaga_sorteada
            sorteio_bloco_b.append({
                "apartamento": ap["ap"],
                "vaga": vaga_sorteada,
                "bloco": ap["bloco"]
            })
            aps_bloco_B.remove(ap)
            vagas.remove(vaga_sorteada)
    
    aps_restantes = aps_bloco_A + aps_bloco_B
    vagas_restantes_total = vagas_bloco_A + vagas_bloco_B + vagas_ampla
    random.shuffle(vagas_restantes_total)
    
    sorteio_ampla = []
    for ap in aps_restantes:
        if vagas_restantes_total:
            vaga_sorteada = vagas_restantes_total.pop(0)
            resultado_final[ap["ap"]] = vaga_sorteada
            sorteio_ampla.append({
                "apartamento": ap["ap"],
                "vaga": vaga_sorteada,
                "bloco": ap["bloco"]
            })
    
    return {
        "timestamp": datetime.now().isoformat(),
        "sorteio_pcd": sorteio_pcd,
        "sorteio_descobertas": sorteio_descobertas,
        "sorteio_bloco_a": sorteio_bloco_a,
        "sorteio_bloco_b": sorteio_bloco_b,
        "sorteio_ampla": sorteio_ampla,
        "resultado_completo": resultado_final
    }

@app.route('/')
def index():
    """Tela principal"""
    vagas, apartamentos = carregar_dados()
    
    # Estatísticas gerais
    total_vagas = len(vagas)
    total_apartamentos = len(apartamentos)
    vagas_cobertas = len([v for v in vagas if v.get("coberta")])
    vagas_descobertas = len([v for v in vagas if not v.get("coberta")])
    vagas_pcd = len([v for v in vagas if v.get("PCD")])
    aps_pcd = len([ap for ap in apartamentos if ap.get("pcd")])
    aps_descobertas = len([ap for ap in apartamentos if ap.get("tipo") == "vaga descoberta"])
    
    stats = {
        "total_vagas": total_vagas,
        "total_apartamentos": total_apartamentos,
        "vagas_cobertas": vagas_cobertas,
        "vagas_descobertas": vagas_descobertas,
        "vagas_pcd": vagas_pcd,
        "aps_pcd": aps_pcd,
        "aps_descobertas": aps_descobertas
    }
    
    return render_template('index.html', stats=stats, tem_resultado=ultimo_resultado is not None)

@app.route('/vagas')
def vagas():
    """Tela de vagas disponíveis"""
    vagas_data, _ = carregar_dados()
    
    # Organizar vagas por categorias
    vagas_por_local = {}
    for vaga in vagas_data:
        local = vaga["loca"]
        if local not in vagas_por_local:
            vagas_por_local[local] = []
        vagas_por_local[local].append(vaga)
    
    return render_template('vagas.html', vagas_por_local=vagas_por_local, vagas_data=vagas_data)

@app.route('/unidades')
def unidades():
    """Tela de unidades"""
    _, apartamentos_data = carregar_dados()
    
    # Organizar por bloco
    aps_bloco_a = [ap for ap in apartamentos_data if ap["bloco"] == "A"]
    aps_bloco_b = [ap for ap in apartamentos_data if ap["bloco"] == "B"]
    
    return render_template('unidades.html', 
                         aps_bloco_a=aps_bloco_a, 
                         aps_bloco_b=aps_bloco_b,
                         apartamentos=apartamentos_data)

@app.route('/sortear')
def sortear():
    """Tela de sorteio"""
    vagas_data, apartamentos_data = carregar_dados()
    
    # Informações para a tela de sorteio
    info = {
        "total_vagas": len(vagas_data),
        "total_apartamentos": len(apartamentos_data),
        "vagas_pcd": len([v for v in vagas_data if v.get("PCD")]),
        "aps_pcd": len([ap for ap in apartamentos_data if ap.get("pcd")]),
        "vagas_descobertas": len([v for v in vagas_data if not v.get("coberta")]),
        "aps_descobertas": len([ap for ap in apartamentos_data if ap.get("tipo") == "vaga descoberta"])
    }
    
    return render_template('sortear.html', info=info)

@app.route('/api/executar-sorteio', methods=['POST'])
def executar_sorteio():
    """API para executar o sorteio"""
    global ultimo_resultado, historico_sorteios
    
    try:
        resultado = realizar_sorteio()
        ultimo_resultado = resultado
        historico_sorteios.append(resultado)
        
        return jsonify({
            "success": True,
            "resultado": resultado
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/resultados')
def resultados():
    """Tela de resultados"""
    if ultimo_resultado is None:
        return render_template('resultados.html', sem_sorteio=True)
    
    return render_template('resultados.html', 
                         resultado=ultimo_resultado, 
                         sem_sorteio=False)

@app.route('/api/limpar-resultado', methods=['POST'])
def limpar_resultado():
    """API para limpar o resultado atual"""
    global ultimo_resultado
    ultimo_resultado = None
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
