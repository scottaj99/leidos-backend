from pydantic import BaseModel
from datetime import date

#This script defines any data sent and recieved by the api to model it properly in delivering to the front end app
#or recieving and inserting into the database

#For validating user data
class UserBase(BaseModel):
    email: str
    name: str
    group_id: int
    day: str
   # registration: str
    

#for post request on user
class UserCreate(UserBase):
    pass

#for configuring user data
class User(UserBase):
    #id: int

    class Config:
        orm_mode = True



#for validating user data
class GroupBase(BaseModel):
    space_id: int

#For post request of a new group
class GroupCreate(GroupBase):
    pass

#auto generate group_id
class Group(GroupBase):
    id: int

    class Config:
        orm_mode = True


#for validating space data
class SpaceBase(BaseModel):
    space_id: int
    disabled: bool

#for posting a new space
class SpaceCreate(SpaceBase):
    pass

#for configuring a space
class Space(SpaceBase):
    class Config:
        orm_mode = True


#for posting a new space reservation
class Space_AvailabilityBase(BaseModel):
    date: date
    space_id: int
    user_id: str

    class Config:
        orm_mode = True

#for post request on spaceAvailability
class Space_AvailabilityCreate(Space_AvailabilityBase):
    pass

#for configuring a space_availability object
class Space_Availability(Space_AvailabilityBase):

    class Config:
        orm_mode = True