import json
import random

# Carregar os dados dos arquivos JSON
with open('vagas.json', 'r', encoding='utf-8') as f:
    vagas = json.load(f)

with open('apartamentos.json', 'r', encoding='utf-8') as f:
    apartamentos = json.load(f)

resultado_final = {}

# ==========================================
# 1º SORTEIO: VAGAS PCD
# ==========================================
# Filtra aps PCD e as vagas específicas para PCD (Ex: Y, W, Z definidas na propriedade PCD)
aps_pcd = [ap for ap in apartamentos if ap.get("pcd") is True]
vagas_pcd = [v for v in vagas if v.get("PCD") is True]

random.shuffle(vagas_pcd) # Embaralha as vagas PCD

for ap in aps_pcd:
    if vagas_pcd:
        vaga_sorteada = vagas_pcd.pop(0)
        resultado_final[ap["ap"]] = vaga_sorteada
        # Remove dos grupos gerais para não sortear novamente
        apartamentos.remove(ap)
        vagas.remove(vaga_sorteada)

# ==========================================
# 2º SORTEIO: VAGAS DESCOBERTAS
# ==========================================
# Regra: Sorteia as vagas descobertas apenas para apartamentos do tipo "vaga descoberta"
vagas_descobertas = [v for v in vagas if v.get("coberta") is False]
random.shuffle(vagas_descobertas)

# Filtra apenas os apartamentos do tipo "vaga descoberta"
aps_para_descobertas = [ap for ap in apartamentos if ap.get("tipo") == "vaga descoberta"]
random.shuffle(aps_para_descobertas)

for ap in aps_para_descobertas:
    if vagas_descobertas:
        vaga_sorteada = vagas_descobertas.pop(0)
        resultado_final[ap["ap"]] = vaga_sorteada
        apartamentos.remove(ap)
        vagas.remove(vaga_sorteada)

# ==========================================
# 3º SORTEIO: BLOCOS (SS2 / SS3) & AMPLA CONCORRÊNCIA
# ==========================================
# Separar as vagas restantes por regras de acesso
vagas_bloco_A = [v for v in vagas if v["loca"] in ["SS2", "SS3"] and v["Facil_acesso"] == "A"]
vagas_bloco_B = [v for v in vagas if v["loca"] in ["SS2", "SS3"] and v["Facil_acesso"] == "B"]
vagas_ampla = [v for v in vagas if v["Facil_acesso"] == "Ampla concorencia" or v["loca"] in ["SS1", "SS4"]]

# Separar os apartamentos restantes por bloco
aps_bloco_A = [ap for ap in apartamentos if ap["bloco"] == "A"]
aps_bloco_B = [ap for ap in apartamentos if ap["bloco"] == "B"]

# Embaralhar todas as listas de vagas para o sorteio
random.shuffle(vagas_bloco_A)
random.shuffle(vagas_bloco_B)

# Sorteio do Bloco A nas vagas reservadas para o Lado A (SS2 e SS3)
for ap in list(aps_bloco_A):
    if vagas_bloco_A:
        vaga_sorteada = vagas_bloco_A.pop(0)
        resultado_final[ap["ap"]] = vaga_sorteada
        aps_bloco_A.remove(ap)
        vagas.remove(vaga_sorteada)

# Sorteio do Bloco B nas vagas reservadas para o Lado B (SS2 e SS3)
for ap in list(aps_bloco_B):
    if vagas_bloco_B:
        vaga_sorteada = vagas_bloco_B.pop(0)
        resultado_final[ap["ap"]] = vaga_sorteada
        aps_bloco_B.remove(ap)
        vagas.remove(vaga_sorteada)

# Junção dos apartamentos que sobraram (não conseguiram vaga no seu próprio bloco)
aps_restantes = aps_bloco_A + aps_bloco_B
# Junção das vagas que sobraram dos blocos + SS1 e SS4 (Ampla Concorrência)
vagas_restantes_total = vagas_bloco_A + vagas_bloco_B + vagas_ampla
random.shuffle(vagas_restantes_total)

# Sorteio final da Ampla Concorrência
for ap in aps_restantes:
    if vagas_restantes_total:
        vaga_sorteada = vagas_restantes_total.pop(0)
        resultado_final[ap["ap"]] = vaga_sorteada

# ==========================================
# EXIBIÇÃO DO RESULTADO
# ==========================================
print("\n --- RESULTADO DO SORTEIO DOS APARTAMENTOS --- ")
for ap, vaga in sorted(resultado_final.items()):
    print(f"Apartamento: {ap}  Vaga: {vaga['vaga']} ({vaga['loca']} | Coberta: {vaga['coberta']} | Acesso: {vaga['Facil_acesso']})")
