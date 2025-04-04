from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.schemas import *
from app import model
from typing import Optional
from app.ultils import *

router=APIRouter(
    prefix="/movie",tags=["Movies"]
)

@router.get("/",status_code=status.HTTP_200_OK, response_model=ListMovies)
def get_movies(state: Optional[str] = None, type_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(model.Movie)
    if type_id is not None:
        query=query.join(model.MovieType).filter(model.MovieType.id_type==type_id)

    if state is not None:
        query=query.filter(model.Movie.state==state)
    movies = query.all()
    if not movies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found")

    print(len(movies))
    return {"movies": movies}

@router.get("/recent", status_code=status.HTTP_200_OK,response_model=ListMovies)
def get_7_recent_movies(db: Session = Depends(get_db)):
    """
    Lấy 7 phim mới ra mắt (NOW_SHOWING) gần đây nhất,
    dựa trên trường time_release (mới nhất => time_release lớn nhất).
    """
    movies = (db.query(model.Movie)
                .filter(model.Movie.state == "NOW_SHOWING")      # Chỉ lấy phim đang chiếu
                .order_by(model.Movie.time_release.desc())       # Sắp xếp theo time_release giảm dần
                .limit(7)                                        # Lấy tối đa 7 phim
                .all())

    if not movies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy phim nào"
        )

    return {"movies": movies}

@router.get("/banner",status_code=status.HTTP_200_OK,response_model=ListMovieBanners)
def get_movie_banners(state :str,db:Session=Depends(get_db )):
    movies=db.query(model.Movie).filter(model.Movie.state==state , model.Movie.banner.isnot(None)).all()
    if not movies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    print(len(movies))
    return {"movies":movies}
@router.get("/{id}", status_code=status.HTTP_200_OK,response_model=MovieDetail)
async def get_details(id: int,db: Session = Depends(get_db) ):
    movie = db.query(model.Movie).join(model.MovieType).join(model.Type).filter(model.Movie.id_movie==id).all()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    types =[mt.type.name for m in movie for mt in m.movie_type]

    response ={
        "id_movie":id,
        "name":movie[0].name,
        "type":types,
        "actor":movie[0].actor,
        "director":movie[0].director,
        "time":movie[0].time,
        "poster":movie[0].poster,
        "overview":movie[0].overview,
        "state":movie[0].state,
    }
    return response