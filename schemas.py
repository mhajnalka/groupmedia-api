from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError, validates, validate
import re
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from models import Employee, ItemVersion, ItemMain, Permission, EventProj, Role

ma = Marshmallow()


class EmployeeSchema(ma.Schema):
    emp_id = fields.Integer()
    username = fields.String(validate=validate.Length(max=25))
    password = fields.String()
    firstname = fields.String(validate=validate.Length(max=50))
    lastname = fields.String(validate=validate.Length(max=50))
    email = fields.Email()
    phone = fields.String(validate=validate.Length(min=10, max=20))
    fax = fields.String(validate=validate.Length(min=8, max=20))
    address = fields.String(validate=validate.Length(max=50))
    city = fields.String(validate=validate.Length(max=50))
    region = fields.String(validate=validate.Length(max=50))
    postcode = fields.String(validate=validate.Length(equal=4))
    country = fields.String(validate=validate.Length(max=50))

    @validates('password')
    def validate_pw(self, pw):
        if len(pw) < 5:
            raise ValidationError("Password cannot be less than 5 characters")
        elif len(pw) > 25:
            raise ValidationError("Password cannot be bigger than 25")
        elif not any(c for c in pw if c.islower()) and not any(c for c in pw if c.isUpper()):
            raise ValidationError("Password must contain lower and upper case letters as well")
        elif not re.match("^[A-Za-z0-9_-]*$", pw):
            raise ValidationError("Password cannot contain any special characters")
        elif not any(c.isdigit() for c in pw) and not any(c.isletter() for c in pw):
            raise ValidationError("Password must contain numbers and digits as well")


class ItemVersionSchema(ma.Schema):
    item_id = fields.Integer()
    filename = fields.String(validate=validate.Length(max=50))
    version = fields.String(validate=validate.Length(max=50))
    lockstate = fields.Boolean()
    islastver = fields.Boolean()
    creadate = fields.Date('%Y-%m-%d')
    itemmain_id = fields.Integer()
    creator_id = fields.Integer()
    project_id = fields.Integer()


class ItemMainSchema(ma.Schema):
    itemmain_id = fields.Integer()
    name = fields.String(validate=validate.Length(max=25))
    desc = fields.String(validate=validate.Length(max=255))
    extension = fields.String(validate=validate.Length(max=4))
    type = fields.String(validate=validate.Length(max=4))

class RoleSchema(ma.Schema):
    role_id = fields.Integer()
    name = fields.String(validate=validate.Length(max=25))
    event_id = fields.Integer()
    emp_id = fields.Integer()
    perm_id = fields.Integer()


class PermissionSchema(ma.Schema):
    perm_ID = fields.Integer()
    name = fields.String(validate=validate.Length(max=25))


class EventProjSchema(ma.Schema):
    event_id = fields.Integer()
    name = fields.String(validate=validate.Length(max=50))
    desc = fields.String(validate=validate.Length(max=255))
    publicity = fields.Boolean()
    state = fields.String(validate=validate.Length(max=10))
    duedate = fields.Date('%Y-%m-%d')
    responsible_id = fields.Integer()
