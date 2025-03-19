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

router=APIRouter(prefix="/room",tags=['Room'])
@router.get("/",status_code=status.HTTP_200_OK)
def get_room(id_showtime:int,db:Session()=Depends(get_db)):
    result=db.query(model.SeatStatus).join(model.Room,model.Room.id_room==model.SeatStatus.id_room).filter(model.SeatStatus.id_showtime==id_showtime).all()
    room_type= result[0].room.type
    return {"type":room_type}
