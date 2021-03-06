import datetime

from pydantic import BaseModel, Field


class BookingCreate(BaseModel):
    user_id: int
    room_id: int
    booked_num: int
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime

class BookingUpdate(BaseModel):
    booking: int
    user_id: int
    room_id: int
    booked_num: int
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime

class BookingDelete(BookingCreate):
    booking_id: int


class Booking(BookingCreate):
    booking_id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str = Field(max_length=12)


class UserUpdate(BaseModel):
    user_id: int
    username: str = Field(max_length=12)

class UserDelete(BaseModel):
    user_id: int


class User(UserCreate):
    user_id: int

    class Config:
        orm_mode = True


class RoomCreate(BaseModel):
    room_name: str = Field(max_length=12)
    capacity: int

class RoomUpdate(BaseModel):
    room_id: int
    room_name: str = Field(max_length=12)
    capacity: int

class RoomDelete(BaseModel):
    room_id: int


class Room(RoomCreate):
    room_id: int

    class Config:
        orm_mode = True
