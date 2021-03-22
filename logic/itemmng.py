from flask import jsonify
from schemas import WorkItemSchema
from models import *
from app import db
from flask_jwt_extended import create_access_token
from sqlalchemy import or_

item_schema = WorkItemSchema()
items_schema = WorkItemSchema(many=True)

# cross-reference should be handled here
