from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
from pydantic import EmailStr


class Cinema(Base):
    __tablename__ = 'cinema'
    id_cinema = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255))


class Room(Base):
    __tablename__ = 'room'
    id_room = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50))
    id_cinema = Column(Integer, ForeignKey('cinema.id_cinema', onupdate="CASCADE"), nullable=False)

    cinema = relationship("Cinema", backref="rooms")


class Seat(Base):
    __tablename__ = 'seat'
    id_seat = Column(Integer, primary_key=True, autoincrement=True)
    id_room = Column(Integer, ForeignKey('room.id_room', onupdate="CASCADE"), nullable=False)
    name = Column(String(50), nullable=False)
    type = Column(String(50))

    room = relationship("Room", backref="seats")


class Showtime(Base):
    __tablename__ = 'showtime'
    id_showtime = Column(Integer, primary_key=True, autoincrement=True)
    time_begin = Column(DateTime, nullable=False)
    id_room = Column(Integer, ForeignKey('room.id_room', onupdate="CASCADE"), nullable=False)
    id_movie = Column(Integer, ForeignKey('movie.id_movie', onupdate="CASCADE"), nullable=False)
    room = relationship("Room", backref="showtimes")


class Movie(Base):
    __tablename__ = 'movie'
    id_movie = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    time = Column(Integer)
    age_limit = Column(Enum('NONE', 'T13', 'T18', name="movie_age_limit"), nullable=False, default="NONE")
    director = Column(String(255))
    actor = Column(String(255))
    poster = Column(String(255))
    banner = Column(String(255))
    time_release = Column(DateTime)
    overview = Column(String(5000))
    state = Column(Enum('COMING_SOON', 'NOW_SHOWING', 'ENDED', name="movie_state"), nullable=False,
                   default="COMING_SOON")

    showtime = relationship("Showtime", backref="movies")
    @property
    def id_type(self):
        return [mt.id_type for mt in self.movie_type]

class Ticket(Base):
    __tablename__ = 'ticket'
    id_ticket = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Float, nullable=False)
    id_seat = Column(Integer, ForeignKey('seat.id_seat', onupdate="CASCADE"), nullable=False)
    id_showtime = Column(Integer, ForeignKey('showtime.id_showtime', onupdate="CASCADE"), nullable=False)

    seat = relationship("Seat", backref="tickets")
    showtime = relationship("Showtime", backref="tickets")


class Receipt(Base):
    __tablename__ = 'receipt'
    id_receipt = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, nullable=False)
    method_pay = Column(String(50))
    state = Column(Enum('PENDING', 'PAID', 'CANCELED', name="payment_state"), nullable=False, default='PENDING')
    id_ticket = Column(Integer, ForeignKey('ticket.id_ticket', onupdate="CASCADE"), nullable=False)
    id_food = Column(Integer, ForeignKey('food.id_food', onupdate="CASCADE"), nullable=True)
    id_user = Column(Integer, ForeignKey('user.id_user', onupdate="CASCADE"), nullable=False)

    ticket = relationship("Ticket", backref="receipts")
    food = relationship("Food", backref="receipts")
    user = relationship("User", backref="receipts")


class Food(Base):
    __tablename__ = 'food'
    id_food = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)


class User(Base):
    __tablename__ = 'user'
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(20))
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    id_role = Column(Integer, ForeignKey('role.id_role', onupdate="CASCADE"), nullable=False)

    # role = relationship("Role", backref="users")


class Role(Base):
    __tablename__ = 'role'
    id_role = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)


class UserReviewMovie(Base):
    __tablename__ = 'user_review_movie'
    id_review = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Float, nullable=False)
    description = Column(String(500))
    id_movie = Column(Integer, ForeignKey('movie.id_movie', onupdate="CASCADE"), nullable=False)
    id_user = Column(Integer, ForeignKey('user.id_user', onupdate="CASCADE"), nullable=False)

    movie = relationship("Movie", backref="reviews")
    user = relationship("User", backref="reviews")


class Type(Base):
    __tablename__ = 'type'
    id_type = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

class  MovieType(Base):
    __tablename__ = 'movie_type'
    id_type = Column(Integer, ForeignKey('type.id_type', onupdate="CASCADE"), primary_key=True)
    id_movie = Column(Integer, ForeignKey('movie.id_movie', onupdate="CASCADE"), primary_key=True)
    movie = relationship("Movie", backref="movie_type")
    type = relationship("Type", backref="movie_type")

