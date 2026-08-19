from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .database import engine, Base
from .routers import auth, movies, reservations, admin
from .seed import seed_db

Base.metadata.create_all(bind=engine)
seed_db()

app = FastAPI(title="Movie Reservation API")

app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(reservations.router)
app.include_router(admin.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/admin")
def read_admin():
    return FileResponse("static/admin.html")