from flask import jsonify
from schemas import ItemMainSchema
from models import *
from app import db
from sqlalchemy import or_

iteminfo_schema = ItemMainSchema()
iteminfos_schema = ItemMainSchema(many=True)

# ADD + DELETE:
# cross-reference should be handled here
