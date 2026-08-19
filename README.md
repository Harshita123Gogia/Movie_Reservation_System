# 🎬 CineReserve - Movie Ticket Booking System

CineReserve is a modern full-stack web application for browsing movies, viewing dynamically scheduled showtimes, and reserving seats in real-time. Built with **FastAPI**, **SQLAlchemy**, and modern frontend tools.

---

## 🚀 Features

* **Dynamic Movie & Showtime Management**: Movies with unique, realistic daily showtime slots across present and future dates.
* **Interactive Cinema Seat Map**: Curved screen interface with color-coded seats (Available, Selected, and Occupied).
* **Direct Seat Reservation**: Select multiple seats and lock them instantly.
* **User Authentication**: Secure JWT-based registration and login system.
* **Background Email Notifications**: Dispatches ticket reservation details asynchronously upon booking.
* **Date Filtering**: Browse showtimes for today and upcoming dates seamlessly.

---

## 🛠️ Tech Stack

* **Backend**: FastAPI, SQLAlchemy, Pydantic, SQLite
* **Frontend**: HTML5, JavaScript (ES6+), Tailwind CSS
* **Authentication**: OAuth2 with Password Hashing (Passlib / Bcrypt) & JWT

---

## ⚙️ Getting Started

**1. Prerequisites**
Ensure you have **Python 3.9+** installed on your system.

**2. Clone the Repository**
```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/Movie_Reservation_System.git](https://github.com/YOUR_GITHUB_USERNAME/Movie_Reservation_System.git)
cd Movie_Reservation_System

```

**3. Install Dependencies**

```bash
pip install -r requirements.txt

```

**4. Database Setup & Seeding**
To clear old data and seed the database with current movies and staggered showtimes:

```bash
python -m app.seed

```

**5. Running the Application**
Start the local development server:

```bash
uvicorn app.main:app --reload

```

Open your browser and navigate to:

```text
[http://127.0.0.1:8000](http://127.0.0.1:8000)

```

**6. Default Admin Credentials**

* **Username**: `admin`
* **Password**: `admin123`


git push origin main

```
