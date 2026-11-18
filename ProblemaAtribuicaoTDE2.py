import numpy as np

custos = [
    [9, 11, 14, 11, 7],
    [6, 15, 13, 13, 10],
    [12, 13, 6, 8, 8],
    [11, 9, 10, 12, 9],
    [7, 12, 14, 10, 14]
]

def procura_zeros(
    matriz: np.ndarray
) -> list[list[int]]:
    zeros = []

    for linha in matriz:
        nova_linha = []

        for valor in linha:
            if valor == 0:
                nova_linha.append(1)
            else:
                nova_linha.append(0)
        zeros.append(nova_linha)
    return zeros

def reduzir_linhas(matriz: np.ndarray) -> None:
    matriz -= matriz.min(axis=1, keepdims=True)

def reduzir_colunas(matriz: np.ndarray) -> None:
    matriz -= matriz.min(axis=0, keepdims=True)

def tentar_atribuir_linha(
    linha: int,
    zeros: list[list[int]],
    linha_por_coluna: list[int],
    visitadas: list[bool]
) -> bool:
    for coluna in range(len(zeros[linha])):
        if not zeros[linha][coluna] or visitadas[coluna]:
            continue

        visitadas[coluna]  = True

        if linha_por_coluna[coluna] == -1 or tentar_atribuir_linha(linha_por_coluna[coluna], zeros, linha_por_coluna, visitadas):
            linha_por_coluna[coluna] = linha
            return True
    return False


def encontrar_atribuicoes(
    matriz: np.ndarray
) -> tuple[list[int], list[int]]:
    n = len(matriz)
    zeros = procura_zeros(matriz)

    linha_por_coluna = [-1] * n

    for linha in range(n):
        visitadas = [False] * n
        tentar_atribuir_linha(linha, zeros, linha_por_coluna, visitadas)

    coluna_por_linha = [-1] * n

    for coluna in range(len(linha_por_coluna)):
        linha = linha_por_coluna[coluna]
        if linha != -1:
            coluna_por_linha[linha] = coluna
    return coluna_por_linha, linha_por_coluna

def cobrir_zeros(
    matriz: np.ndarray,
    coluna_por_linha: list[int],
    linha_por_coluna: list[int]
) -> tuple[list[bool], list[bool]]:
    n = len(matriz)
    zeros = procura_zeros(matriz)

    linhas_marcadas = []
    for i in range(n):
        if coluna_por_linha[i] == -1:
            linhas_marcadas.append(True)
        else:
            linhas_marcadas.append(False)

    colunas_marcadas = [False] * n

    flag = True
    while flag:
        flag = False

        for linha in range(n):
            if not linhas_marcadas[linha]:
                continue

            for coluna in range(n):
                if not zeros[linha][coluna]:
                    continue

                if not colunas_marcadas[coluna]:
                    colunas_marcadas[coluna] = True
                    flag = True

                outra_linha = linha_por_coluna[coluna]

                if outra_linha != -1 and not linhas_marcadas[outra_linha]:
                    linhas_marcadas[outra_linha] = True
                    flag = True

    linhas_cobertas = []
    for i in range(n):
        linhas_cobertas.append(not linhas_marcadas[i])

    colunas_cobertas = colunas_marcadas

    return linhas_cobertas, colunas_cobertas

def hungaro(custos: list[list[int]]) -> tuple[list[int], float]:
    matriz = np.array(custos, dtype=float, copy=True)

    if matriz.ndim != 2 or matriz.shape[0] == 0 or matriz.shape[0] != matriz.shape[1]:
        return

    n = len(matriz)

    reduzir_linhas(matriz)
    reduzir_colunas(matriz)

    while True:
        coluna_por_linha, linha_por_coluna = encontrar_atribuicoes(matriz)

        if -1 not in coluna_por_linha:
            custo_total = 0

            for linha in range(n):
                coluna = coluna_por_linha[linha]
                custo_total += custos[linha][coluna]

            return coluna_por_linha, custo_total

        linhas_cobertas, colunas_cobertas = cobrir_zeros(
            matriz, coluna_por_linha, linha_por_coluna
        )

        nao_cobertos = []

        for linha in range(n):
            for coluna in range(n):
                if not linhas_cobertas[linha] and not colunas_cobertas[coluna]:
                    nao_cobertos.append(matriz[linha, coluna])

        menor_valor = min(nao_cobertos)

        for linha in range(n):
            for coluna in range(n):
                if not linhas_cobertas[linha] and not colunas_cobertas[coluna]:
                    matriz[linha, coluna] -= menor_valor
                elif linhas_cobertas[linha] and colunas_cobertas[coluna]:
                    matriz[linha, coluna] += menor_valor

if __name__ == "__main__":
    coluna_por_linha, custo_total = hungaro(custos)

    for linha in range(len(coluna_por_linha)):
        coluna = coluna_por_linha[linha]
        print(f"Linha {linha} com Coluna {coluna}")

    print(f"Custo total: {custo_total}")
