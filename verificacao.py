# verificacao.py
# Calcula o ótimo EXATO das batalhas por programação dinâmica.
# Não substitui a busca local (exigida pelo PDF): serve só para verificar
# se a solução encontrada pela busca local é o ótimo global.

import itertools

import config
from batalhas import NUM_GINASIOS, NUM_POKEMONS, custo_batalha


def gerar_times_possiveis():
    """Todas as linhas possíveis da matriz: combinações de 0 e 1 com pelo menos um Pokémon."""
    times = []
    for linha in itertools.product([0, 1], repeat=NUM_POKEMONS):
        if sum(linha) > 0:
            times.append(list(linha))
    return times


def calcular_tabela():
    """
    tabela[g] é um dicionário:
        energias depois dos g primeiros ginásios -> (menor custo, energias anteriores, time usado)
    """
    times = gerar_times_possiveis()
    energias_iniciais = tuple([config.ENERGIA_INICIAL] * NUM_POKEMONS)
    tabela = [{energias_iniciais: (0.0, None, None)}]

    for g in range(NUM_GINASIOS):
        proxima = {}
        for energias, (custo, _, _) in tabela[g].items():
            for time in times:
                novas = tuple(energias[p] - time[p] for p in range(NUM_POKEMONS))
                if min(novas) < 0:          # alguém lutaria com energia 0
                    continue
                novo_custo = custo + custo_batalha(g, time)
                if novas not in proxima or novo_custo < proxima[novas][0]:
                    proxima[novas] = (novo_custo, energias, time)
        tabela.append(proxima)

    return tabela


def escolher_estado_final(tabela):
    """Entre os estados finais válidos (alguém com energia mínima), o de menor custo."""
    melhor_estado = None
    melhor_custo = float("inf")
    for energias, (custo, _, _) in tabela[NUM_GINASIOS].items():
        if max(energias) >= config.ENERGIA_MINIMA_FINAL and custo < melhor_custo:
            melhor_estado = energias
            melhor_custo = custo
    return melhor_estado, melhor_custo


def reconstruir_solucao(tabela, estado_final):
    """Volta do último ginásio ao primeiro, recuperando o time usado em cada um."""
    solucao = [None] * NUM_GINASIOS
    estado = estado_final
    for g in range(NUM_GINASIOS, 0, -1):
        _, anterior, time = tabela[g][estado]
        solucao[g - 1] = time
        estado = anterior
    return solucao


def otimo_exato():
    tabela = calcular_tabela()
    estado_final, custo = escolher_estado_final(tabela)
    solucao = reconstruir_solucao(tabela, estado_final)
    return solucao, custo


def contar_execucoes_no_otimo(custos, custo_otimo):
    vezes = 0
    for custo in custos:
        if abs(custo - custo_otimo) < 1e-6:
            vezes += 1
    return vezes