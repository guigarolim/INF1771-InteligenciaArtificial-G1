# batalhas.py
# Regras das batalhas: custo, energia e validade de uma solução.
#
# Uma solução é uma matriz (lista de listas) com uma linha por ginásio
# e uma coluna por Pokémon: solucao[g][p] = 1 se o Pokémon p luta no ginásio g.

import random

import config

# Listas na mesma ordem do config, para acessar os dados por índice
NOMES_POKEMONS = list(config.POKEMONS.keys())
PODERES = list(config.POKEMONS.values())
NOMES_GINASIOS = list(config.GINASIOS.keys())
DIFICULDADES = list(config.GINASIOS.values())

NUM_POKEMONS = len(PODERES)
NUM_GINASIOS = len(DIFICULDADES)


def poder_do_time(linha):
    """Soma o poder dos Pokémon que lutam em um ginásio (uma linha da matriz)."""
    total = 0
    for p in range(NUM_POKEMONS):
        if linha[p] == 1:
            total += PODERES[p]
    return total


def custo_batalha(g, linha):
    """Tempo da batalha no ginásio g: dificuldade / soma dos poderes."""
    return DIFICULDADES[g] / poder_do_time(linha)


def custo_total(solucao):
    """Soma o tempo de todas as batalhas."""
    total = 0
    for g in range(NUM_GINASIOS):
        total += custo_batalha(g, solucao[g])
    return total


def energia_final(solucao):
    """Energia de cada Pokémon depois de todas as batalhas."""
    energias = []
    for p in range(NUM_POKEMONS):
        batalhas = 0
        for g in range(NUM_GINASIOS):
            batalhas += solucao[g][p]
        energias.append(config.ENERGIA_INICIAL - batalhas)
    return energias


def solucao_valida(solucao):
    """Verifica todas as restrições de energia e de participação."""
    # Toda batalha precisa de pelo menos um Pokémon
    for linha in solucao:
        if sum(linha) == 0:
            return False

    energias = energia_final(solucao)

    # Energia negativa = o Pokémon lutou quando já estava com energia 0
    for energia in energias:
        if energia < 0:
            return False

    # Pelo menos um Pokémon precisa chegar ao destino com energia mínima
    if max(energias) < config.ENERGIA_MINIMA_FINAL:
        return False

    return True


# ---------------------------------------------------------------
# Criação de soluções
# ---------------------------------------------------------------

def criar_solucao_vazia():
    """Matriz só com zeros: ninguém luta em lugar nenhum."""
    return [[0] * NUM_POKEMONS for _ in range(NUM_GINASIOS)]


def copiar_solucao(solucao):
    """Cópia independente da matriz (alterar a cópia não altera a original)."""
    return [linha[:] for linha in solucao]


def gerar_solucao_inicial():
    """Cada ginásio recebe um Pokémon sorteado entre os que ainda têm energia."""
    solucao = criar_solucao_vazia()
    energias = [config.ENERGIA_INICIAL] * NUM_POKEMONS

    for g in range(NUM_GINASIOS):
        disponiveis = [p for p in range(NUM_POKEMONS) if energias[p] > 0]
        p = random.choice(disponiveis)
        solucao[g][p] = 1
        energias[p] -= 1

    return solucao


# ---------------------------------------------------------------
# Vizinhança: quatro tipos de movimento
# (cada um altera a matriz recebida; a validade é checada depois)
# ---------------------------------------------------------------

def movimento_flip(solucao):
    """Coloca ou tira um Pokémon de um ginásio."""
    g = random.randrange(NUM_GINASIOS)
    p = random.randrange(NUM_POKEMONS)
    solucao[g][p] = 1 - solucao[g][p]


def movimento_transferir(solucao):
    """Um Pokémon deixa de lutar em um ginásio e passa a lutar em outro."""
    p = random.randrange(NUM_POKEMONS)
    onde_luta = [g for g in range(NUM_GINASIOS) if solucao[g][p] == 1]
    onde_nao_luta = [g for g in range(NUM_GINASIOS) if solucao[g][p] == 0]
    if not onde_luta or not onde_nao_luta:
        return
    origem = random.choice(onde_luta)
    destino = random.choice(onde_nao_luta)
    solucao[origem][p] = 0
    solucao[destino][p] = 1


def movimento_substituir(solucao):
    """Em um ginásio, troca um Pokémon que luta por um que não luta."""
    g = random.randrange(NUM_GINASIOS)
    lutam = [p for p in range(NUM_POKEMONS) if solucao[g][p] == 1]
    nao_lutam = [p for p in range(NUM_POKEMONS) if solucao[g][p] == 0]
    if not lutam or not nao_lutam:
        return
    sai = random.choice(lutam)
    entra = random.choice(nao_lutam)
    solucao[g][sai] = 0
    solucao[g][entra] = 1


def movimento_trocar(solucao):
    """Dois ginásios trocam Pokémon entre si: p sai de g1 e vai para g2, q faz o caminho inverso."""
    g1 = random.randrange(NUM_GINASIOS)
    g2 = random.randrange(NUM_GINASIOS)
    so_em_g1 = [p for p in range(NUM_POKEMONS) if solucao[g1][p] == 1 and solucao[g2][p] == 0]
    so_em_g2 = [p for p in range(NUM_POKEMONS) if solucao[g2][p] == 1 and solucao[g1][p] == 0]
    if not so_em_g1 or not so_em_g2:
        return
    p = random.choice(so_em_g1)
    q = random.choice(so_em_g2)
    solucao[g1][p] = 0
    solucao[g2][p] = 1
    solucao[g2][q] = 0
    solucao[g1][q] = 1


def gerar_vizinho(solucao):
    """Sorteia movimentos até obter um vizinho diferente e válido."""
    while True:
        vizinho = copiar_solucao(solucao)
        movimento = random.choice([movimento_flip,
                                   movimento_transferir,
                                   movimento_substituir,
                                   movimento_trocar])
        movimento(vizinho)
        if vizinho != solucao and solucao_valida(vizinho):
            return vizinho