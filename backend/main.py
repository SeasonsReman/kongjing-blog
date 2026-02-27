from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routes.posts import router as posts_router
from routes.tasks import router as tasks_router
from routes.notes import router as notes_router

app = FastAPI(title="空·境 Blog API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(posts_router)
app.include_router(tasks_router)
app.include_router(notes_router)


@app.get("/")
def root():
    return {"message": "空·境 Blog API is running ✨"}
