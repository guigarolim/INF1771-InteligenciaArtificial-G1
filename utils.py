# utils.py
# Funções de impressão dos resultados.

import config
from batalhas import (NUM_GINASIOS, NUM_POKEMONS, NOMES_GINASIOS, NOMES_POKEMONS,
                      DIFICULDADES, poder_do_time, custo_batalha, custo_total,
                      energia_final, solucao_valida)


def imprimir_titulo(texto):
    print()
    print("=" * 70)
    print(texto)
    print("=" * 70)


def imprimir_solucao(solucao):
    """Pokémon usados em cada batalha, energia final e custo total."""
    print(f"  {'Ginásio':<8} {'Dific.':>6}  {'Pokémon':<28} {'Poder':>5}  {'Tempo':>7}")
    for g in range(NUM_GINASIOS):
        time = [NOMES_POKEMONS[p] for p in range(NUM_POKEMONS) if solucao[g][p] == 1]
        print(f"  {NOMES_GINASIOS[g]:<8} {DIFICULDADES[g]:>6}  {', '.join(time):<28} "
              f"{poder_do_time(solucao[g]):>5.1f}  {custo_batalha(g, solucao[g]):>7.2f}")

    print("\n  Energia final de cada Pokémon:")
    energias = energia_final(solucao)
    for p in range(NUM_POKEMONS):
        batalhas = config.ENERGIA_INICIAL - energias[p]
        print(f"    {NOMES_POKEMONS[p]:<12} lutou {batalhas} vezes -> energia final {energias[p]}")

    print(f"\n  Solução respeita as restrições? {'Sim' if solucao_valida(solucao) else 'Não'}")
    print(f"  Custo total das batalhas: {custo_total(solucao):.4f} minutos")


def imprimir_estatisticas(estatisticas):
    melhor, media, desvio, vezes_no_melhor, num_execucoes = estatisticas
    print(f"  Execuções:                  {num_execucoes}")
    print(f"  Melhor custo:               {melhor:.4f}")
    print(f"  Média:                      {media:.4f}")
    print(f"  Desvio-padrão:              {desvio:.4f}")
    print(f"  Vezes que atingiu o melhor: {vezes_no_melhor}")


def imprimir_comparacao(nome_1, estat_1, nome_2, estat_2):
    """Tabela lado a lado com as estatísticas de dois algoritmos."""
    linhas = ["Melhor custo", "Média", "Desvio-padrão", "Vezes no seu melhor", "Execuções"]
    print(f"  {'':<18} {nome_1:>20} {nome_2:>22}")
    for i, nome_linha in enumerate(linhas):
        valor_1 = estat_1[i]
        valor_2 = estat_2[i]
        if isinstance(valor_1, float):
            print(f"  {nome_linha:<18} {valor_1:>20.4f} {valor_2:>22.4f}")
        else:
            print(f"  {nome_linha:<18} {valor_1:>20} {valor_2:>22}")