from datetime import datetime
from flask import jsonify
from marshmallow import ValidationError
from logic.helper import fill_data, value_chk
from schemas import EmployeeSchema
from models import Employee
from app import db
from flask_jwt_extended import create_access_token
from sqlalchemy import or_

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


# ADD
def add(req):
    username = req.json['username']
    if Employee.query.filter_by(username=username).first():
        return jsonify(message="Username is already taken."), 404
    else:
        request_data = fill_data(classname=Employee, json=req.json)
        request_data['lastlogin'] = datetime.date.today()
        err_str = value_chk(request_data, {'emp_id': 'identifier',
                                           'username': 'username',
                                           'password': 'password',
                                           'firsname': 'first name',
                                           'lastname': 'last name',
                                           'email': 'e-mail'
        })
        try:
            employee = employee_schema.load(request_data)  # load validates the input
            if err_str:
                raise ValueError(err_str)
            db.session.add(employee)
            db.session.commit()
        except (TypeError, ValidationError) as err:
            return jsonify(message=list(eval(str(err)).values())[0][0]), 401
        except ValueError as err:
            return jsonify(message=err), 401

        return jsonify(message="User created successfully"), 201


# javítandó
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
def get_one(emp_id: str):
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
# ELŐSZÖR VALIDÁLUNK, HA A LOAD OK, AKKOR MEHET TOVÁBB
def update(req):
    emp_id = int(req.json['emp_id'])
    employee = Employee.query.filter_by(emp_id=emp_id).first()
    if employee:
        request_data = dict()
        request_data['emp_id'] = req.json['emp_id']
        request_data['username'] = req.json['username']
        request_data['password'] = req.json['password']
        request_data['firstname'] = req.json['firstname']
        request_data['lastname'] = req.json['lastname']
        request_data['email'] = req.json['email']
        request_data['phone'] = req.json['phone']
        request_data['fax'] = req.json['fax']
        request_data['address'] = req.json['address']
        request_data['city'] = req.json['city']
        request_data['region'] = req.json['region']
        request_data['postcode'] = req.json['postcode']
        request_data['country'] = req.json['country']
        try:
            employee = employee_schema.load(request_data)  # load validates the input
            db.session.commit()
        except ValidationError as err:
            return jsonify(Message=err), 401
        return jsonify(Message="Employee update successful"), 202
    else:
        return jsonify(Message="Employee not found"), 404


# DELETE
def delete(emp_id: int):
    employee = Employee.query.filter_by(emp_id=emp_id).first()
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return jsonify(Message="Employee deleted"), 202
    else:
        return jsonify(Message="Employee not found"), 404
