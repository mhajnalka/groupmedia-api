from flask import jsonify
from schemas import EmployeeSchema
from models import *
from app import db
from flask_jwt_extended import create_access_token
from sqlalchemy import or_

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


# !!!!!!!!!!!!!!!!!!!!!!!!!!!ezt majd át kell írni
def add(req):
    username = req.form['username']
    if Employee.query.filter_by(username=username).first():
        return jsonify(message="Username is already taken."), 404
    else:
        password = req.form['password']
        firstname = req.form['firstname']
        lastname = req.form['lastname']
        employee = Employee(username=username,
                            password=password,
                            firstname=firstname,
                            lastname=lastname)
        db.session.add(employee)
        db.session.commit()
        return jsonify(message="User created successfully"), 201


def login(req):
    if req.is_json:
        username = req.json['username']
        password = req.json['password']
    else:
        username = req.form['username']
        password = req.form['password']

    if Employee.query.filter_by(username=username, password=password).first():
        # match found, sending jwt token for logging in
        access_token = create_access_token(identity=username)
        return jsonify(message="Successful login", access_token=access_token), 200
    else:
        return jsonify(message="Invalid login data"), 401


def get_one(emp_id: str):
    employee = Employee.query.filter_by(emp_ID=emp_id).first()
    if employee:
        result = employee_schema.dump(employee)
        return jsonify(result)
    else:
        return jsonify(message="Employee not found"), 404


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


def get_all():
    user_list = Employee.query.all()
    result = employees_schema.dump(user_list)
    return jsonify(result), 200


def update(req):
    emp_id = int(req.form['emp_id'])
    employee = Employee.query.filter_by(emp_ID=emp_id).first()
    if employee:
        # ide kell egy rakat ellenőrzés
        employee.username = req.form['username']
        employee.password = req.form['password']
        employee.firstname = req.form['firstname']
        employee.lastname = req.form['lastname']
        employee.email = req.form['email']
        employee.phone = req.form['phone']
        employee.fax = req.form['fax']
        employee.address = req.form['address']
        employee.city = req.form['city']
        employee.region = req.form['region']
        employee.postcode = req.form['postcode']
        employee.country = req.form['country']
        db.session.commit()
        return jsonify(Message="Employee update successful"), 202
    else:
        return jsonify(Message="Employee not found"), 404


def delete(emp_id: int):
    employee = Employee.query.filter_by(emp_ID=emp_id).first
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return jsonify(Message="Employee deleted"), 202
    else:
        return jsonify(Message="Employee not found"), 404
