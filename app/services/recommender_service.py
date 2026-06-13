import pandas as pd

from app.repositories.csv_repository import load_graph_data
from app.algorithms.bfs import bfs_adjacency_list, reconstruct_path


def build_graph(nodes: pd.DataFrame, likes_edges: pd.DataFrame):
    """
    Construye la lista de adyacencia para recorrer el grafo.

    Aunque la relación original es Usuario -> Canción,
    para el recorrido BFS se utiliza como no dirigido:
    Usuario - Canción - Usuario - Canción.
    """
    node_ids = nodes["node_id"].tolist()

    id_to_idx = {node_id: index for index, node_id in enumerate(node_ids)}
    idx_to_id = {index: node_id for node_id, index in id_to_idx.items()}

    node_type = dict(zip(nodes["node_id"], nodes["node_type"]))

    graph = [[] for _ in range(len(nodes))]
    weights = {}

    for _, row in likes_edges.iterrows():
        source = row["source_id"]
        target = row["target_id"]
        weight = float(row["weight"])

        if source in id_to_idx and target in id_to_idx:
            u = id_to_idx[source]
            v = id_to_idx[target]

            graph[u].append(v)
            graph[v].append(u)

            weights[(source, target)] = weight
            weights[(target, source)] = weight

    return graph, id_to_idx, idx_to_id, node_type, weights


def create_temporary_user(
    nodes: pd.DataFrame,
    likes_edges: pd.DataFrame,
    selected_song_ids: list[str]
):
    """
    Crea un usuario temporal U_NEW conectado a las canciones seleccionadas.
    """
    temporary_user = {
        "node_id": "U_NEW",
        "node_type": "user",
        "name": "Usuario Nuevo",
        "age": "",
        "favorite_genre": "",
        "artist": "",
        "genre": "",
        "release_year": ""
    }

    nodes_with_user = pd.concat(
        [nodes, pd.DataFrame([temporary_user])],
        ignore_index=True
    )

    temporary_edges = []

    for index, song_id in enumerate(selected_song_ids):
        temporary_edges.append({
            "edge_id": f"E_NEW_{index + 1}",
            "source_id": "U_NEW",
            "target_id": song_id,
            "relation_type": "LIKES",
            "weight": 1.0,
            "listen_count": 50,
            "rating": 5
        })

    edges_with_user = pd.concat(
        [likes_edges, pd.DataFrame(temporary_edges)],
        ignore_index=True
    )

    return nodes_with_user, edges_with_user


def recommend_songs_for_temporary_user(
    selected_song_ids: list[str],
    top_n: int = 5
):
    """
    Genera recomendaciones usando:
    - BFS como algoritmo de recorrido.
    - Filtro colaborativo basado en usuarios.
    - Pesos para ordenar las recomendaciones.
    """
    nodes, likes_edges = load_graph_data()

    valid_song_ids = set(
        nodes[nodes["node_type"] == "song"]["node_id"]
    )

    invalid_songs = [
        song_id for song_id in selected_song_ids
        if song_id not in valid_song_ids
    ]

    if invalid_songs:
        raise ValueError(f"Las siguientes canciones no existen en el dataset: {invalid_songs}")

    nodes, likes_edges = create_temporary_user(
        nodes,
        likes_edges,
        selected_song_ids
    )

    graph, id_to_idx, idx_to_id, node_type, weights = build_graph(
        nodes,
        likes_edges
    )

    user_id = "U_NEW"
    user_index = id_to_idx[user_id]

    path, distance = bfs_adjacency_list(graph, user_index)

    user_songs = set(selected_song_ids)

    similar_users = []

    for index, dist in enumerate(distance):
        node_id = idx_to_id[index]

        if (
            dist == 2
            and node_type.get(node_id) == "user"
            and node_id != user_id
        ):
            similar_users.append(node_id)

    recommendations = {}

    for similar_user in similar_users:
        similar_user_songs_df = likes_edges[
            likes_edges["source_id"] == similar_user
        ]

        similar_user_songs = set(similar_user_songs_df["target_id"])

        common_songs = user_songs.intersection(similar_user_songs)

        if not common_songs:
            continue

        similarity = 0

        for song_id in common_songs:
            target_weight = weights.get((user_id, song_id), 0)
            similar_weight = weights.get((similar_user, song_id), 0)

            similarity += min(target_weight, similar_weight)

        for _, row in similar_user_songs_df.iterrows():
            candidate_song = row["target_id"]

            if candidate_song not in user_songs:
                candidate_weight = float(row["weight"])
                score = similarity * candidate_weight

                if candidate_song not in recommendations:
                    recommendations[candidate_song] = {
                        "song_id": candidate_song,
                        "score": 0,
                        "usuarios_similares": set(),
                        "camino_bfs": None
                    }

                recommendations[candidate_song]["score"] += score
                recommendations[candidate_song]["usuarios_similares"].add(similar_user)

                candidate_index = id_to_idx[candidate_song]

                recommendations[candidate_song]["camino_bfs"] = reconstruct_path(
                    path,
                    user_index,
                    candidate_index,
                    idx_to_id
                )

    results = []

    for song_id, info in recommendations.items():
        song_data = nodes[nodes["node_id"] == song_id].iloc[0]

        release_year = song_data["release_year"]

        if pd.isna(release_year) or str(release_year).strip() == "":
            release_year = None
        else:
            release_year = int(float(release_year))

        results.append({
            "song_id": song_id,
            "name": song_data["name"],
            "artist": song_data["artist"] if not pd.isna(song_data["artist"]) else None,
            "genre": song_data["genre"] if not pd.isna(song_data["genre"]) else None,
            "release_year": release_year,
            "score": round(info["score"], 4),
            "usuarios_similares": sorted(list(info["usuarios_similares"])),
            "camino_bfs": " → ".join(info["camino_bfs"])
        })

    results = sorted(
        results,
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_n]