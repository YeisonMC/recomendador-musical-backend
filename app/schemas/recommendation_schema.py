from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    selected_songs: list[str] = Field(
        ...,
        min_length=1,
        description="Lista de IDs de canciones seleccionadas por el usuario."
    )
    top_n: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Cantidad máxima de recomendaciones a devolver."
    )


class RecommendationItem(BaseModel):
    song_id: str
    name: str
    artist: str | None = None
    genre: str | None = None
    release_year: int | None = None
    score: float
    usuarios_similares: list[str]
    camino_bfs: str


class RecommendationResponse(BaseModel):
    selected_songs: list[str]
    recommendations: list[RecommendationItem]