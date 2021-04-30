from flask import jsonify
from marshmallow import ValidationError

from logic import versionmng
from schemas import ItemMainSchema, ItemVersionSchema
from models import *
from app import db

item_schema = ItemMainSchema()
items_schema = ItemMainSchema(many=True)
versions_schema = ItemVersionSchema(many=True)


# #################################################################
# FOR ITEM REQUESTS - not directly as in other *mng.py modules
# #################################################################

# ADD
def add(form):
    try:
        item = ItemMain()
        item.name = form['name']
        item.desc = form['desc'] if 'desc' in form else ""
        if 'extension' in form:
            item.extension = form['extension']
        if 'type' in form:
            item.extension = form['type']
        db.session.add(item)
        db.session.commit()
        return item
    except (TypeError, ValidationError) as err:
        print('Error is: ' + str(list(eval(str(err)).values())[0][0]))
        return str(list(eval(str(err)).values())[0][0])
    except ValueError as err:
        print(err)
        return err
    except KeyError:
        print("MISS")
        return "Missing data"


# returns a single item by ID
def get_one(itemmain_id: int):
    item = ItemMain.query.filter_by(itemmain_id=itemmain_id).first()
    if item:
        result = item_schema.dump(item)
        return jsonify(result)
    else:
        return jsonify(message="Item not found"), 404


# returns all the events
def get_all():
    item_list = ItemMain.query.all()
    result = items_schema.dump(item_list)
    return jsonify(result), 200


# returns all item versions that belong to the same item instance
def get_all_version(name: str):
    item = ItemMain.query.filter_by(name=name).first()
    if item:
        versions = db.session.query(ItemMain.itemmain_id, ItemVersion.item_id, ItemVersion.filename,
                                    ItemVersion.version, ItemVersion.creadate, ItemVersion.lockstate).\
            join(ItemVersion).filter_by(itemmain_id=item.itemmain_id).all()
        print(versions)
        result = versions_schema.dump(versions)
        print(result)
        return jsonify(result), 200
    else:
        return jsonify(message="Item not found"), 404


# DELETE
# cross-reference should be handled here
# if there's only one single version, main info should be deleted as well
def delete(req):
    try:
        itemmain_id = req.form['itemmain_id']
    except KeyError as err:
        return jsonify(message="Main item cannot be undefined."), 401
    item = ItemMain.query.filter_by(itemmain_id=itemmain_id)
    if item:
        if any(v for v in item.ref_versions if v.lockstate is False):
            return jsonify(message="Main item cannot be deleted, there are validated versions in the system."), 401
        db.session.delete(item)
        db.session.commit()
        return jsonify(Message="Item has been deleted"), 202
    else:
        return jsonify(message="Item not found"), 404
