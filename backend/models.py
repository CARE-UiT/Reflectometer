import uuid
from database import Base
from sqlalchemy import UUID, Column, Date, Integer, LargeBinary, String, ForeignKey, Text, Float
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True,unique=True, nullable=False, autoincrement=True)
    user_name = Column(String, nullable=False,unique=True)
    email =  Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    salt = Column(String, nullable=False)

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=True)
    salt = Column(String, nullable=True)
    
    date = Column(Date, nullable=False)
    description = Column(Text, nullable=True)

    owner = Column(Integer, ForeignKey("users.id"), nullable=False)

    sessions = relationship('Session')
    participants = relationship('Participant')

class Participant(Base):
    __tablename__="participants"
    id = Column(Integer, primary_key=True , nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    
    course = Column(Integer, ForeignKey("courses.id"), nullable=False)

    curves = relationship('Curve')
    keyMoments = relationship('KeyMoment')

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String, nullable=False)
    
    course = Column(Integer, ForeignKey("courses.id"), nullable=False)

    keyMoments = relationship('KeyMoment')
    curves = relationship('Curve')

class KeyMoment(Base):
    __tablename__="keymoments"

    id = Column(Integer, primary_key=True , nullable=False, autoincrement=True)
    xvalue = Column(Float,nullable=False)
    yvalue = Column(Float,nullable=False)
    what = Column(Text, nullable=True) # What happend
    when = Column(Text, nullable=True) # When did it happen
    thoughts = Column(Text, nullable=True) # What did you think
    feelings = Column(Text, nullable=True) # What did you feel
    actions = Column(Text, nullable=True) # What did you do
    consequences = Column(Text, nullable=True) # Where there any consequences

    session = Column(UUID, ForeignKey("sessions.id"), nullable=False)
    participant = Column(Integer, ForeignKey("participants.id"), nullable=True)
    curve = Column(Integer, ForeignKey("curves.id"), nullable=False)

class Curve(Base):
    __tablename__="curves"

    id = Column(Float, primary_key=True , nullable=False, autoincrement=True)
    data = Column(LargeBinary, nullable=False) # Pickled list of curve data

    session = Column(UUID, ForeignKey("sessions.id"), nullable=False)
    participant = Column(Integer, ForeignKey("participants.id"), nullable=True)
    
    keyMoments = relationship('KeyMoment')

    