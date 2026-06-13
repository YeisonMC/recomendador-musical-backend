from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"

NODES_CSV_PATH = DATA_DIR / "grafo_nodos.csv"
EDGES_CSV_PATH = DATA_DIR / "aristas_musica.csv"

API_TITLE = "API Recomendador Musical"
API_VERSION = "1.0.0"