from heapq import heappop, heappush
from itertools import count

from networkx.algorithms.shortest_paths.weighted import _weight_function
from haversine import haversine


# Função heurística - distância entre dois pontos palicando haversine
## Utiliza lat/long e considera curvatura da terra
def heuristica(node_A, node_B, df):
    coord_a = (0, 0)
    coord_b = (0, 0)
    flag = 0

    try:
        ca_X = df.loc[(df['label_source'] == node_A)]['pos_X'].iloc[0]
        ca_Y = df.loc[(df['label_source'] == node_A)]['pos_Y'].iloc[0]
        coord_a = (ca_X, ca_Y)
    except IndexError:
        ca_X, ca_Y = None, None
        flag = 1

    try:
        cb_X = df.loc[(df['label_source'] == node_B)]['pos_X'].iloc[0]
        cb_Y = df.loc[(df['label_source'] == node_B)]['pos_Y'].iloc[0]
        coord_b = (cb_X, cb_Y)
    except IndexError:
        cb_X, cb_Y = None, None
        flag = -1

    if flag == 1: coord_a = coord_b
    if flag == -1: coord_b = coord_a

    return haversine(coord_a, coord_b)


# Algoritmo Best first*
def best_first(grafo, no_origem, no_destino, df, peso="weight" ):
    # Ações da fila
    push = heappush
    pop = heappop
    contador = count()

    fila = [(0, next(contador), no_origem, 0, None)]

    # Controle dos nós abertos e visitados
    abertos = {}  # abertos[nó] = (caminho total ate o no, heuristica)
    visitados = {}

    while fila:
        # atualiza o no atual, a distancia atual e o no anterior a partir da fila
        _, _, no_atual, dist, no_anterior = pop(fila)

        # Condição de parada - achou o destino
        if no_atual == no_destino:
            resposta = [no_atual]
            no_aux = no_anterior

            while no_aux is not None:
                resposta.append(no_aux)
                no_aux = visitados[no_aux]
            resposta.reverse()
            return resposta

        # Caso o nó atual já tenha sido visitado
        if no_atual in visitados:

            # Caso especial : primeira chamada
            if visitados[no_atual] is None:
                continue

            custo_abertos, custo_heuri = abertos[no_atual]
            if custo_abertos < dist:
                continue

        visitados[no_atual] = no_anterior

        # Para cada vizinho
        for vizinho, peso in grafo[no_atual].items():
            # Compute o custo entre ele e o nó atual
            custo = 0
            custo_novo = dist + custo

            if vizinho in abertos:
                custo_abertos, custo_heuri = abertos[vizinho]
                # Verificação se o custo de um nó já aberto é menor que custo desse nó pelo caminho atual
                ## Caso seja não substitui -  o caminho existente já é melhor
                if custo_abertos <= custo_novo:
                    continue
            else:
                custo_heuri = heuristica(vizinho, no_destino, df)

            abertos[vizinho] = custo_novo, custo_heuri
            custo = custo_novo + custo_heuri
            push(fila, (custo, next(contador), vizinho, custo_novo, no_atual))


def best_first_distancia(grafo, no_origem, no_destino, df, peso="weight"):
    path = best_first(grafo, no_origem, no_destino, df, peso)
    weight_func = _weight_function(grafo, peso)

    if (len(path) > 1):
        total_weight = 0
        for u, v in zip(path[:-1], path[1:]):
            weight_uv = weight_func(u, v, grafo[u][v])
            total_weight += weight_uv

        return total_weight

    return -1



# Algoritmo A*
def a_estrela(grafo, no_origem, no_destino, df,  peso="weight"):
    # Ações da fila
    push = heappush
    pop = heappop
    contador = count()
    weight_func = _weight_function(grafo, peso)

    fila = [(0, next(contador), no_origem, 0, None)]

    # Controle dos nós abertos e visitados
    abertos = {}  # abertos[nó] = (caminho total ate o no, heuristica)
    visitados = {}

    while fila:
        # atualiza o no atual, a distancia atual e o no anterior a partir da fila
        _, _, no_atual, dist, no_anterior = pop(fila)

        # Condição de parada - achou o destino
        if no_atual == no_destino:
            resposta = [no_atual]
            no_aux = no_anterior

            while no_aux is not None:
                resposta.append(no_aux)
                no_aux = visitados[no_aux]
            resposta.reverse()
            return resposta

        # Caso o nó atual já tenha sido visitado
        if no_atual in visitados:

            # Caso especial : primeira chamada
            if visitados[no_atual] is None:
                continue

            custo_abertos, custo_heuri = abertos[no_atual]
            if custo_abertos < dist:
                continue

        visitados[no_atual] = no_anterior

        # Para cada vizinho
        for vizinho, peso in grafo[no_atual].items():
            # Compute o custo entre ele e o nó atual
            custo = weight_func(no_atual, vizinho, peso)

            # if custo is None:
            #     continue # verificação de custo invalido
            #
            custo_novo = dist + custo

            if vizinho in abertos:
                custo_abertos, custo_heuri = abertos[vizinho]
                # Verificação se o custo de um nó já aberto é menor que custo desse nó pelo caminho atual
                ## Caso seja não substitui -  o caminho existente já é melhor
                if custo_abertos <= custo_novo:
                    continue
            else:
                custo_heuri = heuristica(vizinho, no_destino, df)

            abertos[vizinho] = custo_novo, custo_heuri
            custo = custo_novo + custo_heuri
            push(fila, (custo, next(contador), vizinho, custo_novo, no_atual))


def a_estrela_distancia(grafo, no_origem, no_destino, df, peso="weight"):
    path = a_estrela(grafo, no_origem, no_destino,df, peso)
    weight_func = _weight_function(grafo, peso)

    total_weight = 0
    for u, v in zip(path[:-1], path[1:]):
        weight_uv = weight_func(u, v, grafo[u][v])
        total_weight += weight_uv

    return total_weight


# Algoritmo busca profundidade

def dfs_path(G, source, target):
    caminho = None
    pilha = [(source, [source])]
    visitados = []

    while pilha:
        no_atual, caminho = pilha.pop(0)

        if no_atual == target:
            return caminho

        if no_atual not in visitados:
            visitados.append(no_atual)

            vizinhos = list(G.neighbors(no_atual))
            for index, vizinho in enumerate(vizinhos):
                if vizinho not in visitados:
                    pilha.insert(index, (vizinho, caminho + [vizinho]))


def dfs_distancia(grafo, no_origem, no_destino, peso="weight"):
    path = dfs_path(grafo, no_origem, no_destino)
    weight_func = _weight_function(grafo, peso)

    total_weight = 0
    for u, v in zip(path[:-1], path[1:]):
        weight_uv = weight_func(u, v, grafo[u][v])
        total_weight += weight_uv

    return total_weight