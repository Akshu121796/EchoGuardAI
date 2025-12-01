from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.analysis import router as analysis_router
from routers.results import router as results_router

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(
    title="EchoGuard AI Backend",
    description="Fake News & Misinformation Detection System",
    version="1.0.0"
)

# Enable CORS for local development (allow all origins for simplicity)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(analysis_router)
app.include_router(results_router)


@app.get("/health")
def health():
    return {"status": "ok"}


# Optional: serve frontend static files if frontend folder exists next to workspace root
try:
    # Compute frontend path relative to this file: two parents up -> workspace root
    frontend_path = Path(__file__).resolve().parents[2] / "echoguard_frontend" / "Mumbai hacks"
    if frontend_path.exists():
        app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
        print(f"✅ Serving frontend from: {frontend_path}")
    else:
        print(f"ℹ️ Frontend folder not found at: {frontend_path}")
except Exception as e:
    print("❌ Error mounting frontend static files:", e)
