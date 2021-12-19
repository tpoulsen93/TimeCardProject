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
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('first_name', String),
    Column('last_name', String),
    Column('wage', Float),
    Column('phone_number', String),
    Column('email', String)
)

payroll = Table(
    'payroll', MetaData,
    Column('id', ForeignKey(employees.id)),
    Column('time', Integer),
    Column('date', Date, primary_key=True),
    Column('msg', String)
)


def _insert_time():
    pass


# return true if the employee exists in the database, else return false
def _get_employee_id(first: str, last: str):
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
        
    print("executed")

def _is_employee():
    pass


if __name__ == "__main__":
    # insert_employee(first_name="Taylor", last_name="Poulsen", wage="20.00",  \
    #                 phone_number="432-276-1331", email="DanielMBogden@gmail.com")
    # print("Successfull")

    Session = sessionmaker(bind = engine)
    session = Session()
    members = session.query(employees).all()

    # for employee in members:
    #     # print(f"{employee.first_name}, {employee.last_name}")
    #     print(employee)

    with Session() as session:
        t = session.query(employees).filter(employees.first_name=="Taylor").all()
        print(t)
    
