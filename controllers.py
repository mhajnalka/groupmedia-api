from flask import request, jsonify, Blueprint
from app import db, jwt
from flask_jwt_extended import jwt_required, create_access_token
from logic import employeemng

routes_blueprint = Blueprint('routes', __name__)


@routes_blueprint.route('/api_test')
def api_test():
    return jsonify(message="TEST RESPONSE"), 200


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
# @jwt_required()
def get_all_employees():
    return employeemng.get_all()


@routes_blueprint.route('/update_employee', methods=['PUT'])
# @jwt_required()
def update_employee():
    return employeemng.update(request)


@routes_blueprint.route('/delete_employee/<int:emp_id>', methods=['PUT'])
# @jwt_required()
def delete_employee(emp_id: int):
    return employeemng.delete(emp_id)
