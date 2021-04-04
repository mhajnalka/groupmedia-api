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


# UPDATE
def update(req):
    return ""


# DELETE
# cross-reference should be handled here
# if there's only one single version, main info should be deleted as well
def delete(req):
    return jsonify(message="Something went wrong"), 404
