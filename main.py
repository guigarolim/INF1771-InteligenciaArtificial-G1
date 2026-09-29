# main.py
# Tarefa 1: otimização das batalhas com busca local.

import random

import config
from busca_local import hill_climbing, simulated_annealing
from experimentos import rodar_experimento, calcular_estatisticas, salvar_custos
from verificacao import otimo_exato, contar_execucoes_no_otimo
from utils import imprimir_titulo, imprimir_solucao, imprimir_estatisticas, imprimir_comparacao


def experimento(nome, algoritmo, nome_arquivo):
    """Roda o algoritmo várias vezes, mostra as estatísticas e salva os custos."""
    imprimir_titulo(f"Experimento: {nome}")
    custos, melhor_solucao = rodar_experimento(algoritmo, config.NUM_EXECUCOES)
    melhor, media, desvio, vezes_no_melhor = calcular_estatisticas(custos)
    estatisticas = (melhor, media, desvio, vezes_no_melhor, len(custos))

    print()
    imprimir_estatisticas(estatisticas)
    caminho = salvar_custos(custos, nome_arquivo)
    print(f"  Custos salvos em:           {caminho}")

    return melhor_solucao, estatisticas, custos


def verificar_otimalidade(melhor_sa, custos_hc, custos_sa):
    """Compara os resultados da busca local com o ótimo exato."""
    imprimir_titulo("Verificação de otimalidade (programação dinâmica)")
    _, custo_otimo = otimo_exato()
    diferenca = melhor_sa - custo_otimo

    print(f"  Ótimo exato das batalhas:        {custo_otimo:.4f}")
    print(f"  Melhor do Simulated Annealing:   {melhor_sa:.4f}")
    print(f"  Diferença:                       {diferenca:.4f}"
          f" ({100 * diferenca / custo_otimo:.2f}%)")
    print(f"  Execuções do HC no ótimo:        "
          f"{contar_execucoes_no_otimo(custos_hc, custo_otimo)} de {len(custos_hc)}")
    print(f"  Execuções do SA no ótimo:        "
          f"{contar_execucoes_no_otimo(custos_sa, custo_otimo)} de {len(custos_sa)}")

    if abs(diferenca) < 1e-6:
        print("\n  A melhor solução do Simulated Annealing é o ótimo global.")
    else:
        print("\n  A busca local NÃO atingiu o ótimo global nesta execução.")


def main():
    random.seed(config.SEMENTE)

    # Algoritmo principal: Simulated Annealing. Hill Climbing serve de comparação.
    _, estat_hc, custos_hc = experimento("Hill Climbing", hill_climbing,
                              "custos_hill_climbing.csv")
    melhor_sa, estat_sa, custos_sa = experimento("Simulated Annealing", simulated_annealing,
                                      "custos_simulated_annealing.csv")

    imprimir_titulo("Melhor solução encontrada (Simulated Annealing)")
    print("  Obs.: ginásios na ordem da Tabela 1. A ordem de visita será")
    print("  definida pela rota do A* (Tarefa 2); o custo das batalhas não")
    print("  depende dessa ordem.\n")
    imprimir_solucao(melhor_sa)

    imprimir_titulo("Resumo do experimento")
    imprimir_comparacao("Hill Climbing", estat_hc, "Simulated Annealing", estat_sa)

    if config.VERIFICAR_OTIMO:
        verificar_otimalidade(estat_sa[0], custos_hc, custos_sa)


if __name__ == "__main__":
    main()