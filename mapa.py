from pathlib import Path
import heapq
import math
import config


def carregar_mapa(nome_arquivo="kanto.txt"):
    caminho = Path(nome_arquivo)
    if not caminho.exists():
        caminho = Path(__file__).resolve().parent / nome_arquivo
    with open(caminho, "r", encoding="utf-8") as arquivo:
        mapa = [list(linha.rstrip("\n")) for linha in arquivo if linha.rstrip("\n")]
    validar_mapa(mapa)
    return mapa


def validar_mapa(mapa):
    if not mapa:
        raise ValueError("Mapa vazio.")
    larguras = {len(linha) for linha in mapa}
    if len(larguras) != 1:
        raise ValueError("Todas as linhas do mapa precisam ter o mesmo tamanho.")
    caracteres_validos = set(config.CUSTOS_TERRENO) | set(config.GINASIOS)
    desconhecidos = {c for linha in mapa for c in linha if c not in caracteres_validos}
    if desconhecidos:
        raise ValueError(f"Caracteres desconhecidos no mapa: {sorted(desconhecidos)}")


def localizar_pontos(mapa):
    inicio = None
    destino = None
    ginasios = {}
    for linha in range(len(mapa)):
        for coluna in range(len(mapa[linha])):
            celula = mapa[linha][coluna]
            if celula == "1":
                inicio = (linha, coluna)
            elif celula == "U":
                destino = (linha, coluna)
            elif celula in config.GINASIOS:
                ginasios[celula] = (linha, coluna)
    if inicio is None or destino is None:
        raise ValueError("O mapa precisa conter origem '1' e destino 'U'.")
    faltantes = set(config.GINASIOS) - set(ginasios)
    if faltantes:
        raise ValueError(f"Faltam ginasios no mapa: {sorted(faltantes)}")
    if len(ginasios) != 24:
        raise ValueError(f"Esperados 24 ginasios; encontrados {len(ginasios)}.")
    return inicio, destino, ginasios


def custo_celula(celula):
    if celula in config.GINASIOS:
        return config.CUSTO_GINASIO_NO_MAPA
    return config.CUSTOS_TERRENO[celula]


def vizinhos(mapa, posicao):
    linha, coluna = posicao
    for dl, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nl, nc = linha + dl, coluna + dc
        if 0 <= nl < len(mapa) and 0 <= nc < len(mapa[nl]):
            yield (nl, nc)


def menor_caminho_grade(mapa, origem, destinos=None, nao_expandir=None):
    """Dijkstra na grade. Retorna distancias e predecessores.

    O custo de uma transicao e o custo da celula de destino.
    Se destinos for informado, encerra quando todos forem fechados.
    """
    dist = {origem: 0.0}
    anterior = {}
    fila = [(0.0, origem)]
    pendentes = set(destinos) if destinos is not None else None
    nao_expandir = set(nao_expandir or ())

    while fila:
        custo, atual = heapq.heappop(fila)
        if custo != dist.get(atual):
            continue
        if pendentes is not None and atual in pendentes:
            pendentes.remove(atual)
            if not pendentes:
                break
        # Pontos especiais podem ser destinos de uma aresta, mas nao podem ser
        # atravessados silenciosamente para alcancar outro ponto especial.
        if atual != origem and atual in nao_expandir:
            continue
        for prox in vizinhos(mapa, atual):
            novo = custo + custo_celula(mapa[prox[0]][prox[1]])
            if novo < dist.get(prox, math.inf):
                dist[prox] = novo
                anterior[prox] = atual
                heapq.heappush(fila, (novo, prox))
    return dist, anterior


def reconstruir_caminho_grade(anterior, origem, destino):
    if origem == destino:
        return [origem]
    if destino not in anterior:
        raise ValueError(f"Destino {destino} inalcancavel a partir de {origem}.")
    caminho = [destino]
    atual = destino
    while atual != origem:
        atual = anterior[atual]
        caminho.append(atual)
    caminho.reverse()
    return caminho
