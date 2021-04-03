from datetime import date

from sqlalchemy import Column
from app import db


class Employee(db.Model):
    __tablename__ = 'employee'
    emp_id = Column(db.Integer, primary_key=True)
    username = Column(db.String(25), unique=True)
    password = Column(db.String(25))
    firstname = Column(db.String(50))
    lastname = Column(db.String(50))
    email = Column(db.String(50), unique=True)
    phone = Column(db.String(20))
    fax = Column(db.String(20))
    address = Column(db.String(50))
    city = Column(db.String(50))
    region = Column(db.String(50))
    postcode = Column(db.String(4))
    country = Column(db.String(50))
    create = Column(db.Boolean)
    ref_itemversions = db.relationship('ItemVersion', backref='creator')
    ref_responsibleof = db.relationship('EventProj', backref='responsible')
    ref_roles = db.relationship('Role', backref='emp')


class ItemMain(db.Model):
    __tablename__ = 'itemmain'
    itemmain_id = Column(db.Integer, primary_key=True)
    name = Column(db.String(25), unique=True)
    desc = Column(db.String(255))
    extension = Column(db.String(4))
    type = Column(db.String(4))
    ref_versions = db.relationship('ItemVersion', backref='itemmain')


class ItemVersion(db.Model):
    __tablename__ = 'workitem'
    item_id = Column(db.Integer, primary_key=True)
    filename = Column(db.String(25))
    version = Column(db.Integer)
    lockstate = Column(db.Boolean)
    islastver = Column(db.Boolean)
    creadate = Column(db.Date)
    itemmain_id = db.Column(db.Integer, db.ForeignKey('itemmain.itemmain_id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('employee.emp_id'))
    project_id = db.Column(db.Integer, db.ForeignKey('eventproj.event_id'))


class Role(db.Model):  # N:
    __tablename__ = 'role'
    role_id = Column(db.Integer, primary_key=True)
    name = Column(db.String(25), unique=True)
    event_id = db.Column(db.Integer, db.ForeignKey('eventproj.event_id'))
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.emp_id'))
    perm_id = db.Column(db.Integer, db.ForeignKey('permission.perm_id'))


class Permission(db.Model):
    __tablename__ = 'permission'
    perm_id = Column(db.Integer, primary_key=True)
    name = Column(db.String(25), unique=True)
    ref_roles = db.relationship('Role', backref='perm')


class EventProj(db.Model):
    __tablename__ = 'eventproj'
    event_id = Column(db.Integer, primary_key=True)
    name = Column(db.String(50), unique=True)
    desc = Column(db.String(255))
    publicity = Column(db.Boolean)
    state = Column(db.String(10))
    duedate = Column(db.Date)
    responsible_id = db.Column(db.Integer, db.ForeignKey('employee.emp_id'))
    ref_items = db.relationship('ItemVersion', backref='project')
    ref_roles = db.relationship('Role', backref='event')


class Company(db.Model):
    __tablename__ = 'company'
    comp_id = Column(db.Integer, primary_key=True)
    name = Column(db.String(25), unique=True)
    email = Column(db.String(50))
    phone = Column(db.String(20))
    fax = Column(db.String(20))
    web = Column(db.String(255))
    address = Column(db.String(50))
    city = Column(db.String(50))
    region = Column(db.String(50))
    postcode = Column(db.String(4))
    country = Column(db.String(50))
