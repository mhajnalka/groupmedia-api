from flask import request, jsonify, Blueprint
from schemas import EmployeeSchema
from models import *
from app import db, jwt
from flask_jwt_extended import jwt_required, create_access_token
from sqlalchemy import or_
from logic import employeemng

routes_blueprint = Blueprint('routes', __name__)
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


@routes_blueprint.route('/elmeszagecibe')
def elmeszagecibe():
    return jsonify(message="anyad"), 200


# @routes_blueprint.route('/parameters')
# def parameters():
#    name = request.args.get('name')
#    age = int(request.args.get('age'))
#    return jsonify(message="Mindenhogyszar"), 401


# @routes_blueprint.route('/url_variables/<name>/<age>')
# @app.route('/url_variables/<string:name>/<int:age>')
# def url_variables(name: str, age: int):
#    return jsonify(message="Ezismindenhogyszarcsakszebben"), 401


@routes_blueprint.route('/add_employee', methods=['POST'])
# @jwt_required()
def add_employee():
    return employeemng.add(request)


@routes_blueprint.route('/login', methods=['POST'])
def login():
    return employeemng.login(request)


# get a single employee's data
@routes_blueprint.route('/get_employee/<string:emp_id>', methods=['GET'])
# @jwt_required()
def get_employee(emp_id: str):
    return employeemng.get_one(emp_id)


# get multiple employees' data
@routes_blueprint.route('/get_employees', methods=['GET'])
# @jwt_required()
def get_employees():
    return employeemng.get_many(request)


@routes_blueprint.route('/get_all_employees', methods=['GET'])
def get_all_employees():
    return employeemng.get_all()


# EZ LEHET NEM FOG KELLENI, DE:
# Adding Employee to database
# @routes_blueprint.route('/add_employee', methods=['POST'])
# @jwt_required()
# def get_employees(emp_id: str):
#    username = request.form['username']
#    employee = Employee.query.filter_by(username=username).first()
#    if employee:
#        return jsonify(Message="Employee already exists"), 404
#    else:
#        password = request.form['password']
#        employee = Employee(username=username,
#                            password=password)
#        db.session.add(employee)
#        db.session.commit()
#        return jsonify(Message="Employee added successfully "), 201


@routes_blueprint.route('/update_employee', methods=['PUT'])
def update_employee():
    return employeemng.update(request)


@routes_blueprint.route('/delete_employee/<int:emp_id>', methods=['PUT'])
# @jwt_required()
def delete_employee(emp_id: int):
    return employeemng.delete(emp_id)

#
# eventek.....
#
# itemek......
#
# fileok....
#
# other....
#
