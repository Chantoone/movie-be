from http.client import HTTPResponse

from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from app.core.database import get_db
from sqlalchemy.sql import func
from sqlalchemy import cast, Time
from app.model import Showtime
from app.schemas import *
from app import model
from typing import Optional
from app.ultils import *

from datetime import date,time,datetime

router=APIRouter(
    prefix="/cinema",tags=["Cinema"]
)
@router.get("/get_cinema/{id_movie}",status_code=status.HTTP_200_OK,response_model=ListCinema)
def get_cinema(id_movie:int,db: Session= Depends(get_db)):
    cinemas=(
        db.query(model.Cinema).join(model.Room, model.Cinema.id_cinema == model.Room.id_cinema)
        .join(model.Showtime,model.Room.id_room==model.Showtime.id_room)
        .filter(model.Showtime.id_movie==id_movie)
        .distinct()
        .all()
    )
    return {"cinemas":cinemas}
@router.get("/get_date/{id_movie}/{id_cinema}",status_code=status.HTTP_200_OK,response_model=ListDate)
def get_date(id_movie:int,id_cinema:int,db: Session=Depends(get_db)):
    now = datetime.utcnow().date()
    dates=(
        db.query(func.date(model.Showtime.time_begin).label("date"))
        .join(model.Room,Showtime.id_room == model.Room.id_room)
        .filter(model.Showtime.id_movie==id_movie,model.Room.id_cinema==id_cinema,
                func.date(Showtime.time_begin) >= now)
        .distinct()
        .all()
    )
    return ListDate(
        id_movie=id_movie,
        id_cinema=id_cinema,
        dates=[row.date for row in dates]
    )
@router.get("/get_time/{id_movie}/{id_cinema}/{date}",status_code=status.HTTP_200_OK,response_model=ListTime)
def get_time(id_movie:int,id_cinema:int,date:str,db: Session=Depends(get_db)):
    date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    times_data=(
        db.query(cast(model.Showtime.time_begin, Time).label("time"),
                 model.Showtime.id_showtime)  # ✅ Sửa lỗi PostgreSQL
        .join(model.Room, model.Room.id_room == model.Showtime.id_room)
        .filter(
            model.Room.id_cinema == id_cinema,
            model.Showtime.id_movie == id_movie,
            func.date(model.Showtime.time_begin) == date_obj
        )
        .distinct()
        .all()
    )
    return ListTime(
        id_movie=id_movie,
        id_cinema=id_cinema,
        date=date,
        times=[row.time for row in times_data],
        id_showtime = times_data[0].id_showtime

    )



