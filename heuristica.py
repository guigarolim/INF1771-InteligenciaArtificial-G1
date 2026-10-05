"""Heuristicas admissiveis para o A* dos 24 ginasios."""
from functools import lru_cache
import math

try:
    import numpy as np
    from scipy.optimize import linear_sum_assignment
except Exception:  # dependencia opcional; ha fallback
    np = None
    linear_sum_assignment = None


def criar_heuristica_mst(distancias, qtd_ginasios, indice_destino):
    """Cria h = max(MST, limite de graus, assignment relaxation).

    Todas as parcelas sao lower bounds do custo de completar um caminho que sai
    do ponto atual, visita cada ginasio restante exatamente uma vez e termina em U.
    """
    def aresta_relaxada(a, b):
        return min(distancias[a][b], distancias[b][a])

    @lru_cache(maxsize=None)
    def mst(mask_restantes):
        vertices = [i + 1 for i in range(qtd_ginasios) if mask_restantes & (1 << i)]
        if len(vertices) <= 1:
            return 0.0
        usados = {vertices[0]}
        melhor = {v: aresta_relaxada(vertices[0], v) for v in vertices[1:]}
        total = 0.0
        while len(usados) < len(vertices):
            v = min((x for x in vertices if x not in usados), key=lambda x: melhor[x])
            total += melhor[v]
            usados.add(v)
            for w in vertices:
                if w not in usados:
                    e = aresta_relaxada(v, w)
                    if e < melhor[w]:
                        melhor[w] = e
        return total

    @lru_cache(maxsize=None)
    def assignment_bound(indice_atual, mask_restantes):
        if linear_sum_assignment is None:
            return 0.0
        restantes = [i + 1 for i in range(qtd_ginasios) if mask_restantes & (1 << i)]
        if not restantes:
            return distancias[indice_atual][indice_destino]

        # Em qualquer caminho Hamiltoniano restante:
        # fontes = atual + todos os restantes (cada um tem exatamente uma saida)
        # alvos   = restantes + destino (cada um tem exatamente uma entrada)
        # Ao ignorar a restricao de eliminar subtours obtemos um lower bound.
        fontes = [indice_atual] + restantes
        alvos = restantes + [indice_destino]
        n = len(fontes)
        matriz = np.empty((n, n), dtype=float)
        grande = 1e12
        for i, a in enumerate(fontes):
            for j, b in enumerate(alvos):
                matriz[i, j] = grande if a == b else distancias[a][b]
        linhas, colunas = linear_sum_assignment(matriz)
        return float(matriz[linhas, colunas].sum())

    @lru_cache(maxsize=None)
    def h(indice_atual, mask_visitados):
        todos = (1 << qtd_ginasios) - 1
        mask_restantes = todos ^ mask_visitados
        if mask_restantes == 0:
            return distancias[indice_atual][indice_destino]

        restantes = [i + 1 for i in range(qtd_ginasios) if mask_restantes & (1 << i)]
        liga_atual = min(distancias[indice_atual][v] for v in restantes)
        liga_destino = min(distancias[v][indice_destino] for v in restantes)
        limite_mst = liga_atual + mst(mask_restantes) + liga_destino

        vertices = [indice_atual] + restantes + [indice_destino]
        soma = 0.0
        for v in vertices:
            incidentes = sorted(aresta_relaxada(v, w) for w in vertices if w != v)
            grau = 1 if v in (indice_atual, indice_destino) else 2
            if len(incidentes) < grau:
                return math.inf
            soma += sum(incidentes[:grau])
        limite_graus = soma / 2.0
        limite_assignment = assignment_bound(indice_atual, mask_restantes)
        return max(limite_mst, limite_graus, limite_assignment)

    return h
