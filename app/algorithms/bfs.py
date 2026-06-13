def bfs_adjacency_list(graph: list[list[int]], start: int):
    """
    Ejecuta BFS sobre una lista de adyacencia.

    Retorna:
    - path: arreglo de padres para reconstruir caminos.
    - distance: distancia desde el nodo inicial.
    """
    n = len(graph)

    visited = [False] * n
    path = [-1] * n
    distance = [-1] * n

    queue = [start]
    visited[start] = True
    distance[start] = 0

    while queue:
        current = queue.pop(0)

        for neighbor in graph[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                path[neighbor] = current
                distance[neighbor] = distance[current] + 1
                queue.append(neighbor)

    return path, distance


def reconstruct_path(path: list[int], start: int, end: int, idx_to_id: dict[int, str]) -> list[str]:
    """
    Reconstruye el camino BFS desde el nodo inicial hasta un nodo destino.
    """
    route = []
    current = end

    while current != -1:
        route.append(current)

        if current == start:
            break

        current = path[current]

    route.reverse()

    return [idx_to_id[index] for index in route]