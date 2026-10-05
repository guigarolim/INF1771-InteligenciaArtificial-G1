from pathlib import Path
import config


def visualizar_resultado(mapa, resultado, inicio, destino, ginasios, arquivo=None, mostrar=False):
    """Gera uma interface grafica 2D simples com terreno, caminho e estados do A*."""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.colors import ListedColormap
    except ImportError:
        print("Matplotlib nao instalado; visualizacao grafica ignorada.")
        return None

    categorias = {".": 0, "R": 1, "F": 2, "A": 3, "M": 4}
    dados = np.zeros((len(mapa), len(mapa[0])), dtype=int)
    for i, linha in enumerate(mapa):
        for j, c in enumerate(linha):
            dados[i, j] = categorias.get(c, 0)

    cmap = ListedColormap(["#ffffff", "#b0b0b0", "#7fbf7f", "#79bce8", "#9b6b43"])
    fig, ax = plt.subplots(figsize=(18, 6))
    ax.imshow(dados, cmap=cmap, interpolation="nearest", origin="upper")

    if resultado.expandidos_posicoes:
        ys, xs = zip(*resultado.expandidos_posicoes)
        ax.scatter(xs, ys, s=20, c="#ff9800", alpha=0.7, label="Estados expandidos")
    if resultado.fronteira_posicoes:
        ys, xs = zip(*resultado.fronteira_posicoes)
        ax.scatter(xs, ys, s=20, c="#00bcd4", alpha=0.7, label="Fronteira final")

    ys = [p[0] for p in resultado.caminho_grade]
    xs = [p[1] for p in resultado.caminho_grade]
    ax.plot(xs, ys, c="#d50000", linewidth=1.5, label="Caminho final")

    ax.scatter([inicio[1]], [inicio[0]], c="#1565c0", s=80, marker="o", label="Agente/inicio")
    ax.scatter([destino[1]], [destino[0]], c="#6a1b9a", s=100, marker="*", label="Destino U")
    for nome, (l, c) in ginasios.items():
        ax.text(c, l, nome, fontsize=7, ha="center", va="center", fontweight="bold")

    ax.set_title("Busca A*: rota pelos 24 ginasios")
    ax.set_xlabel(f"Custo da rota: {resultado.custo_rota:.2f} min | Estados expandidos: {resultado.estados_expandidos}")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()

    if arquivo is None:
        arquivo = config.ARQUIVO_VISUALIZACAO
    arquivo = Path(arquivo)
    fig.savefig(arquivo, dpi=180, bbox_inches="tight")
    if mostrar:
        plt.show()
    plt.close(fig)
    return str(arquivo)
