from flask import request, jsonify, Blueprint

from app import db, jwt
from flask_jwt_extended import jwt_required, create_access_token
from logic import employeemng, eventmng, versionmng, itemmng, constmng

routes_blueprint = Blueprint('routes', __name__)


@routes_blueprint.route('/api_test')
def api_test():
    return jsonify(message="TEST RESPONSE"), 200


# #################################################################
# EMPLOYEE REQUESTS
# #################################################################


@routes_blueprint.route('/add_employee', methods=['POST'])
# @jwt_required()
def add_employee():
    return employeemng.add(request)


@routes_blueprint.route('/login', methods=['POST'])
def login():
    return employeemng.login(request)


@routes_blueprint.route('/get_employee/<int:emp_id>', methods=['GET'])
# @jwt_required()
def get_employee(emp_id: int):
    return employeemng.get_one(emp_id)


@routes_blueprint.route('/get_employees', defaults={'username': ''})
@routes_blueprint.route('/get_employees/<username>', methods=['GET'])
# @jwt_required()
def get_employees(username: str):
    return employeemng.get_many(username, request)


@routes_blueprint.route('/get_all_employees', methods=['GET'])
@jwt_required()
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


# #################################################################
# EVENT REQUESTS
# #################################################################


@routes_blueprint.route('/add_event', methods=['POST'])
# @jwt_required()
def add_event():
    return eventmng.add(request)


@routes_blueprint.route('/get_event/<int:event_id>', methods=['GET'])
# @jwt_required()
def get_event(event_id: int):
    return eventmng.get_one(event_id)


@routes_blueprint.route('/get_events', methods=['GET'])
# @jwt_required()
def get_events():
    return eventmng.get_many(request)


@routes_blueprint.route('/get_all_events', methods=['GET'])
# @jwt_required()
def get_all_events():
    return eventmng.get_all()


@routes_blueprint.route('/update_event', methods=['PUT'])
# @jwt_required()
def update_event():
    return eventmng.update(request)


@routes_blueprint.route('/delete_event/<int:event_id>', methods=['PUT'])
# @jwt_required()
def delete_event(event_id: int):
    return eventmng.delete(event_id)


# #################################################################
# VERSION REQUESTS
# #################################################################

@routes_blueprint.route('/add_version', methods=['POST'])
# @jwt_required()
def add_version():
    return versionmng.add(request)


@routes_blueprint.route('/process_file', methods=['POST'])
# @jwt_required()
def process_file():
    return versionmng.process_file(request)


@routes_blueprint.route('/update_version', methods=['PUT'])
# @jwt_required()
def update_version():
    return versionmng.update(request)


@routes_blueprint.route('/show_file', methods=['GET'])
# @jwt_required()
def show_file():
    return versionmng.show_file(request)


@routes_blueprint.route('/validate', methods=['PUT'])
# @jwt_required()
def validate_version():
    return versionmng.validate(request, True)


@routes_blueprint.route('/reject', methods=['PUT'])
# @jwt_required()
def reject_version():
    return versionmng.validate(request, False)


@routes_blueprint.route('/delete_version/<int:item_id>', methods=['PUT'])
# @jwt_required()
def delete_version(item_id: int):
    return versionmng.delete(item_id)


# #################################################################
# ITEM REQUESTS
# #################################################################

@routes_blueprint.route('/get_item/<int:itemmain_id>', methods=['GET'])
# @jwt_required()
def get_item(itemmain_id: int):
    return itemmng.get_one(itemmain_id)


@routes_blueprint.route('/get_all_item', methods=['GET'])
# @jwt_required()
def get_all_item():
    return itemmng.get_all()


@routes_blueprint.route('/get_all_version/<int:itemmain_id>', methods=['GET'])
# @jwt_required()
def get_all_version(itemmain_id: int):
    return itemmng.get_all_version(itemmain_id)


# #################################################################
# OTHER KIND OF REQUESTS
# #################################################################

@routes_blueprint.route('/get_contact', methods=['GET'])
@jwt_required()
def get_contact():
    return constmng.get_one(1)
