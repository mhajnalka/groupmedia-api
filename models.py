from sqlalchemy import Column, Integer, String, Boolean, Date
from app import db


class Employee(db.Model):
    __tablename__ = 'employee'
    emp_ID = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    fax = Column(String)
    address = Column(String)
    city = Column(String)
    region = Column(String)
    postcode = Column(String)
    country = Column(String)
    lastlogin = Column(Date)


class WorkItem(db.Model):
    __tablename__ = 'workitem'
    item_ID = Column(Integer, primary_key=True)
    emp_ID = Column(Integer)
    workiteminfo_ID = Column(Integer)
    filename = Column(String)
    version = Column(Integer)
    lockstate = Column(Boolean)
    islastver = Column(Boolean)
    creadate = Column(Date)


class WorkItemInfo(db.Model):
    __tablename__ = 'workiteminfo'
    workiteminfo_ID = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    desc = Column(String)
    extension = Column(String)
    type = Column(String)


class Role(db.Model):
    role_ID = Column(Integer, primary_key=True)
    event_ID = Column(Integer)
    emp_ID = Column(Integer)
    perm_ID = Column(Integer)


class Permission(db.Model):
    perm_ID = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class ItemOfEvent(db.Model):
    ioe_ID = Column(Integer, primary_key=True)
    event_ID = Column(Integer)
    item_ID = Column(Integer)


class EventProj(db.Model):
    event_ID = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    desc = Column(String)
    publicity = Column(Boolean)
    state = Column(String)
    responsible_ID = Column(String)
    deputy_ID = Column(String)
    duedate = Column(Date)
