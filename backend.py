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

## Creating tables

# User table
class User(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    first_name = mapped_column(String(50), nullable=False)
    last_name = mapped_column(String(50), nullable=False)
    user_name = mapped_column(String(50), nullable=False)
    operation = relationship("Operation", back_populates="user")

    ## sito nereikia kai yra Base
    # def __init__(self, **kw: Any):
    #     # super().__init__(**kw)
    #     for key, value in kw.items():
    #         setattr(self, key, value)

    def __repr__(self):
        return f"({self.id}, {self.first_name}, {self.last_name}, {self.user_name})"
    

#Operation table
class Operation(Base):
    __tablename__ = "operation"
    id = mapped_column(Integer, primary_key=True)
    amount = mapped_column(Integer, nullable=False, default=0)
    comment = mapped_column(String(150), nullable=False, default="")
    date_ = mapped_column(DateTime, default=datetime.today().replace(microsecond=0))
    user_id = mapped_column(Integer, ForeignKey("user.id"))
    type_id = mapped_column(Integer, ForeignKey("type.id"))
    purpose_id = mapped_column(Integer, ForeignKey("purpose.id"))
    user = relationship("User", back_populates="operation")
    type = relationship("Type", back_populates="operation")
    purpose = relationship("Purpose", back_populates="operation")

    def __repr__(self):
        return f"({self.id}, {self.amount}, {self.comment}, {self.date_})"


# Type table
class Type(Base):
    __tablename__ = "type"
    id = mapped_column(Integer, primary_key=True)
    operation_type = mapped_column(String(20), default="") # earnings or spendings
    operation = relationship("Operation", back_populates="type")
    purpose = relationship("Purpose", back_populates="type")

# Purpose table
class Purpose(Base):
    __tablename__ = "purpose"
    id = mapped_column(Integer, primary_key=True)
    operation_purpose = mapped_column(String(50), default="")
    type_id = mapped_column(Integer, ForeignKey("type.id"))
    type = relationship("Type", back_populates="purpose")
    operation = relationship("Operation", back_populates="purpose")


Base.metadata.create_all(engine)



###### Actions with db tables

def query_user(session):
    users = session.query(User).all()
    users_list = [
                [item.id, item.first_name, item.last_name]
                for item in users
            ]
    return users_list

def create_user(f_name, l_name):
    customer = User(first_name=f_name, last_name=l_name)
    session.add(customer)
    session.commit()

def delete_user(session, delete_id):
    try:
        user_on_delete = session.get(User, int(delete_id))
        session.delete(user_on_delete)
        session.commit()
    except Exception as e:
        print(f"Error: {e}")

def select_from_user_list_table(session, row_value):
    items = session.query(User).all()
    items_list = [
                [item.id, item.first_name, item.last_name]
                for item in items
            ]
    return items_list[row_value]

def select_from_user_listings_table(session, row_value, user_id_n):
    items = session.query(Operation).filter_by(user_id=user_id_n)
    items_list = [
                [item.id, item.amount, item.comment, item.date_]
                for item in items
            ]
    return items_list[row_value]

def insert_new_record(amount_n, comment_n, user_id_n):
    items = Operation(amount=amount_n, comment=comment_n, user_id=user_id_n)
    session.add(items)
    session.commit()

def query_user_items(session, user_id_n):
    items = session.query(Operation).filter_by(user_id=user_id_n)
    items_list = [
                [item.id, item.amount, item.comment, item.date_]
                for item in items
            ]
    return items_list

def query_all_items(session):
    items = session.query(Operation).join(User).all()
    items_list = [
                [item.id, item.user.first_name, item.amount, item.comment, item.date_]
                for item in items
            ]
    return items_list