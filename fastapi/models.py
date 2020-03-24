from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from .database import Base

#Model for users, declaring email as primary key and interacting with groups table with group_id foreign key
#All user information is required for different parts of the front end application
class User(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True, unique=True, index=True)
    name = Column(String, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    day = Column(String, index=True, default=True)

    allGroups = relationship("Group", back_populates="allUsers")
    availabilityUsers = relationship("Space_Availability", back_populates="usersActive")

#Model for groups, declaring group_id as the primary key and using space_id to connect with the space table
#All information is required for interactions on the front end application.
class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    space_id = Column(Integer, ForeignKey("spaces.space_id"))

    allUsers = relationship("User", back_populates="allGroups")

    allSpaces = relationship("Space", back_populates="spaceGroup")

#Model for spaces, declaring space_id as the primary key and a disabled boolean field which recieves special treatment if true
class Space(Base):
    __tablename__ = "spaces"

    space_id = Column(Integer, primary_key=True, index=True)
    disabled = Column(Boolean, default = False)

    spaceGroup = relationship("Group", back_populates="allSpaces")
    availabilitySpaces = relationship("Space_Availability", back_populates="spacesActive")

#Model for space reservations, using space_id as the foreign key and primary key to connct woth the space data.
#Also declares user_id and date which are needed for space validation
class Space_Availability(Base):
    __tablename__ = "space_availability"

    space_id = Column(Integer, ForeignKey("spaces.space_id"),primary_key=True)
    user_id = Column(Integer, ForeignKey("users.email"))
    date = Column(Date,primary_key=True, index = True)

    spacesActive = relationship("Space", back_populates="availabilitySpaces")
    usersActive = relationship("User", back_populates="availabilityUsers")


