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
    if 'username' in req.json and employeemng.find_user(req.json['username']):
        emp = employeemng.find_user(req.json['username'])
        role.emp_id = str(emp.emp_id)
        req.json['emp_id'] = emp.emp_id
        req.json.pop('username', None)
    else:
        return jsonify(message="Employee not found."), 404
    if 'perm_id' in req.json and Permission.query.filter_by(perm_id=req.json['perm_id']).one_or_none:
        role.perm_id = req.json['perm_id']
    else:
        return jsonify(message="Permission not found."), 404
    try:
        db.session.add(role)
        db.session.commit()
    except (TypeError, ValidationError) as err:
        return jsonify(message=list(eval(str(err)).values())[0][0]), 401
    except ValueError as err:
        return jsonify(message=err), 401
    return jsonify(message="Role has been created"), 201


# UPDATE
def update(req):
    if 'role_id' in req.json:
        role = Role.query.filter_by(req.json['role_id']).first()
        if role:
            if 'event_id' in req.json:
                if eventmng.exists(req.json['event_id']):
                    role.event_id = req.json['event_id']
                else:
                    return jsonify(message="Event not found."), 404
            if 'emp_id' in req.json:
                if employeemng.exists(req.json['emp_id']):
                    role.responsible_id = req.json['emp_id']
                else:
                    return jsonify(message="Employee not found."), 404
            if 'perm_id' in req.json:
                if Permission.query.filter_by(perm_id=req.json['perm_id']).one_or_none:
                    role.responsible_id = req.json['perm_id']
                else:
                    return jsonify(message="Permission not found."), 404
        try:
            role_schema.load(req.json)
            db.session.commit()
        except (TypeError, ValidationError) as err:
            return jsonify(message=list(eval(str(err)).values())[0][0]), 401
        except ValueError as err:
            return jsonify(message=err), 401
        return jsonify(message="Role has been updated"), 201
    else:
        return ""


# DELETE
def delete(role_id: int):
    role = Role.query.filter_by(role_id=role_id).first()
    if role:
        db.session.delete(role)
        db.session.commit()
        return jsonify(Message="Role has been deleted"), 202
    else:
        return jsonify(Message="An error happened, role not found"), 404


# #################################################################
# OTHER
# #################################################################

# returns a boolean by role_id if exists or not
def exists(emp_id: int, event_id: int, perm_id: int):
    role = Role.query.filter_by(emp_id=emp_id,
                                event_id=event_id,
                                perm_id=perm_id).first()
    if role:
        return True
    else:
        return False
