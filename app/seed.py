from datetime import datetime, timedelta
from .database import SessionLocal, engine, Base
from .models import User, Movie, Showtime, UserRole
from .auth import get_password_hash

def seed_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Create default admin user
    admin = User(
        username="admin",
        email="admin@cinema.com",
        hashed_password=get_password_hash("admin123"),
        role=UserRole.ADMIN
    )
    db.add(admin)

    # Movie definitions paired with unique daily showtime hours (hour, minute)
    movies_with_schedules = [
        {
            "movie": {
                "title": "Inception",
                "description": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
                "poster_url": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=600&q=80",
                "genre": "Sci-Fi"
            },
            "slots": [(10, 15), (13, 45), (17, 30), (21, 00)]  # 10:15 AM, 1:45 PM, 5:30 PM, 9:00 PM
        },
        {
            "movie": {
                "title": "The Dark Knight",
                "description": "When the menace known as the Joker wreaks havoc and chaos on Gotham, Batman must accept one of the greatest psychological and physical tests.",
                "poster_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=600&q=80",
                "genre": "Action"
            },
            "slots": [(11, 00), (14, 30), (18, 15), (22, 00)]  # 11:00 AM, 2:30 PM, 6:15 PM, 10:00 PM
        },
        {
            "movie": {
                "title": "Interstellar",
                "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
                "poster_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=600&q=80",
                "genre": "Sci-Fi"
            },
            "slots": [(9, 30), (13, 00), (16, 45), (20, 30)]  # 9:30 AM, 1:00 PM, 4:45 PM, 8:30 PM
        },
        {
            "movie": {
                "title": "Dune: Part Two",
                "description": "Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family.",
                "poster_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=600&q=80",
                "genre": "Adventure"
            },
            "slots": [(10, 45), (14, 15), (19, 00), (22, 30)]  # 10:45 AM, 2:15 PM, 7:00 PM, 10:30 PM
        },
        {
            "movie": {
                "title": "Oppenheimer",
                "description": "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.",
                "poster_url": "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?auto=format&fit=crop&w=600&q=80",
                "genre": "Drama"
            },
            "slots": [(12, 00), (15, 45), (19, 30)]           # 12:00 PM, 3:45 PM, 7:30 PM
        },
        {
            "movie": {
                "title": "Spider-Man: Across the Spider-Verse",
                "description": "Miles Morales catapults across the Multiverse, where he encounters a team of Spider-People charged with protecting its existence.",
                "poster_url": "https://images.unsplash.com/photo-1635805737707-575885ab0820?auto=format&fit=crop&w=600&q=80",
                "genre": "Animation"
            },
            "slots": [(11, 30), (15, 00), (18, 30), (21, 30)]  # 11:30 AM, 3:00 PM, 6:30 PM, 9:30 PM
        }
    ]

    now = datetime.now()

    for item in movies_with_schedules:
        # Save movie
        movie = Movie(**item["movie"])
        db.add(movie)
        db.commit()
        db.refresh(movie)

        # Generate unique showtimes for the next 5 days
        for day_offset in range(0, 5):
            target_date = now + timedelta(days=day_offset)
            
            for hour, minute in item["slots"]:
                slot_datetime = target_date.replace(
                    hour=hour, 
                    minute=minute, 
                    second=0, 
                    microsecond=0
                )
                
                showtime = Showtime(
                    movie_id=movie.id,
                    start_time=slot_datetime,
                    total_seats=36
                )
                db.add(showtime)

    db.commit()
    db.close()
    print("Database successfully seeded with unique showtimes for each movie.")

if __name__ == "__main__":
    seed_db()
