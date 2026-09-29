# config.py
# Para alterar qualquer valor, edite apenas este arquivo.

# Tabela 1 - fator de poder de cada Pokémon
POKEMONS = {
    "Pikachu": 1.5,
    "Bulbassauro": 1.4,
    "Rattata": 1.3,
    "Caterpie": 1.2,
    "Weedle": 1.1,
}

# Tabela 2 - dificuldade de cada ginásio
# A chave é o caractere que representa o ginásio no mapa
GINASIOS = {
    "2": 35,  "3": 40,  "4": 45,  "5": 50,  "6": 55,  "7": 60,
    "8": 65,  "9": 70,  "B": 75,  "C": 80,  "D": 85,  "E": 90,
    "G": 95,  "H": 100, "I": 110, "J": 120, "K": 130, "L": 140,
    "N": 150, "O": 155, "P": 160, "Q": 165, "S": 170, "T": 180,
}

# Regras de energia
ENERGIA_INICIAL = 6
ENERGIA_MINIMA_FINAL = 1 

# Hill Climbing: para depois de tantas tentativas seguidas sem melhorar
HC_MAX_SEM_MELHORA = 2000

# Simulated Annealing
SA_TEMPERATURA_INICIAL = 50.0
SA_TEMPERATURA_FINAL = 0.1
SA_ALFA = 0.98                        # a cada etapa: temperatura = temperatura * alfa
SA_ITERACOES_POR_TEMPERATURA = 200    # vizinhos testados em cada temperatura
NUM_EXECUCOES = 30              # quantas vezes cada algoritmo é executado
PASTA_RESULTADOS = "resultados" # onde os custos de cada execução são salvos

SEMENTE = None

# Verificação de otimalidade por programação dinâmica
VERIFICAR_OTIMO = True