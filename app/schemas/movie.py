from dataclasses import Field
from datetime import datetime
from typing import List

from pydantic import BaseModel

class Movie(BaseModel):
    name: str
    id_movie: int
    poster: str
    state: str
    id_type: List[int]
    class Config:
        orm_mode = True

class ListMovies(BaseModel):
    movies: List[Movie]
    class Config:
        orm_mode = True
class MovieBaner(BaseModel):
    banner: str
    id_movie: int
    class Config:
        orm_mode = True
class ListMovieBanners(BaseModel):
    movies: List[MovieBaner]
class MovieType(BaseModel):
    id_movie: int
    id_type: int
class MovieDetail(BaseModel):
    id_movie: int
    name: str
    actor: str
    director: str
    type: List[str]
    time : int
    poster: str
    overview: str
    state: str
    class Config:
        orm_mode = True
