from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import Reservation, Showtime, Movie, ReservationStatus
from ..auth import require_admin

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/reports")
def get_reports(db: Session = Depends(get_db), current_user = Depends(require_admin)):
    TICKET_PRICE = 12.50
    total_reservations = db.query(Reservation).filter(Reservation.status == ReservationStatus.CONFIRMED).count()
    revenue = total_reservations * TICKET_PRICE

    showtimes = db.query(Showtime).all()
    occupancy_report = []

    for st in showtimes:
        booked = db.query(Reservation).filter(
            Reservation.showtime_id == st.id,
            Reservation.status == ReservationStatus.CONFIRMED
        ).count()
        capacity_percentage = round((booked / st.total_seats) * 100, 2) if st.total_seats > 0 else 0
        occupancy_report.append({
            "showtime_id": st.id,
            "movie_title": st.movie.title,
            "start_time": st.start_time,
            "booked_seats": booked,
            "total_seats": st.total_seats,
            "occupancy": f"{capacity_percentage}%"
        })

    return {
        "total_active_reservations": total_reservations,
        "total_revenue": f"${revenue:.2f}",
        "occupancy": occupancy_report
    }