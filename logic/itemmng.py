from flask import jsonify
from schemas import ItemMainSchema, ItemVersionSchema
from models import *
from app import db
from sqlalchemy import or_

iteminfo_schema = ItemMainSchema()
iteminfos_schema = ItemMainSchema(many=True)
itemversion_schema = ItemVersionSchema()
itemversions_schema = ItemMainSchema(many=True)


# ADD
# cross-reference should be handled here
# checks if we have already created the item, if so we only need a new version
def add(req):
    return jsonify(message="Something went wrong"), 404


# DELETE
# cross-reference should be handled here
# if there's only one single version, main info should be deleted as well
def delete(req):
    return jsonify(message="Something went wrong"), 404
