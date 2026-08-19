from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class MovieBase(BaseModel):
    title: str
    description: str
    poster_url: str
    genre: str

class MovieCreate(MovieBase):
    pass

class ShowtimeBase(BaseModel):
    start_time: datetime
    total_seats: int = 40

class ShowtimeCreate(ShowtimeBase):
    movie_id: int

class ShowtimeResponse(ShowtimeBase):
    id: int
    movie_id: int

    class Config:
        from_attributes = True

class MovieResponse(MovieBase):
    id: int
    showtimes: List[ShowtimeResponse] = []

    class Config:
        from_attributes = True

class ReservationCreate(BaseModel):
    showtime_id: int
    seat_numbers: List[int]

class ReservationResponse(BaseModel):
    id: int
    showtime_id: int
    seat_number: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True