from fastapi import FastAPI
from app.api.routes import auth
from app.db.database import engine, Base
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

@app.on_event("startup")
def on_startup():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error creating tables: {e}")

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to LocalReach API"}