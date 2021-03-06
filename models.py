from sqlalchemy import Column
from app import db


class Employee(db.Model):
    __tablename__ = 'employee'
    emp_id = Column(db.Integer, primary_key=True)
    username = Column(db.String(25), unique=True)
    password = Column(db.String(25), nullable=False)
    firstname = Column(db.String(50), nullable=False)
    lastname = Column(db.String(50), nullable=False)
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

    # will return the string representation of an employee instance
    def __repr__(self):
        return f'''
                Username            : {self.username}
                Name                : {self.firstname} {self.lastname}
                Email               : {self.email}
                Phone               : {self.phone}
                '''


class ItemMain(db.Model):
    __tablename__ = 'itemmain'
    itemmain_id = Column(db.Integer, primary_key=True)
    name = Column(db.String(25), unique=True)
    desc = Column(db.String(255))
    extension = Column(db.String(4))
    type = Column(db.String(4))
    ref_versions = db.relationship('ItemVersion', backref='itemmain')

    # will return the string representation of a main item instance
    def __repr__(self):
        return f'''
                Name                : {self.name}
                Description         : {self.desc} 
                Extension           : {self.extension}
                Type                : {self.type}
                '''


class ItemVersion(db.Model):
    __tablename__ = 'workitem'
    item_id = Column(db.Integer, primary_key=True)
    filename = Column(db.String(25), nullable=False)
    version = Column(db.Integer, nullable=False)
    desc = Column(db.String(255))
    lockstate = Column(db.Boolean)
    rejected = Column(db.Boolean)
    islastver = Column(db.Boolean)
    creadate = Column(db.Date)
    itemmain_id = db.Column(db.Integer, db.ForeignKey('itemmain.itemmain_id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('employee.emp_id'))
    project_id = db.Column(db.Integer, db.ForeignKey('eventproj.event_id'))

    # will return the string representation of a version instance
    def __repr__(self):
        return f'''
                Filename            : {self.filename}
                Version             : {self.version}.0
                Description         : {self.desc}
                Date of creation    : {self.creadate}
                '''


class Role(db.Model):  # N:
    __tablename__ = 'role'
    role_id = Column(db.Integer, primary_key=True)
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
    state = Column(db.String(10), nullable=False)
    duedate = Column(db.Date)
    responsible_id = db.Column(db.Integer, db.ForeignKey('employee.emp_id'))
    ref_items = db.relationship('ItemVersion', backref='project')
    ref_roles = db.relationship('Role', backref='event')

    # will return the string representation of an event instance
    def __repr__(self):
        return f'''
                Identifier of event : {self.event_id}
                Name                : {self.name}
                Description         : {self.desc}
                Publicity           : {self.publicity}
                State               : {self.state}
                Due date            : {self.duedate}
                '''


class Company(db.Model):
    __tablename__ = 'company'
    comp_id = Column(db.Integer, primary_key=True)
    name = Column(db.String(255), unique=True)
    email = Column(db.String(50))
    phone = Column(db.String(20))
    fax = Column(db.String(20))
    web = Column(db.String(255))
    address = Column(db.String(50))
    city = Column(db.String(50))
    region = Column(db.String(50))
    postcode = Column(db.String(4))
    country = Column(db.String(50))

    # will return the string representation of a company instance
    def __repr__(self):
        return f'''
                _______________________________________________________________
                _______________________________________________________________
                {self.name}
                Phone         : {self.phone}
                Fax           : {self.fax}
                Web           : {self.web}
                Address       : {self.postcode} {self.city}, {self.address}
                '''
