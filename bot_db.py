from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(50), nullable=True)
    username = Column(String(100), nullable=True)
    tg_id = Column(Integer, unique=True, nullable=False)
    is_admin = Column(Boolean, default=False)
    registered = Column(DateTime, default=datetime.now())

    generated_images = relationship("Image", back_populates="user")
    # sent_messages = relationship("Sent_Message", back_populates="sent_message")

class Image(Base):
    __tablename__ = "generated_images"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="generated_images")
    size = Column(String(10))
    path = Column(String)


class Sent_Message(Base):
    __tablename__ = "sent_messages"

    id = Column(Integer, primary_key=True)
    sent_message = Column(String)
    tg_id = Column(Integer)
    # user_id = Column(Integer, ForeignKey("users.id"))
    # user = relationship("User", back_populates="sent_message")

engine = create_engine("sqlite:///db.sqlite3")
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

def create(instance):
    session.add(instance=instance)
    session.commit()

def delete(instance):
    session.delete(instance=instance)
    session.commit()


