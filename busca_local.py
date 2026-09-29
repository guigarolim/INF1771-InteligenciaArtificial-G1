# busca_local.py
# Algoritmos de busca local para escolher os Pokémon de cada batalha.

import math
import random

import config
from batalhas import gerar_solucao_inicial, gerar_vizinho, custo_total


def hill_climbing():
    """Hill Climbing estocástico: aceita um vizinho aleatório só se ele for melhor."""
    atual = gerar_solucao_inicial()
    custo_atual = custo_total(atual)

    tentativas_sem_melhora = 0
    iteracoes = 0

    while tentativas_sem_melhora < config.HC_MAX_SEM_MELHORA:
        vizinho = gerar_vizinho(atual)
        custo_vizinho = custo_total(vizinho)
        iteracoes += 1

        if custo_vizinho < custo_atual:
            atual = vizinho
            custo_atual = custo_vizinho
            tentativas_sem_melhora = 0
        else:
            tentativas_sem_melhora += 1

    return atual, custo_atual, iteracoes


def aceita_vizinho(delta, temperatura):
    """Melhoras são sempre aceitas; pioras, com probabilidade e^(-delta/T)."""
    if delta <= 0:
        return True
    return random.random() < math.exp(-delta / temperatura)


def simulated_annealing():
    """Como o Hill Climbing, mas às vezes aceita pioras para escapar de ótimos locais."""
    atual = gerar_solucao_inicial()
    custo_atual = custo_total(atual)

    melhor = atual
    melhor_custo = custo_atual

    temperatura = config.SA_TEMPERATURA_INICIAL
    iteracoes = 0

    while temperatura > config.SA_TEMPERATURA_FINAL:
        for _ in range(config.SA_ITERACOES_POR_TEMPERATURA):
            vizinho = gerar_vizinho(atual)
            custo_vizinho = custo_total(vizinho)
            delta = custo_vizinho - custo_atual
            iteracoes += 1

            if aceita_vizinho(delta, temperatura):
                atual = vizinho
                custo_atual = custo_vizinho

                if custo_atual < melhor_custo:
                    melhor = atual
                    melhor_custo = custo_atual

        temperatura = temperatura * config.SA_ALFA

    return melhor, melhor_custo, iteracoes