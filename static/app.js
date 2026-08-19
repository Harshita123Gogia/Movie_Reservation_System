let selectedShowtimeId = null;
let selectedSeats = [];
let isSignUp = false;

document.addEventListener("DOMContentLoaded", () => {
    const dateInput = document.getElementById("date-filter");
    if (dateInput) {
        // Set default filter date to today's date
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        dateInput.value = `${year}-${month}-${day}`;
    }
    checkUser();
    loadMovies();
});

function checkUser() {
    const token = localStorage.getItem("token");
    const authControls = document.getElementById("auth-controls");
    if (token && authControls) {
        authControls.innerHTML = `
            <a href="/admin" class="text-sm font-semibold text-slate-300 hover:text-white mr-2">Admin Panel</a>
            <button onclick="logout()" class="bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-semibold px-4 py-2 rounded-lg transition border border-slate-700">Logout</button>
        `;
    }
}

async function loadMovies() {
    const dateInput = document.getElementById("date-filter");
    const dateVal = dateInput ? dateInput.value : "";
    
    const url = dateVal ? `/api/movies?date_filter=${dateVal}` : "/api/movies";
    
    try {
        const res = await fetch(url);
        const movies = await res.json();
        const container = document.getElementById("movie-list");

        if (!movies || movies.length === 0) {
            container.innerHTML = `<div class="col-span-full text-center py-12 text-slate-500">No showtimes available for the selected date.</div>`;
            return;
        }

        container.innerHTML = movies.map(movie => `
            <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden flex flex-col justify-between shadow-xl hover:border-slate-700 transition">
                <div>
                    <div class="relative h-64 overflow-hidden">
                        <img src="${movie.poster_url}" alt="${movie.title}" class="w-full h-full object-cover">
                        <span class="absolute top-3 left-3 bg-red-600/90 text-white text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-md backdrop-blur-sm">${movie.genre}</span>
                    </div>
                    <div class="p-5">
                        <h3 class="text-xl font-bold text-white mb-2">${movie.title}</h3>
                        <p class="text-slate-400 text-xs line-clamp-3 leading-relaxed mb-4">${movie.description}</p>
                    </div>
                </div>
                <div class="p-5 pt-0 border-t border-slate-800/50 mt-auto">
                    <p class="text-[11px] font-bold text-slate-400 tracking-wider uppercase mb-3 pt-4">Available Showtimes</p>
                    <div class="flex flex-wrap gap-2">
                        ${movie.showtimes && movie.showtimes.length > 0 ? movie.showtimes.map(st => {
                            const showTimeStr = new Date(st.start_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                            return `
                                <button onclick="openSeatModal(${st.id}, '${movie.title.replace(/'/g, "\\'")}', '${showTimeStr}')" 
                                    class="bg-slate-800 hover:bg-red-600 text-slate-200 hover:text-white text-xs font-semibold px-3 py-2 rounded-lg transition border border-slate-700/60 flex items-center gap-1">
                                    🕒 ${showTimeStr}
                                </button>
                            `;
                        }).join('') : '<span class="text-xs text-slate-500 italic">No showtimes scheduled</span>'}
                    </div>
                </div>
            </div>
        `).join('');
    } catch (err) {
        console.error("Failed to load movies:", err);
    }
}

async function openSeatModal(showtimeId, movieTitle, showtimeStr) {
    if (!localStorage.getItem("token")) {
        alert("Please sign in first to reserve seats.");
        showAuthModal(true);
        return;
    }

    selectedShowtimeId = showtimeId;
    selectedSeats = [];
    document.getElementById("modal-movie-title").innerText = movieTitle;
    document.getElementById("modal-showtime-info").innerText = `Showtime: ${showtimeStr}`;

    try {
        const res = await fetch(`/api/reservations/showtime/${showtimeId}/seats`);
        const data = await res.json();

        const grid = document.getElementById("seat-grid");
        grid.innerHTML = data.seats.map(s => {
            if (s.available) {
                return `
                    <button 
                        type="button"
                        onclick="toggleSeat(${s.seat_number})" 
                        id="seat-${s.seat_number}" 
                        class="p-2.5 text-xs font-bold rounded-lg transition border border-slate-700 bg-slate-800 text-slate-200 hover:border-emerald-500 hover:bg-slate-700"
                    >
                        ${s.seat_number}
                    </button>
                `;
            } else {
                return `
                    <button 
                        type="button"
                        disabled 
                        class="p-2.5 text-xs font-bold rounded-lg bg-red-950/60 border border-red-900/40 text-red-700 cursor-not-allowed"
                    >
                        ${s.seat_number}
                    </button>
                `;
            }
        }).join('');

        updateSelectedCount();
        document.getElementById("seat-modal").classList.remove("hidden");
    } catch (err) {
        alert("Error loading seat layout.");
    }
}

function toggleSeat(seatNum) {
    const btn = document.getElementById(`seat-${seatNum}`);
    if (selectedSeats.includes(seatNum)) {
        selectedSeats = selectedSeats.filter(s => s !== seatNum);
        btn.className = "p-2.5 text-xs font-bold rounded-lg transition border border-slate-700 bg-slate-800 text-slate-200 hover:border-emerald-500 hover:bg-slate-700";
    } else {
        selectedSeats.push(seatNum);
        btn.className = "p-2.5 text-xs font-bold rounded-lg transition bg-emerald-600 text-white border border-emerald-500 shadow-md shadow-emerald-600/30";
    }
    updateSelectedCount();
}

function updateSelectedCount() {
    document.getElementById("selected-count").innerText = `${selectedSeats.length} seat(s) selected`;
}

function closeSeatModal() {
    document.getElementById("seat-modal").classList.add("hidden");
}

async function confirmBooking() {
    if (selectedSeats.length === 0) return alert("Please select at least one seat.");

    try {
        const res = await fetch("/api/reservations", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("token")}`
            },
            body: JSON.stringify({ showtime_id: selectedShowtimeId, seat_numbers: selectedSeats })
        });

        if (res.ok) {
            alert("Seats successfully reserved!");
            closeSeatModal();
            loadMovies();
        } else {
            const err = await res.json();
            alert(`Reservation failed: ${err.detail}`);
        }
    } catch (err) {
        alert("An error occurred while confirming reservation.");
    }
}

function showAuthModal(show) {
    document.getElementById("auth-modal").classList.toggle("hidden", !show);
}

function toggleAuthMode() {
    isSignUp = !isSignUp;
    document.getElementById("auth-title").innerText = isSignUp ? "Create Account" : "Sign In";
    document.getElementById("email-field-container").classList.toggle("hidden", !isSignUp);
    document.getElementById("auth-toggle-btn").innerText = isSignUp ? "Have an account? Sign In" : "Need an account? Register";
}

async function handleAuth(e) {
    e.preventDefault();
    const username = document.getElementById("auth-username").value;
    const password = document.getElementById("auth-password").value;

    if (isSignUp) {
        const email = document.getElementById("auth-email").value;
        const res = await fetch("/api/auth/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password })
        });
        if (res.ok) {
            alert("Account created successfully! Please sign in.");
            toggleAuthMode();
        } else {
            const err = await res.json();
            alert(`Signup failed: ${err.detail}`);
        }
    } else {
        const formData = new URLSearchParams();
        formData.append("username", username);
        formData.append("password", password);

        const res = await fetch("/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData
        });

        if (res.ok) {
            const data = await res.json();
            localStorage.setItem("token", data.access_token);
            showAuthModal(false);
            location.reload();
        } else {
            alert("Invalid username or password.");
        }
    }
}

function logout() {
    localStorage.removeItem("token");
    location.reload();
}