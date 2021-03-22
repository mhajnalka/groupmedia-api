from flask import jsonify
from schemas import EventProjSchema
from models import EventProj
from app import db
from sqlalchemy import or_

event_schema = EventProjSchema()
events_schema = EventProjSchema(many=True)


# !!!!!!!!!!!!!!!!!!!!!!!!!!!ezt majd át kell írni
# ADD
def add(req):
    name = req.form['name']
    if EventProj.query.filter_by(name=name).first():
        return jsonify(message="Event name is already taken."), 401
    else:
        desc = req.form['desc']
        publicity = req.form['publicity']
        state = req.form['state']
        responsible_id = req.form['responsible_ID']
        deputy_id = req.form['deputy_ID']
        due_date = req.form['duedate']
        new_event = EventProj(name=name,
                              desc=desc,
                              publicity=publicity,
                              state=state,
                              responsible_ID=responsible_id,
                              deputy_ID=deputy_id,
                              duedate=due_date)
        db.session.add(new_event)
        db.session.commit()
        return jsonify(message="Event created successfully"), 201


# returns a single event by ID
def get_one(event_id: str):
    event = EventProj.query.filter_by(event_ID=event_id).first()
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
                                      responsible_ID=responsible_id,
                                      deputy_ID=deputy_id,
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
    event_id = int(req.form['event_id'])
    event = EventProj.query.filter_by(event_ID=event_id).first()
    if event:
        # ide kell egy rakat ellenőrzés
        event.name = req.form['name']
        event.desc = req.form['desc']
        event.publicity = req.form['publicity']
        event.state = req.form['state']
        event.responsible_ID = req.form['responsible_ID']
        event.deputy_ID = req.form['deputy_ID']
        event.duedate = req.form['duedate']
        db.session.commit()
        return jsonify(Message="Event update successful"), 202
    else:
        return jsonify(Message="Event not found"), 404


# DELETE
def delete(event_id: int):
    event = EventProj.query.filter_by(event_ID=event_id).first()
    if event:
        db.session.delete(event)
        db.session.commit()
        return jsonify(Message="Event deleted"), 202
    else:
        return jsonify(Message="Event not found"), 404
