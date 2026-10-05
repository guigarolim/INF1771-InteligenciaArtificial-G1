# config.py
# Centraliza todos os parametros configuraveis do trabalho.

POKEMONS = {
    "Pikachu": 1.5,
    "Bulbassauro": 1.4,
    "Rattata": 1.3,
    "Caterpie": 1.2,
    "Weedle": 1.1,
}

# Identificador no mapa -> dificuldade da batalha.
GINASIOS = {
    "2": 35,  "3": 40,  "4": 45,  "5": 50,  "6": 55,  "7": 60,
    "8": 65,  "9": 70,  "B": 75,  "C": 80,  "D": 85,  "E": 90,
    "G": 95,  "H": 100, "I": 110, "J": 120, "K": 130, "L": 140,
    "N": 150, "O": 155, "P": 160, "Q": 165, "S": 170, "T": 180,
}

# Custo para ENTRAR em cada tipo de celula, em minutos.
CUSTOS_TERRENO = {
    ".": 1,
    "M": 200,
    "A": 30,
    "F": 15,
    "R": 5,
    "1": 1,
    "U": 1,
}
CUSTO_GINASIO_NO_MAPA = 1

ENERGIA_INICIAL = 6
ENERGIA_MINIMA_FINAL = 1

# Busca local
HC_MAX_SEM_MELHORA = 2000
SA_TEMPERATURA_INICIAL = 50.0
SA_TEMPERATURA_FINAL = 0.1
SA_ALFA = 0.98
SA_ITERACOES_POR_TEMPERATURA = 200
NUM_EXECUCOES = 30
PASTA_RESULTADOS = "resultados"
SEMENTE = None
VERIFICAR_OTIMO = True

# A*: se True, imprime progresso resumido a cada N expansoes.
A_STAR_MOSTRAR_PROGRESSO = True
A_STAR_INTERVALO_PROGRESSO = 10000

# Visualizacao
ARQUIVO_VISUALIZACAO = "resultado_rota.png"
