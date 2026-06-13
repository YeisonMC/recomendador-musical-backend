from fastapi import APIRouter

from app.repositories.csv_repository import load_nodes

router = APIRouter()


@router.get("/songs")
def get_songs():
    nodes = load_nodes()

    songs = nodes[nodes["node_type"] == "song"].copy()

    result = []

    for _, row in songs.iterrows():
        result.append({
            "song_id": row["node_id"],
            "name": row["name"],
            "artist": row["artist"] if "artist" in row and not str(row["artist"]) == "nan" else None,
            "genre": row["genre"] if "genre" in row and not str(row["genre"]) == "nan" else None,
            "release_year": int(float(row["release_year"]))
            if "release_year" in row and str(row["release_year"]).strip() not in ["", "nan"]
            else None
        })

    return {
        "total": len(result),
        "songs": result[:100]
        #    "songs": result
    }