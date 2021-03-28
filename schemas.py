from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError, validates, validate
import re

ma = Marshmallow()

"""
class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('emp_ID', 'username', 'password', 'firstname', 'lastname', 'email', 'phone',
                  'fax', 'address', 'city', 'region', 'postcode', 'country', 'lastlogin')



def validate_length(length, param_name, max_length, min_length):
    if length > max_length:
        raise ValidationError(f"{param_name} cannot be bigger than {max_length}")
    elif length < min_length:
        raise ValidationError(f"{param_name} cannot be less than {min_length}")
        

class ItemVersionSchema(ma.Schema):
    class Meta:
        fields = ('item_ID', 'emp_ID', 'workiteminfo_ID', 'filename', 'version', 'lockstate',
                  'islastver', 'creadate')
"""


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
    lastlogin = fields.Date('YYYY-MM-dd')

    @validates('password')
    def validate_pw(self, pw):
        if len(pw) < 5:
            raise ValidationError("Password cannot be less than 5")
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
    creadate = fields.Date()
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
    duedate = fields.Date()
    responsible_id = fields.Integer()
    deputy_id = fields.Integer()


"""

class ItemMainSchema(ma.Schema):
    class Meta:
        fields = ('workiteminfo_ID', 'name', 'desc', 'extension', 'type')


class RoleSchema(ma.Schema):
    class Meta:
        fields = ('role_ID', 'event_ID', 'emp_ID', 'perm_ID')


class PermissionSchema(ma.Schema):
    class Meta:
        fields = ('perm_ID', 'name')


class EventProjSchema(ma.Schema):
    class Meta:
        fields = ('event_ID', 'name', 'desc', 'publicity', 'state', 'responsible_ID',
                  'deputy_ID', 'duedate')
"""
