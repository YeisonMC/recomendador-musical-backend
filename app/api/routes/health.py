from fastapi import APIRouter

router = APIRouter()


# @router.get("/health")
# def health_check():
#     return {
#         "status": "ok",
#         "message": "Backend del recomendador musical funcionando correctamente."
#     }

@router.api_route("/health", methods=["GET", "HEAD"])
def health_check():
    return {
        "status": "ok",
        "message": "Backend del recomendador musical funcionando correctamente."
    }