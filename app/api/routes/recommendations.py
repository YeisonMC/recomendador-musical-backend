from fastapi import APIRouter, HTTPException

from app.schemas.recommendation_schema import (
    RecommendationRequest,
    RecommendationResponse
)
from app.services.recommender_service import recommend_songs_for_temporary_user

router = APIRouter()


@router.post(
    "/recommendations",
    response_model=RecommendationResponse
)
def get_recommendations(request: RecommendationRequest):
    try:
        recommendations = recommend_songs_for_temporary_user(
            selected_song_ids=request.selected_songs,
            top_n=request.top_n
        )

        return {
            "selected_songs": request.selected_songs,
            "recommendations": recommendations
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )