import json
import os
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float, Date
from sqlalchemy.orm import session, sessionmaker
from dotenv import load_dotenv
from datetime import date


employees = Table(
    'employees', MetaData,
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

def _insert_employee():
    pass

# return true if the employee exists in the database, else return false
def _get_employee_id(first: str, last: str):
    record = session\
        .query(employees)\
        .filter(employees.first_name.like(first), employees.last_name.like(last))\
        .first()

    return record.id if record != None else False
