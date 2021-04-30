import datetime
from flask import jsonify
from marshmallow import ValidationError
from logic import employeemng
from schemas import EventProjSchema
from models import EventProj, ItemVersion
from app import db
from sqlalchemy import or_

event_schema = EventProjSchema()
events_schema = EventProjSchema(many=True)

_statuses = ('PENDING', 'INPROGRESS', 'WAITING', 'FINISHED', 'CANCELLED')


# #################################################################
# FOR EVENT REQUESTS
# #################################################################


# ADD
def add(req):
    try:
        name = req.json['name']
    except KeyError as err:
        return jsonify(message="Event name cannot be undefined."), 401
    if not EventProj.query.filter_by(name=name).first():
        try:
            event = EventProj()
            event.name = name
            event.desc = req.json['desc'] if 'desc' in req.json else ""
            event.publicity = req.json['publicity'] if 'publicity' in req.json else 1
            event.state = req.json['state'] if 'state' in req.json else "PENDING"
            if event.state not in _statuses:
                return jsonify(message="Invalid status for an event."), 404
            event.duedate = datetime.datetime.strptime(req.json['duedate'], '%Y-%m-%d') if 'duedate' in req.json else ""
            if 'responsible_id' in req.json and employeemng.find_user(req.json['responsible_id']):
                emp = employeemng.find_user(req.json['responsible_id'])
                event.responsible_id = emp.emp_id
                req.json['responsible_id'] = emp.emp_id
            else:
                return jsonify(message="Responsible not found."), 404
            db.session.add(event)
            db.session.commit()
        except (TypeError, ValidationError) as err:
            return jsonify(message=list(eval(str(err)).values())[0][0]), 401
        except ValueError as err:
            return jsonify(message=err), 401
        except KeyError:
            return jsonify(message="Missing data"), 401
        return jsonify(message="Event created successfully"), 201
    else:
        return jsonify(message="Event name is already taken."), 404


# returns a single event by ID
def get_one(event_id: int):
    event = EventProj.query.filter_by(event_id=event_id).first()
    if event:
        result = events_schema.dump(event)
        return jsonify(result)
    else:
        return jsonify(message="Event not found"), 404


# returns a list of filtered events
def get_many(req):
    name = req.args.get('name')
    state = req.args.get('state')
    responsible_id = req.args.get('responsible_id')
    deputy_id = req.args.get('deputy_id')
    due_date = req.args.get('duedate')
    event_list = \
        EventProj.query.filter_by(or_(name=name,
                                      state=state,
                                      responsible_id=responsible_id,
                                      deputy_id=deputy_id,
                                      duedate=due_date))
    if event_list:
        result = events_schema.dump(event_list)
        return jsonify(result)
    else:
        return jsonify(Message="No employees found"), 404


# returns all the events
def get_all():
    event_list = EventProj.query.all()
    result = events_schema.dump(event_list)
    return jsonify(result), 200


# UPDATE
def update(req):
    event_id = int(req.json['event_id'])
    event = EventProj.query.filter_by(event_id=event_id).first()
    if event:
        try:
            event.desc = req.json['desc'] if 'desc' in req.json else event.desc
            event.publicity = req.json['publicity'] if 'publicity' in req.json else event.publicity
            event.state = req.json['state'] if 'state' in req.json else event.state
            if event.state not in _statuses:
                return jsonify(message="Invalid status for an event."), 404
            elif event.state == _statuses[4] and ItemVersion.query.filter_by(project_id=event_id,
                                                                             lockstate=True):
                return jsonify(message="Event cannot be closed, it has items that have not been validated yet."), 401
            event.duedate = req.json['duedate'] if 'duedate' in req.json else event.duedate
            if 'responsible_id' in req.json and employeemng.exists(req.json['responsible_id']):
                event.responsible_id = req.json['responsible_id']
            event_schema.load(req.json)
            db.session.commit()
        except (TypeError, ValidationError) as err:
            return jsonify(message=list(eval(str(err)).values())[0][0]), 401
        except ValueError as err:
            return jsonify(message=err), 401
        except KeyError:
            return jsonify(message="Missing data"), 401
        return jsonify(message="Event updated successfully"), 201
    else:
        return jsonify(Message="Event not found"), 404


# DELETED or CANCELLED (when not empty)
def delete(event_id: int):
    event = EventProj.query.filter_by(event_id=event_id).first()
    if event:
        if ItemVersion.query.filter_by(project_id=event_id).first:
            event.state = _statuses[4]
        else:
            db.session.delete(event)
        db.session.commit()
        return jsonify(Message="Event has beeen deleted"), 202
    else:
        return jsonify(Message="Event not found"), 404


# Sets event's state to FINISHED
def set_finished(event_id: int):
    event = EventProj.query.filter_by(event_id=event_id).first()
    if event:
        event.state = _statuses[3]
        db.session.commit()
        return jsonify(Message="Event state has been updated"), 201
    else:
        return jsonify(Message="Event not found"), 404

# #################################################################
# OTHER
# #################################################################


# seeking whether if there's an existing event with the given id
def exists(event_id: int):
    event = EventProj.query.filter_by(event_id=event_id).first()
    if event:
        return True
    else:
        return False


# seeking whether if the event with the given id is still modifiable
def is_wip(event_id: int):
    event = EventProj.query.filter_by(event_id=event_id).first()
    if event.state in [_statuses[1]]:
        return True
    else:
        return False
