import json
import os
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float, Date
from sqlalchemy.orm import sessionmaker
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
    Column ('time', Integer),
    Column('date', Date, primary_key=True),
    Column('msg', String)
)


def _insert_time():
    pass


def _insert_employee():
    pass

def _is_employee():
    pass
