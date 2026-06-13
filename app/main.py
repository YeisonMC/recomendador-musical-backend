from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import API_TITLE, API_VERSION
from app.api.routes import health, recommendations
from app.api.routes import health, recommendations, songs

app = FastAPI(
    title=API_TITLE,
    version=API_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173", 
        "https://recomendador-musical-frontend.vercel.app",
        "https://recomendador-musical-frontend-g35gub7cj-yeisonmcs-projects.vercel.app",
    ],
    allow_origin_regex=r"https://recomendador-musical-frontend-.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(recommendations.router, prefix="/api", tags=["Recommendations"])
app.include_router(songs.router, prefix="/api", tags=["Songs"])

@app.get("/")
def root():
    return {
        "message": "API del sistema de recomendación musical."
    }