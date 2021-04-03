from flask import jsonify
from marshmallow import ValidationError
from schemas import EmployeeSchema
from models import Employee
from app import db
from flask_jwt_extended import create_access_token
from sqlalchemy import or_

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


# #################################################################
# FOR EMPLOYEE REQUESTS
# #################################################################


# ADD
def add(req):
    try:
        username = req.json['username']
    except KeyError as err:
        return jsonify(message="Username cannot be undefined."), 401
    if not Employee.query.filter_by(username=username).first():
        try:
            employee = Employee()
            employee.username = req.json['username'] if 'username' in req.json else ""
            employee.password = req.json['password'] if 'password' in req.json else ""
            employee.firstname = req.json['firstname'] if 'firstname' in req.json else ""
            employee.lastname = req.json['lastname'] if 'lastname' in req.json else ""
            employee.email = req.json['email'] if 'email' in req.json else ""
            employee.phone = req.json['phone'] if 'phone' in req.json else ""
            employee.fax = req.json['fax'] if 'fax' in req.json else ""
            employee.address = req.json['address'] if 'address' in req.json else ""
            employee.city = req.json['city'] if 'city' in req.json else ""
            employee.region = req.json['region'] if 'region' in req.json else ""
            employee.postcode = req.json['postcode'] if 'postcode' in req.json else ""
            employee.country = req.json['country'] if 'country' in req.json else ""
            employee.create = req.json['create'] if 'create' in req.json else False
            employee_schema.load(req.json)
            db.session.add(employee)
            db.session.commit()
        except (TypeError, ValidationError) as err:
            return jsonify(message=list(eval(str(err)).values())[0][0]), 401
        except ValueError as err:
            return jsonify(message=err), 401
        except KeyError:
            return jsonify(message="Missing data"), 401
        return jsonify(message="Employee created successfully"), 201
    else:
        return jsonify(message="Username is already taken."), 404


# returns success message and access token for authorization
def login(req):
    username = req.json['username']
    password = req.json['password']

    if Employee.query.filter_by(username=username, password=password).first():
        # match found, sending jwt token for logging in
        access_token = create_access_token(identity=username)
        return jsonify(message="Successful login", access_token=access_token), 200
    else:
        return jsonify(message="Invalid login data"), 401


# returns a single employee by ID
def get_one(emp_id: int):
    employee = Employee.query.filter_by(emp_id=emp_id).first()
    if employee:
        result = employee_schema.dump(employee)
        return jsonify(result)
    else:
        return jsonify(message="Employee not found"), 404


# returns a list of filtered employees
def get_many(req):
    username = req.args.get('username')
    firstname = req.args.get('firstname')
    lastname = req.args.get('lastname')
    email = req.args.get('email')
    employee_list = \
        Employee.query.filter_by(or_(username=username, firstname=firstname, lastname=lastname, email=email))
    if employee_list:
        result = employees_schema.dump(employee_list)
        return jsonify(result)
    else:
        return jsonify(Message="No employees found"), 404


# returns all the employees
def get_all():
    user_list = Employee.query.all()
    result = employees_schema.dump(user_list)
    return jsonify(result), 200


# UPDATE
def update(req):
    try:
        emp_id = int(req.json['emp_id'])
    except KeyError as err:
        return jsonify(message="Username cannot be undefined."), 401
    employee = Employee.query.filter_by(emp_id=emp_id).first()
    if employee:
        try:
            employee.password = req.json['password'] if 'password' in req.json else employee.password
            employee.firstname = req.json['firstname'] if 'firstname' in req.json else employee.firstname
            employee.lastname = req.json['lastname'] if 'lastname' in req.json else employee.lastname
            employee.email = req.json['email'] if 'email' in req.json else employee.email
            employee.phone = req.json['phone'] if 'phone' in req.json else employee.phone
            employee.fax = req.json['fax'] if 'fax' in req.json else employee.fax
            employee.address = req.json['address'] if 'address' in req.json else employee.address
            employee.city = req.json['city'] if 'city' in req.json else employee.city
            employee.region = req.json['region'] if 'region' in req.json else employee.region
            employee.postcode = req.json['postcode'] if 'postcode' in req.json else employee.postcode
            employee.country = req.json['country'] if 'country' in req.json else employee.country
            employee_schema.load(req.json)
            db.session.commit()
        except (TypeError, ValidationError) as err:
            return jsonify(message=list(eval(str(err)).values())[0][0]), 401
        except ValueError as err:
            return jsonify(message=err), 401
        except KeyError:
            return jsonify(message="Missing data"), 401
        return jsonify(message="Employee has been successfully updated"), 201
    else:
        return jsonify(Message="Employee not found"), 404


# DELETE
def delete(emp_id: int):
    employee = Employee.query.filter_by(emp_id=emp_id).first()
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return jsonify(Message="Employee has been deleted"), 202
    else:
        return jsonify(Message="Employee not found"), 404


# #################################################################
# OTHER
# #################################################################

# returns a single employee by ID
def exists(emp_id: int):
    employee = Employee.query.filter_by(emp_id=emp_id).first()
    if employee:
        return True
    else:
        return False
