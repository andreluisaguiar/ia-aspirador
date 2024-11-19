import tkinter as tk
import random

# ------------------ Ambiente ------------------

linhas, colunas = 5, 5
estado_ambiente = [[random.choice(["Sujo", "Limpo"]) for _ in range(colunas)] for _ in range(linhas)]
posicao_agente = (0, 0)  # Linha e coluna iniciais do agente
performance = 0

# ------------------ Funções do Ambiente ------------------

def inicializar_ambiente():
    global estado_ambiente, posicao_agente, performance
    estado_ambiente = [[random.choice(["Sujo", "Limpo"]) for _ in range(colunas)] for _ in range(linhas)]
    posicao_agente = (0, 0)
    performance = 0
    atualizar_interface()

def perceber():
    linha, coluna = posicao_agente
    return (linha, coluna, estado_ambiente[linha][coluna])

def executar_acao(acao):
    global posicao_agente, estado_ambiente, performance
    linha, coluna = posicao_agente
    if acao == "Aspire":
        if estado_ambiente[linha][coluna] == "Sujo":
            estado_ambiente[linha][coluna] = "Limpo"
            performance += 10
    elif acao == "Cima" and linha > 0:
        posicao_agente = (linha - 1, coluna)
        performance -= 1
    elif acao == "Baixo" and linha < linhas - 1:
        posicao_agente = (linha + 1, coluna)
        performance -= 1
    elif acao == "Esquerda" and coluna > 0:
        posicao_agente = (linha, coluna - 1)
        performance -= 1
    elif acao == "Direita" and coluna < colunas - 1:
        posicao_agente = (linha, coluna + 1)
        performance -= 1
    atualizar_interface()

def ambiente_limpo():
    return all(celula == "Limpo" for linha in estado_ambiente for celula in linha)

# ------------------ Modelos de Agentes ------------------

# Modelo Aleatório
def agente_aleatorio(percepcao):
    acoes = ["Cima", "Baixo", "Esquerda", "Direita", "Aspire", "Nada"]
    return random.choice(acoes)

# Modelo Reflexivo
def agente_reflexivo(percepcao):
    linha, coluna, estado = percepcao
    if estado == "Sujo":
        return "Aspire"
    else:
        return random.choice(["Cima", "Baixo", "Esquerda", "Direita"])

# Modelo Baseado em Tabela
def agente_tabela(percepcao):
    linha, coluna, estado = percepcao
    if estado == "Sujo":
        return "Aspire"
    if coluna == colunas - 1:  # Na borda direita, mova para a esquerda
        return "Esquerda"
    if coluna == 0:  # Na borda esquerda, mova para a direita
        return "Direita"
    if linha == linhas - 1:  # Na borda inferior, suba
        return "Cima"
    if linha == 0:  # Na borda superior, desça
        return "Baixo"
    return random.choice(["Direita", "Esquerda", "Cima", "Baixo"])

# Modelo Baseado em Histórico (Modelo)
modelo_agente = [[None for _ in range(colunas)] for _ in range(linhas)]

def agente_modelo(percepcao):
    global modelo_agente
    linha, coluna, estado = percepcao
    modelo_agente[linha][coluna] = estado

    if all(celula == "Limpo" for linha in modelo_agente for celula in linha if celula is not None):
        return "Nada"
    elif estado == "Sujo":
        return "Aspire"
    else:
        return random.choice(["Cima", "Baixo", "Esquerda", "Direita"])

# ------------------ Atualização da Interface ------------------

def atualizar_interface():
    for i in range(linhas):
        for j in range(colunas):
            estado = estado_ambiente[i][j]
            if (i, j) == posicao_agente:
                celulas[i][j].config(bg="blue", text=f"{estado}\nAgente")
            else:
                celulas[i][j].config(bg="lightgray", text=estado)
    # Atualizar pontuação
    lbl_performance.config(text=f"Performance: {performance}")
    if ambiente_limpo():
        lbl_status.config(text="Status: Ambiente Limpo!")
    else:
        lbl_status.config(text="Status: Ambiente Sujo!")

# ------------------ Interface Gráfica ------------------

def criar_interface():
    global celulas, lbl_performance, lbl_status, modelo_var
    root = tk.Tk()
    root.title("Vacuum Cleaner - Modelos")

    # Criar variável Tk associada à janela
    modelo_var = tk.StringVar(root)
    modelo_var.set("Aleatorio")

    # Grid de células
    celulas = []
    for i in range(linhas):
        linha_celulas = []
        for j in range(colunas):
            celula = tk.Label(root, text="", bg="lightgray", width=10, height=5, font=("Arial", 10))
            celula.grid(row=i, column=j, padx=2, pady=2)
            linha_celulas.append(celula)
        celulas.append(linha_celulas)

    # Botão de próxima ação
    btn_next = tk.Button(root, text="Next", command=executar_proxima_acao)
    btn_next.grid(row=linhas, column=0, columnspan=colunas // 2)

    # Label de performance
    global lbl_performance
    lbl_performance = tk.Label(root, text="Performance: 0", font=("Arial", 12))
    lbl_performance.grid(row=linhas + 1, column=0, columnspan=colunas // 2)

    # Label de status
    global lbl_status
    lbl_status = tk.Label(root, text="Status: Ambiente Sujo!", font=("Arial", 12))
    lbl_status.grid(row=linhas + 1, column=colunas // 2, columnspan=colunas // 2)

    # Menu de seleção do modelo
    lbl_modelo = tk.Label(root, text="Modelo:", font=("Arial", 12))
    lbl_modelo.grid(row=linhas + 2, column=0, columnspan=1)

    menu_modelo = tk.OptionMenu(root, modelo_var, "Aleatorio", "Reflexivo", "Baseado em Modelo", "Baseado em Tabela")
    menu_modelo.grid(row=linhas + 2, column=1, columnspan=colunas - 1)

    # Inicializar o ambiente
    inicializar_ambiente()

    # Iniciar loop do Tkinter
    root.mainloop()

def executar_proxima_acao():
    percepcao = perceber()
    modelo = modelo_var.get()

    # Inicializar ação com um valor padrão
    acao = "Nada"  

    # Verificar o modelo selecionado
    if modelo == "Aleatorio":
        acao = agente_aleatorio(percepcao)
    elif modelo == "Reflexivo":
        acao = agente_reflexivo(percepcao)
    elif modelo == "Baseado em Modelo":
        acao = agente_modelo(percepcao)
    elif modelo == "Baseado em Tabela":
        acao = agente_tabela(percepcao)

    # Executar a ação
    executar_acao(acao)

# ------------------ Execução ------------------

if __name__ == "__main__":
    criar_interface()