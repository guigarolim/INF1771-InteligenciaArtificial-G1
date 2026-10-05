# Trabalho 1 - Inteligencia Artificial / Pokemon Kanto
# Integra Tarefa 1 (busca local para batalhas) e Tarefa 2 (A* para rota).

import argparse
import random

import config
from astar import a_estrela_ginasios
from batalhas import custo_total as custo_batalhas, energia_final, NOMES_GINASIOS, NOMES_POKEMONS
from busca_local import hill_climbing, simulated_annealing
from experimentos import rodar_experimento, calcular_estatisticas, salvar_custos
from mapa import carregar_mapa, localizar_pontos
from utils import imprimir_titulo, imprimir_solucao, imprimir_estatisticas, imprimir_comparacao
from verificacao import otimo_exato, contar_execucoes_no_otimo
from visualizacao import visualizar_resultado


def experimento(nome, algoritmo, nome_arquivo, num_execucoes):
    imprimir_titulo(f"Experimento: {nome}")
    custos, melhor_solucao = rodar_experimento(algoritmo, num_execucoes)
    melhor, media, desvio, vezes_no_melhor = calcular_estatisticas(custos)
    estatisticas = (melhor, media, desvio, vezes_no_melhor, len(custos))
    print()
    imprimir_estatisticas(estatisticas)
    caminho = salvar_custos(custos, nome_arquivo)
    print(f"  Custos salvos em:           {caminho}")
    return melhor_solucao, estatisticas, custos


def verificar_otimalidade(melhor_sa, custos_hc, custos_sa):
    imprimir_titulo("Verificacao do otimo das batalhas (programacao dinamica)")
    _, custo_otimo = otimo_exato()
    diferenca = melhor_sa - custo_otimo
    print(f"  Otimo exato das batalhas:        {custo_otimo:.4f}")
    print(f"  Melhor do Simulated Annealing:   {melhor_sa:.4f}")
    print(f"  Diferenca:                       {diferenca:.4f} ({100*diferenca/custo_otimo:.2f}%)")
    print(f"  Execucoes HC no otimo:           {contar_execucoes_no_otimo(custos_hc, custo_otimo)} de {len(custos_hc)}")
    print(f"  Execucoes SA no otimo:           {contar_execucoes_no_otimo(custos_sa, custo_otimo)} de {len(custos_sa)}")


def imprimir_resumo_final(resultado_rota, solucao_batalhas):
    imprimir_titulo("RESULTADO FINAL DO TRABALHO")
    print("  Ordem de visita aos 24 ginasios:")
    print("  1 -> " + " -> ".join(resultado_rota.ordem_ginasios) + " -> U")

    print("\n  Pokemon usados em cada batalha, na ordem real da rota:")
    indice_por_nome = {nome: i for i, nome in enumerate(NOMES_GINASIOS)}
    for ordem, nome_ginasio in enumerate(resultado_rota.ordem_ginasios, start=1):
        g = indice_por_nome[nome_ginasio]
        usados = [NOMES_POKEMONS[p] for p, usa in enumerate(solucao_batalhas[g]) if usa]
        print(f"    {ordem:>2}. Ginasio {nome_ginasio}: {', '.join(usados)}")

    energias = energia_final(solucao_batalhas)
    print("\n  Energia final:")
    for nome, energia in zip(NOMES_POKEMONS, energias):
        print(f"    {nome:<12}: {energia}")

    cb = custo_batalhas(solucao_batalhas)
    cr = resultado_rota.custo_rota
    print(f"\n  Custo das batalhas: {cb:.4f} minutos")
    print(f"  Custo da rota:      {cr:.4f} minutos")
    print(f"  CUSTO TOTAL:        {cb + cr:.4f} minutos")
    print(f"  Estados expandidos pelo A*: {resultado_rota.estados_expandidos}")
    print(f"  Estados restantes na fronteira: {resultado_rota.fronteira_final}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mapa", default="kanto.txt")
    parser.add_argument("--execucoes", type=int, default=config.NUM_EXECUCOES,
                        help="numero de execucoes de HC e SA")
    parser.add_argument("--sem-verificacao", action="store_true",
                        help="nao calcula o otimo exato das batalhas por DP")
    parser.add_argument("--mostrar", action="store_true",
                        help="abre a figura da rota ao final")
    args = parser.parse_args()

    random.seed(config.SEMENTE)

    mapa = carregar_mapa(args.mapa)
    inicio, destino, ginasios = localizar_pontos(mapa)
    print(f"Mapa carregado: {len(mapa)} linhas x {len(mapa[0])} colunas")
    print(f"Origem: {inicio} | Destino U: {destino} | Ginasios: {len(ginasios)}")

    # Tarefa 1: busca local exigida pelo enunciado.
    _, estat_hc, custos_hc = experimento("Hill Climbing", hill_climbing,
                                         "custos_hill_climbing.csv", args.execucoes)
    melhor_sa, estat_sa, custos_sa = experimento("Simulated Annealing", simulated_annealing,
                                                  "custos_simulated_annealing.csv", args.execucoes)

    imprimir_titulo("Melhor solucao de batalhas (Simulated Annealing)")
    imprimir_solucao(melhor_sa)
    imprimir_titulo("Comparacao dos experimentos")
    imprimir_comparacao("Hill Climbing", estat_hc, "Simulated Annealing", estat_sa)

    if config.VERIFICAR_OTIMO and not args.sem_verificacao:
        verificar_otimalidade(estat_sa[0], custos_hc, custos_sa)

    # Tarefa 2: A* exato no estado (ponto atual, conjunto de ginasios visitados).
    imprimir_titulo("A*: calculando rota pelos 24 ginasios")
    resultado_rota = a_estrela_ginasios(mapa, inicio, destino, ginasios)

    imprimir_resumo_final(resultado_rota, melhor_sa)
    arquivo = visualizar_resultado(mapa, resultado_rota, inicio, destino, ginasios,
                                   arquivo=config.ARQUIVO_VISUALIZACAO, mostrar=args.mostrar)
    if arquivo:
        print(f"\n  Visualizacao grafica salva em: {arquivo}")


if __name__ == "__main__":
    main()
