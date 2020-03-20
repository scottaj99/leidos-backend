from sqlalchemy.orm import Session
from datetime import date

from . import models, schemas

#For get method to return a user based on their email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

#For get method, return a group of users based on their group
def get_users_by_group(db: Session, group_id: int):
    return db.query(models.User).filter(models.User.group_id == group_id).all()

#for get method, returns all users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

#for post method, creates a new user object and adds it to the database
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, name=user.name, group_id=user.group_id, day=user.day)
    #registration=user.registration
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#for delete method, removes the user from the database based on their email
def delete_user(db: Session, email: str):
    db.query(models.User).filter(models.User.email == email).delete()
    db.commit()
    return 


#for get method, returns the group based on the group_id requested
def get_group(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()

#for get method, returns all groups
def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Group).offset(skip).limit(limit).all()

#for get method, returns a group based on their space_id
def get_group_by_space(db: Session, space_id: int):
    return db.query(models.Group).filter(models.Group.space_id == space_id).first()

#for post method, creates a new group and adds it to the database
def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(space_id = group.space_id)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

#for delete method, removes the group from the database based on the group_id entered
def delete_group(db: Session, group_id: int):
    db.query(models.Group).filter(models.Group.id==group_id).delete()
    db.commit()
    return 

#for get method, checks to see if the given space id is available on the given date
def get_valid_datespace_availability(db, date = date, space_id=int):
    return db.query(models.Space_Availability).filter(models.Space_Availability.space_id == space_id).filter(models.Space_Availability.date == date).first()

#for get method, ensures that a user hasn't booked more than one space in a day
def get_valid_userspace_availability(db, date = date, user_id=str):
    return db.query(models.Space_Availability).filter(models.Space_Availability.date == date).filter(models.Space_Availability.user_id == user_id).first()

#for get method, returns the space based on the space_id requested
def get_space(db: Session, space_id: int):
    return db.query(models.Space).filter(models.Space.space_id == space_id).first()

#for get method, returns all spaces
def get_spaces(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Space).offset(skip).limit(limit).all()

#For post method, creates a new space and adds it to the database
def create_space(db: Session, space: schemas.SpaceCreate):
    db_space = models.Space(space_id = space.space_id, disabled = space.disabled)
    db.add(db_space)
    db.commit()
    db.refresh(db_space)
    return db_space

#For delete method, removes a space from the database based on the space_id
def delete_space(db: Session, space_id: int):
    db.query(models.Space).filter(models.Space.space_id==space_id).delete()
    db.commit()
    return 


#for a post method, creates a new reservation of a space
def create_space_availability_taken(db: Session, space_available: schemas.Space_AvailabilityCreate):
    db_space_availability = models.Space_Availability(space_id = space_available.space_id, user_id = space_available.user_id, date = space_available.date)
    db.add(db_space_availability)
    db.commit()
    db.refresh(db_space_availability)
    return db_space_availability

#get method, to see if a space is taken by a user on a set day
def space_availability_check(space_id: int, user_id: str, date: date, db: Session):
    return db.query(models.Space_Availability).filter(models.Space_Availability.date == date).filter(models.Space_Availability.user_id == user_id).filter(models.Space_Availability.space_id == space_id).first()

# def get_space_availability_by_date(db: Session, space_id: int, date: datetime.date):
#     return db.query(models.Space_Availability).filter(models.Space_Availability.space_id == space_id,models.Space_Availability.date == date).first()

#for get method, returns all spaces reserved on the given date
def get_space_availability_by_date(db: Session,date: date):
    return db.query(models.Space_Availability).filter(models.Space_Availability.date == date).all()

#for get method, returns all spaces reserved by a given user
def get_space_availability_by_user(db: Session,user_id: str):
    return db.query(models.Space_Availability).filter(models.Space_Availability.user_id == user_id).all()

#get method, returns all space reservations regardless of user, time or space_id
def get_spaces_availability(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Space_Availability).offset(skip).limit(limit).all()

#delete method, finds a space reservation based on the date, spaceid and userid and deletes it
def delete_space_avail(db: Session, space_id: int, user_id: str, date: date):
    db.query(models.Space_Availability).filter(models.Space_Availability.date == date).filter(models.Space_Availability.user_id == user_id).filter(models.Space_Availability.space_id == space_id).delete()
    db.commit()
    return