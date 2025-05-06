from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from app.core.database import get_db
from sqlalchemy.sql import func
from sqlalchemy import cast, Time
from app.model import Showtime
from app.schemas import *
from app import model
from typing import Optional, List
from app.ultils import *

from datetime import date,time,datetime
router=APIRouter(prefix="/receipt",tags=['Receipt'])
@router.post('/',status_code=status.HTTP_201_CREATED)
def create_receipt(receipt_data: CreateReceipt,db:Session=Depends(get_db)):
    new_receipt=model.Receipt(time=datetime.now(),method_pay="VNPAY",state="PAID",id_user=receipt_data.id_user)
    db.add(new_receipt)
    db.flush()
    for food in receipt_data.foods:
        receipt_food=model.ReceiptFood(
            id_receipt=new_receipt.id_receipt,
            id_food=food.id_food,
            quantity=food.quantity,
        )
        db.add(receipt_food)
    for ticket in receipt_data.tickets:
        db.add(model.Ticket(
            id_seat=ticket.id_seat,
            id_room=ticket.id_room,
            id_showtime=ticket.id_showtime,
            price=ticket.price,
            receipt_id=new_receipt.id_receipt
        ))
        seat = db.query(model.SeatStatus).filter(
            model.SeatStatus.id_seat == ticket.id_seat,
            model.SeatStatus.id_room == ticket.id_room,
            model.SeatStatus.id_showtime == ticket.id_showtime
        ).first()
        seat.state="BOOKED"
    db.commit()
    db.refresh(new_receipt)
    return Response(status_code=status.HTTP_201_CREATED)
@router.get("/detail/{receipt_id}",status_code=status.HTTP_200_OK,response_model=ReceiptDetail)
def get_receipt(receipt_id:int,db:Session=Depends(get_db)):
    receipt = db.query(model.Receipt).filter(model.Receipt.id_receipt == receipt_id).first()
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")

    foods = [
        {
            "id_food": rf.food.id_food,
            "name": rf.food.name,
            "price": rf.food.price,
            "quantity": rf.quantity,
            "total": rf.food.price * rf.quantity
        }
        for rf in receipt.receipt_foods
    ]
    total_food = sum(item["total"] for item in foods)

    tickets = []
    for t in receipt.tickets:
        room = db.query(model.Room).filter(model.Room.id_room == t.id_room).first()
        cinema = db.query(model.Cinema).filter(model.Cinema.id_cinema == room.id_cinema).first() if room else None
        tickets.append({
            "id_ticket": t.id_ticket,
            "price": t.price,
            "id_seat": t.id_seat,
            "id_room": t.id_room,
            "id_showtime": t.id_showtime,
            "room_name": room.name if room else None,
            "cinema_name": cinema.name if cinema else None
        })
    total_ticket = sum(t.price for t in receipt.tickets)
    total_amount = total_food + total_ticket
    return {
        "id_receipt": receipt.id_receipt,
        "time": receipt.time,
        "method_pay": receipt.method_pay,
        "state": receipt.state,
        "foods": foods,
        "tickets": tickets,
        "total_amount": total_amount
    }
@router.get("/list/",status_code=status.HTTP_200_OK,response_model=List[ListReceipts])
def get_List_Receipt(id_user:int,db:Session= Depends(get_db)):
    receipts= (
        db.query(model.Receipt.id_receipt,
                 model.Movie.name.label("movie_name"),
                 model.Showtime.time_begin,
                 model.Cinema.name.label("cinema_name"),
                 model.Seat.name.label("seat_name")
        )
        .join(model.Ticket,model.Ticket.receipt_id==model.Receipt.id_receipt)
        .join(model.Showtime, model.Ticket.id_showtime==model.Showtime.id_showtime)
        .join(model.Movie,model.Showtime.id_movie==model.Movie.id_movie)
        .join(model.Room, model.Room.id_room == model.Ticket.id_room)
        .join(model.Cinema, model.Cinema.id_cinema == model.Room.id_cinema)
        .join(model.Seat, (model.Seat.id_seat == model.Ticket.id_seat) & (model.Seat.id_room == model.Ticket.id_room))
        .filter(model.Receipt.id_user == id_user)
        .all()

    )
    result={}
    for id_receipt, movie_name, time_begin,cinema_name,seat_name in receipts:
        if id_receipt not in result:
            result[id_receipt] = {
                "id_receipt": id_receipt,
                "movie_name": movie_name,
                "date_begin": time_begin.date(),
                "time_begin": time_begin.time(),
                "cinema_name": cinema_name,
                "seats":[]
            }
            result[id_receipt]["seats"].append(seat_name)
    return list(result.values())
