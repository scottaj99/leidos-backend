from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session


from . import crud, models, schemas
from .database import SessionLocal, engine
from datetime import date
from starlette.middleware.cors import CORSMiddleware


'''
This declares all get/post/delete methods that are required for the front end to recieve and send information.
It uses the models to interact with the database and calls on methods called in crud.py to carry out each task
'''

#Declare the middleware and urls which can interavt with the middleware
app = FastAPI()
origins = [
    "http://localhost:19000",
    "http://localhost:19006",
    "http://localhost:8000",
    "http://192.168.1.66:19006"
]
#Configure apps middleware settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#Create all models and connect to db
models.Base.metadata.create_all(bind=engine)



# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

#declare delete method for removing users from db
@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if db_user:
        return crud.delete_user(db=db, email=email)
#declare post request to create a user
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

#get request to return all users
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

#get request to return the users based on their group_id
@app.get("/users/group/{group_id}", response_model=List[schemas.User])
def read_user(group_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_users_by_group(db, group_id=group_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#get user whos email matches that in the url
@app.get("/users/email/{email}", response_model=schemas.User)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



#post request to add a new group
@app.post("/groups/", response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    db_group = crud.get_group_by_space(db, space_id=group.space_id)
    if db_group:
        raise HTTPException(status_code=400, detail="Space already occupied by group")
    return crud.create_group(db=db, group=group)

#get request to return a group based on a group_id
@app.get("/groups/{group_id}", response_model=schemas.Group)
def read_group(group_id: int, db: Session = Depends(get_db)):
    db_group = crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

#get request to return all groups
@app.get("/groups/", response_model=List[schemas.Group])
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    groups = crud.get_groups(db, skip=skip, limit=limit)
    return groups

#delete request to delete a group based on the group id
@app.delete("/groups/{group_id}", response_model=schemas.Group)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    db_group = crud.get_group(db, group_id=group_id)
    if db_group:
        return crud.delete_group(db=db, group_id=group_id)



#post request adds a new space to the spaces db
@app.post("/spaces/", response_model=schemas.Space)
def create_space(space: schemas.SpaceCreate, db: Session = Depends(get_db)):
    db_space = crud.get_space(db, space_id=space.space_id)
    if db_space:
        raise HTTPException(status_code=400, detail="Space already exists")
    return crud.create_space(db=db, space=space)

#post request adds a new reservation to the space availability model
@app.post("/spaces/availability", response_model=schemas.Space_Availability)
def create_space_occupied_on_date(space_available: schemas.Space_AvailabilityCreate, db: Session = Depends(get_db)):
    db_space_availability = crud.get_valid_datespace_availability(db, date = space_available.date, space_id = space_available.space_id)
    db_user_availability = crud.get_valid_userspace_availability(db, user_id = space_available.user_id, date = space_available.date)
    if db_space_availability:
        raise HTTPException(status_code=400, detail="Space already occupied on date")
    if db_user_availability:
        raise HTTPException(status_code=400, detail="User already occupies a space on this date")    
    return crud.create_space_availability_taken(db=db, space_available=space_available)

#get request to return all spaces reserved on the given date
@app.get("/spaces/availability/date/{date}", response_model=List[schemas.Space_Availability])
def read_space_availability(date: date,db: Session = Depends(get_db)):
    db_space_available = crud.get_space_availability_by_date(db, date=date)
    if db_space_available is None:
        return db_space_available
    return db_space_available

#get request to return all spaces reserved by a given user
@app.get("/spaces/availability/user/{user_id}", response_model=List[schemas.Space_Availability])
def read_space_user(user_id: str,db: Session = Depends(get_db)):
    db_space_available = crud.get_space_availability_by_user(db, user_id=user_id)
    if db_space_available is None:
        return db_space_available
    return db_space_available

#get request to return all space reservations
@app.get("/spaces/availability", response_model=List[schemas.Space_Availability])
def read_all_spaces_availability(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    spaces_available = crud.get_spaces_availability(db, skip=skip, limit=limit)
    return spaces_available

#get request to return all spaces
@app.get("/spaces/", response_model=List[schemas.Space])
def read_spaces(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    spaces = crud.get_spaces(db, skip=skip, limit=limit)
    return spaces

#get request to return the space information give the space id
@app.get("/spaces/{space_id}", response_model=schemas.Space)
def read_space(space_id: int, db: Session = Depends(get_db)):
    db_space = crud.get_space(db, space_id=space_id)
    if db_space is None:
        raise HTTPException(status_code=404, detail="Space not found")
    return db_space

#delete method to remove a space from the db
@app.delete("/spaces/{space_id}", response_model=schemas.Space)
def delete_space(space_id: int, db: Session = Depends(get_db)):
    db_space = crud.get_space(db, space_id=space_id)
    if db_space:
        return crud.delete_space(db=db, space_id=space_id)

#delete method to remove a space reservation
@app.delete("/spaces/availability/{user_id}/{date}/{space_id}", response_model=schemas.Space_Availability)
def delete_space_avail(space_id: int, user_id: str, date: date, db: Session = Depends(get_db)):
    db_space_availability = crud.space_availability_check(space_id=space_id, user_id=user_id, date=date, db=db)
    if db_space_availability:
            return crud.delete_space_avail(db=db, space_id=space_id, user_id=user_id, date=date)















