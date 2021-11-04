import datetime
from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def index():
    return {"message": "Success"}


# @app.post("/users")
# async def users(users: User):
#     return {"users": users}


# @app.post("/rooms")
# async def rooms(rooms: Room):
#     return {"rooms": rooms}


# @app.post("/bookings")
# async def bookings(bookings: Booking):
#     return {"bookings": bookings}


@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    return user


@app.get("/users", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/rooms", response_model=List[schemas.Room])
async def read_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rooms = crud.get_rooms(db, skip=skip, limit=limit)
    return rooms


@app.get("/bookings", response_model=List[schemas.Booking])
async def read_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bookings = crud.get_bookings(db, skip=skip, limit=limit)
    return bookings


@app.post("/users", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.post("/rooms", response_model=schemas.Room)
async def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    return crud.create_room(db, room)


@app.post("/bookings", response_model=schemas.Booking)
async def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    return crud.create_booking(db, booking)


@app.delete("/users/delete", response_model=schemas.User)
async def delete_user(user: schemas.UserDelete, db: Session = Depends(get_db)):
    return crud.delete_user(db, user)


@app.delete("/rooms/delete", response_model=schemas.Room)
async def delete_room(room: schemas.RoomDelete, db: Session = Depends(get_db)):
    return crud.delete_room(db, room)


@app.delete("/bookings/delete", response_model=schemas.Booking)
async def delete_booking(booking: schemas.BookingDelete, db: Session = Depends(get_db)):
    return crud.delete_booking(db, booking)
