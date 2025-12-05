from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.config.db import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255))
    address = relationship("AddressModel", back_populates="user", uselist=False)


class AddressModel(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String(255))
    city = Column(String(255))
    zip = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("UserModel", back_populates="address")
