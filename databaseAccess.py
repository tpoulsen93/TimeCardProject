import json
import os
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float, Date
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy import create_engine, insert
from dotenv import load_dotenv
from datetime import date


engine = create_engine('sqlite:///database.db')

meta = MetaData()


employees = Table(
    'employees', meta, 
    Column('id', Integer, autoincrement=True, unique=True, primary_key=True),
    Column('first_name', String),
    Column('last_name', String),
    Column('wage', Float),
    Column('phone_number', String, unique=True),
    Column('email', String)
)

payroll = Table(
    'payroll', meta,
    Column('id', ForeignKey('employees.id')),
    Column('time', Float),
    Column('draw', Float),
    Column('date', Date, primary_key=True),
    Column('msg', String)
)

meta.create_all(engine)


def insert_time(id, time, msg):
    stmt = insert(payroll).values(id=id, time=time, date=date.today(), msg=msg)

    with engine.connect() as conn:
        conn.execute(stmt)


# return true if the employee exists in the database, else return false
def get_employee_id(first: str, last: str):
    record = session\
        .query(employees)\
        .filter(employees.first_name.like(first), employees.last_name.like(last))\
        .first()

    return record.id if record != None else False
    


def insert_employee(first_name=None, last_name=None, wage=None, phone_number=None, email=None):
    stmt = insert(employees).values(first_name=first_name, last_name=last_name, wage=wage, \
                                    phone_number=phone_number, email=email)

    with engine.connect() as conn:
        conn.execute(stmt)


if __name__ == "__main__":
    # insert_employee(first_name="Taylor", last_name="Poulsen", wage="20.00",  \
    #                 phone_number="432-276-1331", email="DanielMBogden@gmail.com")
    # print("Successfull")

    Session = sessionmaker(bind = engine)
    session = Session()
    members = session.query(employees).all()

    with Session() as session:
        t = session.query(employees).filter(employees.first_name=="Taylor").all()
        print(t)
    
