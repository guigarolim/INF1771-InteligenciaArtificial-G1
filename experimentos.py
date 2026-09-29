# experimentos.py
# Executa um algoritmo de busca local várias vezes e resume os resultados.

import os
import statistics

import config


def rodar_experimento(algoritmo, num_execucoes):
    """Executa o algoritmo várias vezes e guarda o custo de cada execução."""
    custos = []
    melhor_solucao = None
    melhor_custo = float("inf")

    for i in range(num_execucoes):
        solucao, custo, iteracoes = algoritmo()
        custos.append(custo)
        print(f"  Execução {i + 1:>2}: {custo:.4f}  ({iteracoes} iterações)")

        if custo < melhor_custo:
            melhor_custo = custo
            melhor_solucao = solucao

    return custos, melhor_solucao


def calcular_estatisticas(custos):
    """Melhor, média, desvio-padrão e quantas execuções atingiram o melhor."""
    melhor = min(custos)
    media = statistics.mean(custos)
    desvio = statistics.stdev(custos) if len(custos) > 1 else 0.0

    # Custos são números reais: comparamos com uma pequena tolerância
    vezes_no_melhor = 0
    for custo in custos:
        if abs(custo - melhor) < 1e-6:
            vezes_no_melhor += 1

    return melhor, media, desvio, vezes_no_melhor


def salvar_custos(custos, nome_arquivo):
    """Salva o custo de cada execução em um CSV dentro da pasta de resultados."""
    os.makedirs(config.PASTA_RESULTADOS, exist_ok=True)
    caminho = os.path.join(config.PASTA_RESULTADOS, nome_arquivo)

    with open(caminho, "w") as arquivo:
        arquivo.write("execucao,custo\n")
        for i, custo in enumerate(custos):
            arquivo.write(f"{i + 1},{custo:.4f}\n")

    return caminho