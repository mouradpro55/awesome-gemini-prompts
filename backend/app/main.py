from fastapi import FastAPI
from app.api.routes import auth
from app.db.database import engine, Base
from app.core.config import settings

# Create all tables in the database (for testing/development purposes)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to LocalReach API"}