from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from typing import List
from ..database import get_db
from ..models import Reservation, Showtime, User, ReservationStatus
from ..schemas import ReservationCreate, ReservationResponse
from ..auth import get_current_user

router = APIRouter(prefix="/api/reservations", tags=["Reservations"])

@router.get("/showtime/{showtime_id}/seats")
def get_seat_status(showtime_id: int, db: Session = Depends(get_db)):
    showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")

    reserved_seats = db.query(Reservation.seat_number).filter(
        Reservation.showtime_id == showtime_id,
        Reservation.status == ReservationStatus.CONFIRMED
    ).all()
    reserved_set = {r[0] for r in reserved_seats}

    seats = []
    for i in range(1, showtime.total_seats + 1):
        seats.append({
            "seat_number": i,
            "available": i not in reserved_set
        })
    return {"showtime_id": showtime_id, "total_seats": showtime.total_seats, "seats": seats}

@router.post("", response_model=List[ReservationResponse])
def create_reservation(payload: ReservationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    showtime = db.query(Showtime).filter(Showtime.id == payload.showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")

    if showtime.start_time < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Cannot reserve seats for past showtimes")

    created = []
    try:
        for seat in payload.seat_numbers:
            if seat < 1 or seat > showtime.total_seats:
                raise HTTPException(status_code=400, detail=f"Invalid seat number {seat}")
            
            existing = db.query(Reservation).filter(
                Reservation.showtime_id == payload.showtime_id,
                Reservation.seat_number == seat,
                Reservation.status == ReservationStatus.CONFIRMED
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail=f"Seat {seat} is already reserved")

            res = Reservation(
                user_id=current_user.id,
                showtime_id=payload.showtime_id,
                seat_number=seat,
                status=ReservationStatus.CONFIRMED
            )
            db.add(res)
            created.append(res)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Concurrency error: One or more selected seats were already booked.")

    for res in created:
        db.refresh(res)
    return created

@router.get("/my", response_model=List[ReservationResponse])
def get_my_reservations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Reservation).filter(Reservation.user_id == current_user.id).all()

@router.post("/{reservation_id}/cancel")
def cancel_reservation(reservation_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    res = db.query(Reservation).filter(Reservation.id == reservation_id, Reservation.user_id == current_user.id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Reservation not found")

    if res.showtime.start_time < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Cannot cancel past showtime reservations")

    res.status = ReservationStatus.CANCELLED
    db.commit()
    return {"message": "Reservation cancelled successfully"}