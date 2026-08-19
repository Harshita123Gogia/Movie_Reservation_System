from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from ..database import get_db
from ..models import Movie, Showtime
from ..schemas import MovieCreate, MovieResponse, ShowtimeCreate, ShowtimeResponse
from ..auth import require_admin

router = APIRouter(prefix="/api/movies", tags=["Movies"])

@router.get("", response_model=List[MovieResponse])
def get_movies(date_filter: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Movie)
    movies = query.all()
    if date_filter:
        target_date = datetime.strptime(date_filter, "%Y-%m-%d").date()
        for movie in movies:
            movie.showtimes = [st for st in movie.showtimes if st.start_time.date() == target_date]
    return movies

@router.post("", response_model=MovieResponse)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    db_movie = Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return {"message": "Movie deleted successfully"}

@router.post("/showtimes", response_model=ShowtimeResponse)
def add_showtime(showtime: ShowtimeCreate, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    movie = db.query(Movie).filter(Movie.id == showtime.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db_showtime = Showtime(**showtime.dict())
    db.add(db_showtime)
    db.commit()
    db.refresh(db_showtime)
    return db_showtime