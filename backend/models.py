from database import Base
from sqlalchemy import Column, Integer, LargeBinary, String, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True,unique=True, nullable=False, autoincrement=True)
    user_name = Column(String, nullable=False,unique=True)
    email =  Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    salt = Column(String, nullable=False)

class Course(Base):
    __tablename__="courses"
    id = Column(Integer, primary_key=True , nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=True)
    salt = Column(String, nullable=True)

    owner = Column(Integer, ForeignKey("users.id"), nullable=False)

    sessions = relationship('Session')
    participants = relationship('Participant')

class Participant(Base):
    __tablename__="participants"
    id = Column(Integer, primary_key=True , nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    
    course = Column(Integer, ForeignKey("courses.id"), nullable=False)

    curves = relationship('Curve')
    responses = relationship('Response')

class Session(Base):
    __tablename__="sessions"
    id = Column(Integer, primary_key=True , nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=True)
    salt = Column(String, nullable=True)
    
    course = Column(Integer, ForeignKey("courses.id"), nullable=False)

    responses = relationship('Response')
    curves = relationship('Curve')

class Response(Base):
    __tablename__="responses"

    id = Column(Integer, primary_key=True , nullable=False, autoincrement=True)
    what = Column(String, nullable=True) # What happend
    when = Column(String, nullable=True) # When did it happen
    thoughts = Column(String, nullable=True) # What did you think
    feelings = Column(String, nullable=True) # What did you feel
    actions = Column(String, nullable=True) # What did you do
    consequences = Column(String, nullable=True) # Where there any consequences

    session = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    participant = Column(Integer, ForeignKey("participants.id"), nullable=False)
    curve = Column(Integer, ForeignKey("curves.id"), nullable=False)

class Curve(Base):
    __tablename__="curves"

    id = Column(Integer, primary_key=True , nullable=False, autoincrement=True)
    data = Column(LargeBinary, nullable=False) # Pickled list of curve data

    session = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    participant = Column(Integer, ForeignKey("participants.id"), nullable=False)
    
    responses = relationship('Response')

    