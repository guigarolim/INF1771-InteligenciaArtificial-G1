import heapq
import math
from dataclasses import dataclass

import config
from heuristica import criar_heuristica_mst
from mapa import menor_caminho_grade, reconstruir_caminho_grade, custo_celula


@dataclass
class ResultadoAStar:
    ordem_ginasios: list
    caminho_grade: list
    custo_rota: float
    estados_expandidos: int
    fronteira_final: int
    expandidos_posicoes: set
    fronteira_posicoes: set


def _precalcular_distancias(mapa, especiais):
    n = len(especiais)
    matriz = [[math.inf] * n for _ in range(n)]
    predecessores = {}
    alvos = set(especiais)
    for i, origem in enumerate(especiais):
        dist, ant = menor_caminho_grade(mapa, origem, alvos - {origem}, nao_expandir=alvos - {origem})
        predecessores[i] = ant
        matriz[i][i] = 0.0
        for j, destino in enumerate(especiais):
            if i != j:
                matriz[i][j] = dist[destino]
    return matriz, predecessores


def _custo_rota_indices(rota, distancias):
    return float(custo_celula("1")) + sum(distancias[a][b] for a, b in zip(rota, rota[1:]))


def _rota_inicial_2opt(distancias, qtd_ginasios, destino_idx):
    """Constroi incumbente factivel (vizinho mais proximo + 2-opt)."""
    atual = 0
    restantes = set(range(1, qtd_ginasios + 1))
    rota = [0]
    while restantes:
        prox = min(restantes, key=lambda j: distancias[atual][j])
        rota.append(prox)
        restantes.remove(prox)
        atual = prox
    rota.append(destino_idx)
    melhor = rota
    melhor_custo = _custo_rota_indices(melhor, distancias)

    mudou = True
    while mudou:
        mudou = False
        for i in range(1, len(melhor) - 2):
            for j in range(i + 1, len(melhor) - 1):
                candidata = melhor[:i] + list(reversed(melhor[i:j + 1])) + melhor[j + 1:]
                custo = _custo_rota_indices(candidata, distancias)
                if custo + 1e-9 < melhor_custo:
                    melhor, melhor_custo = candidata, custo
                    mudou = True
                    break
            if mudou:
                break
    return melhor, melhor_custo


def a_estrela_ginasios(mapa, inicio, destino, ginasios):
    """A* exato sobre estados (local especial atual, conjunto de ginasios visitados).

    A grade e condensada em um grafo completo dos pontos especiais usando Dijkstra,
    mas o caminho final e reconstruido celula a celula no mapa original.
    """
    nomes = list(config.GINASIOS.keys())
    pos_ginasios = [ginasios[n] for n in nomes]
    especiais = [inicio] + pos_ginasios + [destino]
    qtd = len(nomes)
    destino_idx = qtd + 1

    distancias, predecessores = _precalcular_distancias(mapa, especiais)
    h = criar_heuristica_mst(distancias, qtd, destino_idx)
    todos = (1 << qtd) - 1

    estado_inicial = (0, 0)  # indice atual, mascara visitados
    g_score = {estado_inicial: float(custo_celula("1"))}  # origem tambem custa +1
    anterior = {}
    contador = 0
    heap = [(g_score[estado_inicial] + h(0, 0), g_score[estado_inicial], contador, estado_inicial)]
    rota_incumbente, limite_superior = _rota_inicial_2opt(distancias, qtd, destino_idx)
    expandidos = 0
    expandidos_posicoes = set()

    estado_goal = None
    custo_goal = limite_superior
    sequencia_incumbente = rota_incumbente

    while heap:
        f, g, _, estado = heapq.heappop(heap)
        if g != g_score.get(estado):
            continue
        if f >= custo_goal - 1e-9:
            # Como a fila esta ordenada por f, nenhum estado restante pode melhorar o incumbente.
            break

        atual_idx, mask = estado
        expandidos += 1
        expandidos_posicoes.add(especiais[atual_idx])

        if mask == todos:
            total = g + distancias[atual_idx][destino_idx]
            if total < custo_goal:
                custo_goal = total
                estado_goal = estado
            # Como h neste estado e exatamente a distancia a U, se este e o menor f,
            # a primeira solucao fechada e otima.
            break

        if config.A_STAR_MOSTRAR_PROGRESSO and expandidos % config.A_STAR_INTERVALO_PROGRESSO == 0:
            print(f"  A*: {expandidos} estados expandidos; fronteira={len(heap)}; melhor f={f:.1f}")

        for bit in range(qtd):
            flag = 1 << bit
            if mask & flag:
                continue
            prox_idx = bit + 1
            novo_mask = mask | flag
            novo_estado = (prox_idx, novo_mask)
            novo_g = g + distancias[atual_idx][prox_idx]
            novo_f = novo_g + h(prox_idx, novo_mask)
            if novo_f >= min(limite_superior, custo_goal):
                continue
            if novo_g < g_score.get(novo_estado, math.inf):
                g_score[novo_estado] = novo_g
                anterior[novo_estado] = estado
                contador += 1
                heapq.heappush(heap, (novo_f, novo_g, contador, novo_estado))

    # Se A* encontrou incumbente melhor, reconstrui-lo; caso contrario,
    # o esvaziamento/corte por f prova que a rota incumbente e otima.
    if estado_goal is not None:
        estados = []
        e = estado_goal
        while True:
            estados.append(e)
            if e == estado_inicial:
                break
            e = anterior[e]
        estados.reverse()
        sequencia_indices = [s[0] for s in estados] + [destino_idx]
    else:
        sequencia_indices = sequencia_incumbente
    ordem = [nomes[i - 1] for i in sequencia_indices if 1 <= i <= qtd]

    # Reconstruir trajeto completo na matriz.
    caminho_grade = []
    for a, b in zip(sequencia_indices, sequencia_indices[1:]):
        trecho = reconstruir_caminho_grade(predecessores[a], especiais[a], especiais[b])
        if caminho_grade:
            trecho = trecho[1:]
        caminho_grade.extend(trecho)

    fronteira_posicoes = {especiais[estado[0]] for _, g, _, estado in heap if g == g_score.get(estado)}
    return ResultadoAStar(
        ordem_ginasios=ordem,
        caminho_grade=caminho_grade,
        custo_rota=custo_goal,
        estados_expandidos=expandidos,
        fronteira_final=len(heap),
        expandidos_posicoes=expandidos_posicoes,
        fronteira_posicoes=fronteira_posicoes,
    )
