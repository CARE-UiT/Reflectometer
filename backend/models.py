from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"

    user_name = Column(String, nullable=False, primary_key=True, )
    email =  Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    salt = Column(String, nullable=False)