from flask import jsonify
from schemas import EmployeeSchema
from models import Employee
from app import db
from flask_jwt_extended import create_access_token
from sqlalchemy import or_

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


# !!!!!!!!!!!!!!!!!!!!!!!!!!!ezt majd át kell írni
# ADD
def add(req):
    username = req.json['username']
    if Employee.query.filter_by(username=username).first():
        return jsonify(message="Username is already taken."), 404
    else:
        password = req.json['password']
        firstname = req.json['firstname']
        lastname = req.json['lastname']
        employee = Employee(username=username,
                            password=password,
                            firstname=firstname,
                            lastname=lastname)
        db.session.add(employee)
        db.session.commit()
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
    employee = Employee.query.filter_by(emp_ID=emp_id).first()
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
    emp_id = int(req.json['emp_id'])
    employee = Employee.query.filter_by(emp_ID=emp_id).first()
    if employee:
        # ide kell egy rakat ellenőrzés
        employee.username = req.json['username']
        employee.password = req.json['password']
        employee.firstname = req.json['firstname']
        employee.lastname = req.json['lastname']
        employee.email = req.json['email']
        employee.phone = req.json['phone']
        employee.fax = req.json['fax']
        employee.address = req.json['address']
        employee.city = req.json['city']
        employee.region = req.json['region']
        employee.postcode = req.json['postcode']
        employee.country = req.json['country']
        db.session.commit()
        return jsonify(Message="Employee update successful"), 202
    else:
        return jsonify(Message="Employee not found"), 404


# DELETE
def delete(emp_id: int):
    employee = Employee.query.filter_by(emp_ID=emp_id).first()
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return jsonify(Message="Employee deleted"), 202
    else:
        return jsonify(Message="Employee not found"), 404
