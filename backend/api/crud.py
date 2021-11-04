from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Room).offset(skip).limit(limit).all()


def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.User):
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_room(db: Session, room: schemas.Room):
    db_room = models.Room(room_name=room.room_name, capacity=room.capacity)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def create_booking(db: Session, booking: schemas.Booking):
    # 予約時間の重複チェック
    db_booked = (
        db.query(models.Booking)
        .filter(models.Booking.room_id == booking.room_id)
        .filter(models.Booking.end_datetime > booking.start_datetime)
        .filter(models.Booking.start_datetime < booking.end_datetime)
        .all()
    )

    if len(db_booked) == 0:
        db_booking = models.Booking(
            user_id=booking.user_id,
            room_id=booking.room_id,
            booked_num=booking.booked_num,
            start_datetime=booking.start_datetime,
            end_datetime=booking.end_datetime,
        )
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        return db_booking

    else:
        raise HTTPException(status_code=404, detail="Already booked")


def delete_user(db: Session, user: schemas.UserDelete):
    db_user = db.query(models.User).filter(models.User.user_id == user.user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user


def delete_room(db: Session, room: schemas.RoomDelete):
    db_room = db.query(models.Room).filter(models.Room.room_id == room.room_id).first()
    db.delete(db_room)
    db.commit()
    return db_room


def delete_booking(db: Session, booking: schemas.BookingDelete):
    db_booking = (
        db.query(models.Booking)
        .filter(models.Booking.booking_id == booking.booking_id)
        .first()
    )
    db.delete(db_booking)
    db.commit()
    return db_booking
