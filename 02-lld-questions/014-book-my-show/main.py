"""

Requirements:
- Users will see a movie list and select a movie
- Selected movies will have a list of venues
- Each venue will have a calander of that movie timings
- users can give number of seats to book.
- User have to pay and get confermation notifications



Classes:
User
Movie Class (can have different movie types like 3d, 2d, etc. for future use)
Venue
Show class - movie, start time, end time
Booking - user, seats, movie, venue, timings
controller of movie booking

"""

# 12:23
from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
import datetime



class Booking:
    show: Show
    booked_by: User
    seats_booked: int
    price: int
    timestamp: datetime.datetime

    def __init__(self, show: Show, booked_by: User, seats_booked: int):
        self.show = show
        self.booked_by = booked_by
        self.seats_booked = seats_booked
        self.price = self.show.price * self.seats_booked
        self.timestamp = datetime.datetime.now()


class User:
    id: int
    name: int

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

class MovieTypeEnum(Enum):
    THREE_D = 1
    TWO_D = 2


class Movie:
    id: int
    name: str
    description: str
    duration: float
    type: MovieTypeEnum

    def __init__(self, id: int, name: str, description: str, duration: float, type: MovieTypeEnum):
        self.id = id
        self.name = name
        self.description = description
        self.duration = duration
        self.type = type
    
    def __repr__(self):
        return self.name

class Show:
    id: int
    movie: Movie
    start_time: datetime.datetime
    end_time: datetime.datetime
    theater: Theater
    seat_count: int
    price: int
    

    def __init__(self, id: int, movie: Movie, start_time: datetime.datetime, end_time: datetime.datetime, theater: Theater, price: int, seat_count: int):
        self.id = id
        self.movie = movie
        self.start_time = start_time
        self.end_time = end_time
        self.theater = theater
        self.price = price
        self.seat_count = seat_count



class Theater:
    id: int
    name: str
    description: str
    shows: list[Show]
    bookings: list[Booking]

    def __init__(self, id: int, name: str, description: str, shows: list[Show]):
        self.id = id
        self.name = name
        self.description = description
        self.shows = shows
        self.bookings = []
    
    def has_movie(self, movie):
        for show in self.shows:
            hosted_movie = show.movie
            if movie.id == hosted_movie.id:
                return True
    
    def movie_shows(self, movie):
        shows = []
        for show in self.shows:
            hosted_movie = show.movie
            if movie.id == hosted_movie.id:
                shows.append(show)
        
        return shows

    def book_show(self, show: Show, seat_count: int, user: User):
        seats_booked = 0
        for booking in self.bookings:
            if booking.show.id == show.id:
                seats_booked += booking.seats_booked
        
        if seats_booked + seat_count > show.seat_count:
            return None
        
        booking = Booking(show, user, seat_count)
        self.bookings.append(booking)
        return booking





class MovieBookingSystemController:

    def __init__(self):
        self.users = []
        self.movies = []
        self.theaters: list[Theater] = []


    
    def add_user(self, user: User):
        self.users.append(user)
    
    def add_movies(self, movie: Movie):
        self.movies.append(movie)

    def add_theater(self, theater: Theater):
        self.theaters.append(theater)
    
    def list_movies(self):
        return ', '.join([str(movie) for movie in self.movies])
    
    def list_theater(self, movie):
        theaters = []
        for theater in self.theaters:
            if theater.has_movie(movie):
                theaters.append(theater)
    
        return theaters
    
    def theater_shows(self, theater: Theater, movie: Movie):
        return theater.movie_shows(movie)
    
    def book_show(self, theater: Theater, show: Show, user: User, seat_count: int):
        booking = theater.book_show(show, seat_count, user)
        return booking
    

if __name__ == "__main__":
    # Step 1: Create users
    user1 = User(1, "Alice")
    user2 = User(2, "Bob")

    # Step 2: Create movies
    movie1 = Movie(101, "Inception", "Sci-fi thriller", 2.5, MovieTypeEnum.TWO_D)
    movie2 = Movie(102, "Avatar", "Fantasy epic", 3.0, MovieTypeEnum.THREE_D)

    # Step 3: Create showtimes
    start1 = datetime.datetime(2025, 7, 5, 18, 0)
    end1 = datetime.datetime(2025, 7, 5, 20, 30)
    start2 = datetime.datetime(2025, 7, 5, 21, 0)
    end2 = datetime.datetime(2025, 7, 5, 23, 30)

    # Step 4: Create shows (without theater reference yet)
    show1 = Show(1, movie1, start1, end1, None, price=250, seat_count=50)
    show2 = Show(2, movie2, start2, end2, None, price=300, seat_count=40)

    # Step 5: Create a theater and assign shows
    theater1 = Theater(1, "INOX Cinema", "Downtown multiplex", [show1, show2])
    show1.theater = theater1
    show2.theater = theater1

    # Step 6: Setup booking controller
    controller = MovieBookingSystemController()
    controller.add_user(user1)
    controller.add_user(user2)
    controller.add_movies(movie1)
    controller.add_movies(movie2)
    controller.add_theater(theater1)

    # Step 7: Display available movies
    print("📽️ Available Movies:")
    print(controller.list_movies())

    # Step 8: Display theaters playing 'Inception'
    print("\n🏢 Theaters playing Inception:")
    for t in controller.list_theater(movie1):
        print(f"- {t.name}")

    # Step 9: Display showtimes for 'Inception'
    print("\n🎞️ Shows for 'Inception':")
    for show in controller.theater_shows(theater1, movie1):
        print(f"Show ID: {show.id}, Time: {show.start_time.strftime('%H:%M')} to {show.end_time.strftime('%H:%M')}, Price: ₹{show.price}")

    # Step 10: Perform bookings
    print("\n✅ Booking 3 seats for Alice in Show 1:")
    booking1 = controller.book_show(theater1, show1, user1, 3)
    print("Booking successful!" if booking1 else "Booking failed!")

    print("\n✅ Booking 47 seats for Bob in Show 1 (should succeed):")
    booking2 = controller.book_show(theater1, show1, user2, 47)
    print("Booking successful!" if booking2 else "Booking failed!")

    print("\n❌ Booking 1 more seat for Alice in Show 1 (should fail - overbook):")
    booking3 = controller.book_show(theater1, show1, user1, 1)
    print("Booking successful!" if booking3 else "Booking failed!")