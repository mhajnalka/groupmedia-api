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
    lastlogin = Column(db.Date)
    itemversions = db.relationship('ItemVersion', backref='creator')
    responsibleof = db.relationship('EventProj', backref='responsible')
    deputyof = db.relationship('EventProj', backref='deputy')
    roles = db.relationship('Role', backref='emp')


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


class ItemMain(db.Model):
    __tablename__ = 'workiteminfo'
    itemmain_id = Column(db.Integer, primary_key=True)
    name = Column(db.String(25), unique=True)
    desc = Column(db.String(255))
    extension = Column(db.String(4))
    type = Column(db.String(4))
    versions = db.relationship('ItemVersion', backref='itemmain')


class Role(db.Model):  # N:
    role_ID = Column(db.Integer, primary_key=True)
    name = Column(db.String(25), unique=True)
    event_id = db.Column(db.Integer, db.ForeignKey('eventproj.event_id'))
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.emp_id'))
    perm_id = db.Column(db.Integer, db.ForeignKey('permission.perm_id'))


class Permission(db.Model):
    perm_id = Column(db.Integer, primary_key=True)
    name = Column(db.String(25), unique=True)
    roles = db.relationship('Role', backref='perm')


class ItemOfEvent(db.Model):
    ioe_id = Column(db.Integer, primary_key=True)
    event_id = Column(db.Integer)
    item_id = Column(db.Integer)


class EventProj(db.Model):
    event_id = Column(db.Integer, primary_key=True)
    name = Column(db.String(50), unique=True)
    desc = Column(db.String(255))
    publicity = Column(db.Boolean)
    state = Column(db.String(10))
    duedate = Column(db.Date)
    responsible_id = db.Column(db.Integer, db.ForeignKey('employee.emp_id'))
    deputy_id = db.Column(db.Integer, db.ForeignKey('employee.emp_id'))
    items = db.relationship('ItemVersion', backref='project')
    roles = db.relationship('Role', backref='event')
