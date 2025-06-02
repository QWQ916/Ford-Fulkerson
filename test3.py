import networkx as nx
import matplotlib.pyplot as plt

# Ваша матрица смежности
matrix = [
    [0, 7, 4, 0, 0, 0],  # A (0)
    [0, 0, 4, 0, 2, 0],  # B (1)
    [0, 4, 0, 4, 8, 0],  # C (2)
    [0, 0, 0, 0, 0, 12],  # D (3)
    [0, 0, 0, 4, 0, 5],  # E (4)
    [0, 0, 0, 0, 0, 0]  # F (5)
]

node_labels = ['A', 'B', 'C', 'D', 'E', 'F']


def build_graph_from_matrix(matrix): # из матрицы смежности получаем списки смежности, чтобы работать с ними легче в алгоритме
    G = nx.DiGraph() # делаем граф ориентированным
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 0:
                G.add_edge(i, j, capacity=matrix[i][j])
                if not G.has_edge(j, i):
                    G.add_edge(j, i, capacity=0)
    return G


def draw_graph(G_residual, path=None, title=""):
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G_residual)

    # Вершины с буквенными подписями
    labels_nodes = {i: node_labels[i] for i in G_residual.nodes()}
    nx.draw_networkx_nodes(G_residual, pos, node_color='lightblue', node_size=700)
    nx.draw_networkx_labels(G_residual, pos, font_size=14, font_weight='bold', labels=labels_nodes)

    # Ребра
    nx.draw_networkx_edges(G_residual, pos, width=1.5)

    # Метки ребер: текущий поток / емкость
    labels = {}
    for u, v in G_residual.edges():
        cap = G_residual[u][v]['capacity']
        flow = G_residual[u][v].get('flow', 0)
        labels[(u, v)] = f"{flow}/{cap}"

    nx.draw_networkx_edge_labels(G_residual, pos, label_pos=0.3, font_size=10, edge_labels=labels)

    # Выделение выбранного пути красным
    if path:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G_residual, pos,
                               edgelist=path_edges,
                               edge_color='red',
                               width=3)

    plt.title(title)
    plt.axis('off')
    plt.show()


def dfs_find_path(G_residual, s, t): # DFS алгоритм для нахождения пути
    visited = set()

    def dfs(u):
        if u == t:
            return [u]
        visited.add(u)
        for v in G_residual.neighbors(u):
            residual_cap = G_residual[u][v]['capacity'] - G_residual[u][v].get('flow', 0)
            if residual_cap > 1e-8 and v not in visited:
                result = dfs(v)
                if result:
                    return [u] + result
        return None

    return dfs(s)


def ford_fulkerson(matrix): # алогритм Форда-Фалкерсона с визуализацией
    G = build_graph_from_matrix(matrix)

    s = 0  # A
    t = len(matrix) - 1  # F

    max_flow = 0

    while True:
        path = dfs_find_path(G, s, t)
        if not path:
            break

        # Находим минимальный остаточный поток вдоль пути
        residuals = []
        for u, v in zip(path[:-1], path[1:]):
            cap = G[u][v]['capacity']
            flow = G[u][v].get('flow', 0)
            residuals.append(cap - flow)
        bottleneck = min(residuals)

        # Обновляем потоки по пути
        for u, v in zip(path[:-1], path[1:]):
            G[u][v]['flow'] = G[u][v].get('flow', 0) + bottleneck
            G[v][u]['flow'] = G[v][u].get('flow', 0) - bottleneck

        max_flow += bottleneck

        draw_graph(G,
                   path=path,
                   title=f"Найденный DFS путь: {' -> '.join(node_labels[i] for i in path)}\nМаксимальный поток на данной итерации: {max_flow}")

    print(f"Максимальный поток сети: {max_flow}")


# Запуск алгоритма
ford_fulkerson(matrix)