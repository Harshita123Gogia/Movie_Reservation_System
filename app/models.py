from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class ReservationStatus(str, enum.Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default=UserRole.USER)

    reservations = relationship("Reservation", back_populates="user")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    poster_url = Column(String)
    genre = Column(String, nullable=False)

    showtimes = relationship("Showtime", back_populates="movie", cascade="all, delete")

class Showtime(Base):
    __tablename__ = "showtimes"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    total_seats = Column(Integer, default=40)

    movie = relationship("Movie", back_populates="showtimes")
    reservations = relationship("Reservation", back_populates="showtime", cascade="all, delete")

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    showtime_id = Column(Integer, ForeignKey("showtimes.id"), nullable=False)
    seat_number = Column(Integer, nullable=False)
    status = Column(String, default=ReservationStatus.CONFIRMED)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reservations")
    showtime = relationship("Showtime", back_populates="reservations")

    __table_args__ = (
        UniqueConstraint('showtime_id', 'seat_number', name='_showtime_seat_uc'),
    )