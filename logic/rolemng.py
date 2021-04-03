from flask import jsonify
from marshmallow import ValidationError
from logic import employeemng, eventmng
from schemas import RoleSchema
from models import Role, Permission
from app import db

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)


# #################################################################
# FOR ROLE REQUESTS
# #################################################################


# ADD - no bulk insert, only one record at once
def add(req):
    role = Role()
    if 'event_id' in req.json and eventmng.exists(req.json['event_id']):
        role.event_id = req.json['event_id']
    else:
        return jsonify(message="Event not found."), 404
    if 'emp_id' in req.json and employeemng.exists(req.json['emp_id']):
        role.responsible_id = req.json['emp_id']
    else:
        return jsonify(message="Employee not found."), 404
    if 'perm_id' in req.json and Permission.query.filter_by(perm_id=req.json['perm_id']).one_or_none:
        role.responsible_id = req.json['perm_id']
    else:
        return jsonify(message="Permission not found."), 404
    try:
        role_schema.load(req.json)
        db.session.add(role)
        db.session.commit()
    except (TypeError, ValidationError) as err:
        return jsonify(message=list(eval(str(err)).values())[0][0]), 401
    except ValueError as err:
        return jsonify(message=err), 401
    return jsonify(message="Role has been created"), 201


# UPDATE
def update(req):
    return jsonify(Message="Role not found"), 404


# DELETE
def delete(role_id: int):
    role = Role.query.filter_by(role_id=role_id).first()
    if role:
        db.session.delete(role)
        db.session.commit()
        return jsonify(Message="Role has been deleted"), 202
    else:
        return jsonify(Message="An error happened, role not found"), 404
