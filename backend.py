# libraries
from typing import Any
from sqlalchemy import create_engine, Integer, String, Float, DateTime, Table, Column, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Session, relationship
from datetime import datetime

# declarative base
class Base(DeclarativeBase):
    pass

# creating db and declaring session
engine = create_engine('sqlite:///home_accounting.db')
session = sessionmaker(bind=engine)()

# Creating tables

class User_(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    first_name = mapped_column(String(50), nullable=False)
    last_name = mapped_column(String(50), nullable=False)

    def __init__(self, **kw: Any):
        # super().__init__(**kw)
        for key, value in kw.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"({self.id}, {self.first_name}, {self.last_name})"
    


Base.metadata.create_all(engine)

# class Operation_(Base):
#     __tablename__ = "user"
#     id = mapped_column(Integer, primary_key=True)
#     first_name = mapped_column("first_name", String(50))
#     last_name = mapped_column("last_name", String(50))

#     def __repr__(self):
#         return f"({self.id}, {self.first_name}, {self.last_name})"

###### Actions with db tables

def query_user(session):
    users = session.query(User_).all()
    users_list = [
                [item.id, item.first_name, item.last_name]
                for item in users
            ]
    return users_list

def create_user(f_name, l_name):
    customer = User_(first_name=f_name, last_name=l_name)
    session.add(customer)
    session.commit()

def delete_user(session, delete_id):
    try:
        user_on_delete = session.get(User_, int(delete_id))
        session.delete(user_on_delete)
        session.commit()
    except Exception as e:
        print(f"Error: {e}")

def select_user_list(session, row_value):
    users = session.query(User_).all()
    users_list = [
                [item.id, item.first_name, item.last_name]
                for item in users
            ]
    return users_list[row_value]

