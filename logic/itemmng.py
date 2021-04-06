from flask import jsonify
from marshmallow import ValidationError
from schemas import ItemMainSchema
from models import *
from app import db

item_schema = ItemMainSchema()
items_schema = ItemMainSchema(many=True)


# #################################################################
# FOR ITEM REQUESTS - not directly as in other *mng.py modules
# #################################################################

# ADD
def add(json):
    try:
        item = ItemMain()
        item.name = json['name']
        item.desc = json['desc'] if 'desc' in json else ""
        if 'extension' in json:
            item.extension = json['extension']
        if 'type' in json:
            item.extension = json['type']
        item_schema.load(json)
        return item
    except (TypeError, ValidationError) as err:
        return str(list(eval(str(err)).values())[0][0])
    except ValueError as err:
        return err
    except KeyError:
        return "Missing data"


# DELETE
# cross-reference should be handled here
# if there's only one single version, main info should be deleted as well
def delete(req):
    try:
        itemmain_id = req.json['itemmain_id']
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
