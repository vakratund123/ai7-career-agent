import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.core.config import STATIC_DIR, DATA_DIR, EXPORTS_DIR
from backend.db.database import init_db
from backend.db.seed import seed_database
from backend.api.routes import router as api_router
from backend.services.scheduler import scheduler

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("ai7.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing AI7 Career Agent Platform...")
    init_db()
    # Check if database has been seeded; if not, seed it
    from backend.db.database import get_db
    with get_db() as conn:
        count = conn.execute("SELECT count(*) FROM companies").fetchone()[0]
        if count == 0:
            logger.info("Seeding initial target companies and candidate CV...")
            seed_database()

    # Start the autonomous background scheduler
    await scheduler.start()
    logger.info("AI7 Career Agent is live and operating.")
    yield
    await scheduler.stop()
    logger.info("AI7 Career Agent shutting down.")

app = FastAPI(
    title="AI7 Career Agent",
    description="Autonomous Multi-Agent Career Operating System for AI7 PRIVATE LIMITED",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# Mount frontend static files
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=False)
