import pandas as pd

from app.core.config import NODES_CSV_PATH, EDGES_CSV_PATH


def load_nodes() -> pd.DataFrame:
    """
    Carga el archivo CSV de nodos.
    """
    return pd.read_csv(NODES_CSV_PATH)


def load_edges() -> pd.DataFrame:
    """
    Carga el archivo CSV de aristas.
    """
    return pd.read_csv(EDGES_CSV_PATH)


def load_graph_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Carga nodos y aristas del grafo.
    """
    nodes = load_nodes()
    edges = load_edges()

    likes_edges = edges[edges["relation_type"] == "LIKES"].copy()

    return nodes, likes_edges