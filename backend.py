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

    ## Not nessesary if Base used
    # def __init__(self, **kw: Any):
    #     # super().__init__(**kw)
    #     for key, value in kw.items():
    #         setattr(self, key, value)

    def __repr__(self):
        return f"({self.id}, {self.first_name}, {self.last_name}, {self.user_name})"
    

# Operation table
class Operation(Base):
    __tablename__ = "operation"
    id = mapped_column(Integer, primary_key=True)
    amount = mapped_column(Float, nullable=False, default=0)
    comment = mapped_column(String(150), nullable=False, default="")
    date_ = mapped_column(DateTime, default=datetime.today().replace(microsecond=0))
    user_id = mapped_column(Integer, ForeignKey("user.id"))
    type_id = mapped_column(Integer, ForeignKey("type.id"))
    category_id = mapped_column(Integer, ForeignKey("category.id"))
    user = relationship("User", back_populates="operation")
    type = relationship("Type", back_populates="operation")
    category = relationship("Category", back_populates="operation")

    def __repr__(self):
        return f"({self.id}, {self.amount}, {self.comment}, {self.date_})"


# Type table (earnings and spendings)
class Type(Base):
    __tablename__ = "type"
    id = mapped_column(Integer, primary_key=True)
    operation_type = mapped_column(String(20), default="") # earnings and spendings
    operation = relationship("Operation", back_populates="type")
    category = relationship("Category", back_populates="type")

    def __repr__(self):
        return f"({self.id}, {self.operation_type})"

# Category table (taxes, grocery store spendings, fuel etc.)
class Category(Base):
    __tablename__ = "category"
    id = mapped_column(Integer, primary_key=True)
    operation_category = mapped_column(String(50), default="")
    type_id = mapped_column(Integer, ForeignKey("type.id"))
    type = relationship("Type", back_populates="category")
    operation = relationship("Operation", back_populates="category")

    def __repr__(self):
        return f"({self.id}, {self.operation_category})"


Base.metadata.create_all(engine)



###### Actions with db tables


# def populate_type_db_table(session):
#     earnings = Type(operation_type="Earnings")
#     expenses = Type(operation_type="Expenses")
#     session.add(earnings)
#     session.add(expenses)
#     session.commit()


def query_user(session):
    users = session.query(User).all()
    users_list = [
                [item.id, item.first_name, item.last_name, item.user_name]
                for item in users
            ]
    return users_list

def create_user(f_name, l_name, u_name):
    customer = User(first_name=f_name, last_name=l_name, user_name=u_name)
    session.add(customer)
    session.commit()

def delete_user(session, delete_id):
    try:
        count_on_delete = session.query(Operation).filter(Operation.user_id == delete_id).count()
        for item in range(count_on_delete):
            item = session.query(Operation).filter(Operation.user_id == delete_id).first()
            session.delete(item)
        #session.delete(user_on_delete)
        user_on_delete = session.query(User).filter(User.id == delete_id).first()
        session.delete(user_on_delete)
        session.commit()
    except Exception as e:
        print(f"Error: {e}")


def select_from_user_list_table(session, row_value):
    items = session.query(User).all()
    items_list = [
                [item.id, item.first_name, item.last_name, item.user_name]
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

def query_user_items(session, user_id_n):
    items = session.query(Operation, Type, Category).filter(Operation.type_id == Type.id).filter(Operation.category_id == Category.id).filter_by(user_id=user_id_n)
    items_list = [
                [operation.id, type.operation_type, operation.amount, category.operation_category, operation.comment, operation.date_]
                for operation, type, category in items
            ]
    return items_list

def query_all_items(session):
    items = session.query(User, Operation, Type, Category)\
        .filter(User.id == Operation.user_id).filter(Operation.type_id == Type.id).filter(Operation.category_id == Category.id).all()
    items_list = [
                [operation.id, user.user_name, type.operation_type, operation.amount, category.operation_category, operation.comment, operation.date_]
                for user, operation, type, category in items
            ]
    return items_list

def edit_user(id, f_name, l_name, u_name):
    try:
        editable_user = session.get(User, id)
    except Exception as e:
        print(f"error: {e}")
    else:
        editable_user.first_name = f_name
        editable_user.last_name = l_name
        editable_user.user_name = u_name
    session.commit()


def populate_earnings_category_combo():
    result = session.query(Category.id, Category.operation_category)\
                .join(Type)\
                .filter(Type.operation_type == "earnings")\
                .all()
    return result

def populate_expenses_category_combo():
    result = session.query(Category.id, Category.operation_category)\
                .join(Type)\
                .filter(Type.operation_type == "expenses")\
                .all()
    return result

def insert_earnings_record(saved_user_id, earnings_type_id, earnings_amount, earnings_category_id, earnings_comment):
    operation = Operation(amount=earnings_amount, comment=earnings_comment, user_id=saved_user_id, type_id=earnings_type_id, category_id=earnings_category_id)
    session.add(operation)
    session.commit()

def insert_spendings_record(saved_user_id, spendings_type_id, spendings_amount, spendings_category_id, spendings_comment):
    operation = Operation(amount=spendings_amount, comment=spendings_comment, user_id=saved_user_id, type_id=spendings_type_id, category_id=spendings_category_id)
    session.add(operation)
    session.commit()

def delete_item(delete_id):
    try:
        item_on_delete = session.query(Operation).filter(Operation.id == delete_id).first()
        session.delete(item_on_delete)
        session.commit()
    except Exception as e:
        print(f"Error: {e}")

# def insert_new_record(type_n, amount_n, category_n, comment_n, user_id_n, type_id_n, category_id_n): # get type.id , get category.id
#     type = Type(operation_type=type_n) # no need
#     category = Category(operation_category=category_n, type_id=type_id_n) # no need
#     operation = Operation(amount=amount_n, comment=comment_n, user_id=user_id_n, type_id=type_id_n, category_id=category_id_n)
#     session.add_all([operation, type, category])
#     session.commit()
