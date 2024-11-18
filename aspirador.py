import random

# ------------------ Ambiente ------------------

estado_ambiente = {"loc_A": "Sujo", "loc_B": "Sujo"}
local_agente = "loc_A"

def inicializar_ambiente():
    global estado_ambiente, local_agente
    estado_ambiente = {"loc_A": "Sujo", "loc_B": "Sujo"}
    local_agente = "loc_A"

def perceber():
    global local_agente
    return (local_agente, estado_ambiente[local_agente])

def executar_acao(acao):
    global local_agente, estado_ambiente
    if acao == "Aspire":
        estado_ambiente[local_agente] = "Limpo"
    elif acao == "Direita":
        local_agente = "loc_B"
    elif acao == "Esquerda":
        local_agente = "loc_A"
    elif acao == "Nada":
        pass

def ambiente_limpo():
    return all(estado == "Limpo" for estado in estado_ambiente.values())

# ------------------ Agentes ------------------

def agente_aleatorio(percepcao):
    acoes = ["Direita", "Esquerda", "Aspire", "Nada"]
    return random.choice(acoes)

def agente_reflexivo(percepcao):
    local, estado = percepcao
    if estado == "Sujo":
        return "Aspire"
    elif local == "loc_A":
        return "Direita"
    elif local == "loc_B":
        return "Esquerda"

modelo_agente = {"loc_A": None, "loc_B": None}

def agente_modelo(percepcao):
    global modelo_agente
    local, estado = percepcao
    modelo_agente[local] = estado  

    if modelo_agente["loc_A"] == modelo_agente["loc_B"] == "Limpo":
        return "Nada"
    elif estado == "Sujo":
        return "Aspire"
    elif local == "loc_A":
        return "Direita"
    elif local == "loc_B":
        return "Esquerda"

# ------------------ Simulação ------------------

def executar_simulacao(agente, passos=10):
    inicializar_ambiente()
    for passo in range(passos):
        percepcao = perceber()  
        acao = agente(percepcao)  
        executar_acao(acao) 

       
        print(f"Passo {passo + 1}: Local: {local_agente}, Acao: {acao}, Estado: {estado_ambiente}")

        if ambiente_limpo():
            print("O ambiente esta limpo! Fim da simulacao.")
            break

# ------------------ Execução ------------------

if __name__ == "__main__":
    print("Simulacao com Agente Aleatorio:")
    executar_simulacao(agente_aleatorio)

    print("\nSimulacao com Agente Reflexivo:")
    executar_simulacao(agente_reflexivo)

    print("\nSimulacao com Agente Baseado em Modelo:")
    executar_simulacao(agente_modelo)