import datetime
from flask import jsonify
from marshmallow import ValidationError
from logic import employeemng, eventmng, itemmng, rolemng
from schemas import ItemMainSchema, ItemVersionSchema
from models import *
from app import db

version_schema = ItemVersionSchema()
versions_schema = ItemMainSchema(many=True)


# #################################################################
# FOR ITEM REQUESTS
# #################################################################

# ADD
# Identified by name, so can be handled together with the main object
def add(req):
    if 'name' in req.json:
        name = req.json['name']
        item = ItemMain.query.filter_by(name=name).first()
        version = ItemVersion()
        version.desc = req.json['desc'] if 'desc' in req.json else ""
        version.lockstate = 1
        version.rejected = 0
        version.islastver = 0
        version.creadate = \
            datetime.datetime.strptime(req.json['creadate'], '%d-%m-%Y') if 'creadate' in req.json else ""
        # checking project and it's state, which must be modifiable
        if 'project_id' in req.json and eventmng.exists(req.json['project_id']):
            if eventmng.is_wip(req.json['project_id']):
                version.project_id = req.json['project_id']
            else:
                return jsonify(message="An error happened: event with wrong state"), 404
        else:
            return jsonify(message="An error happened, event not found."), 404
        # checking creator
        if 'creator_id' in req.json and employeemng.exists(req.json['creator_id']):
            version.creator_id = req.json['creator_id']
        else:
            return jsonify(message="An error happened, creator not found."), 404
        if not rolemng.exists(version.creator_id, version.project_id, 2):
            return jsonify(message="Role not found, permission denied."), 404
        # item is true when it exists with the param of name
        if item:
            try:
                # version only
                version.filename = req.json['filename'] if 'filename' in req.json else ""
                # checking main item's connected last version, if not locked, then it has to be updated as well
                # we have to raise the major part of the version number, minor part is not handled
                prev_version = ItemVersion.query.filter_by(itemmain_id=item.itemmain_id,
                                                           islastver=True).first()
                if prev_version.lockstate:
                    return jsonify(message="Item cannot be modified when previous version is locked.")
                version.version = prev_version.version + 1
                # +ATTACHMENT, IN AN OTHER METHOD
                # needs to be stored (maybe even renamed)

                version_schema.load(version)
                db.session.add(version)
                db.session.commit()
            except (TypeError, ValidationError) as err:
                return jsonify(message=list(eval(str(err)).values())[0][0]), 401
            except ValueError as err:
                return jsonify(message=err), 401
            except KeyError as err:
                return jsonify(message="Missing data: " + err.args[0]), 401
        else:
            # 1.0 version - new main item
            version.version = 1
            # create main item
            new_item = itemmng.add(req.json)
            if isinstance(new_item, str):
                return jsonify(message=new_item), 401
            version.itemmain_id = new_item.itemmain_id
            try:
                version.filename = req.json['filename'] if 'filename' in req.json else ""

                # +ATTACHMENT, IN AN OTHER METHOD
                # needs to be stored (maybe even renamed)

                version_schema.load(version)
                db.session.add(new_item)
                db.session.add(version)
                db.session.commit()
            except (TypeError, ValidationError) as err:
                return jsonify(message=list(eval(str(err)).values())[0][0]), 401
            except ValueError as err:
                return jsonify(message=err), 401
            except KeyError as err:
                return jsonify(message="Missing data: " + err.args[0]), 401
    else:
        return jsonify(message="Name cannot be empty"), 404
    return jsonify(message="Item has been created"), 201


# handles received files separately from administration
# in order to be able to manage files, file name has to be the same as defined in the add method
def process_file(req):
    return ""


# UPDATE
def update(req):
    if 'item_id' and 'desc' in req.json:
        version = ItemVersion.query.filter_by(item_id=req.json['item_id']).first()
        version.desc = req.json['item_id']
        try:
            version_schema.load(version)
            db.session.commit()
        except (TypeError, ValidationError) as err:
            return jsonify(message=list(eval(str(err)).values())[0][0]), 401
        except ValueError as err:
            return jsonify(message=err), 401
        except KeyError as err:
            return jsonify(message="Missing data: " + err.args[0]), 401
    else:
        return jsonify(message="Wrong parameters given."), 401
    # future option is to be able to change the uploaded file
    return ""


# returns the stored file
def show_file(req):
    return ""


# checks for validation role, unlocks version, so it becomes the last/active version in the system
# or when set_valid is false then sets reject attribute to TRUE
def validate(req, set_valid):
    if 'item_id' in req.json:
        item_id = req.json['item_id']
    else:
        return jsonify(message="Bad request."), 404
    version = ItemVersion.query.filter_by(item_id=item_id).first()
    if not version:
        return jsonify(message="Version not found"), 404
    # checking permission
    if 'validator_id' in req.json and employeemng.exists(req.json['validator_id']):
        validator_id = req.json['validator_id']
    else:
        return jsonify(message="An error happened, validator user not found."), 404
    if not rolemng.exists(validator_id, version.project_id, 3) or \
            EventProj.query.filter_by(event_id=version.project_id,
                                      responsible_id=validator_id):
        return jsonify(message="This user does not have permission to validate items."), 404
    if set_valid:
        if not version.version == 1:
            prev_version = ItemVersion.query.filter_by(itemmain_id=version.itemmain_id,
                                                       islastver=True).first()
            prev_version.islastver = 0
        version.islastver = 1
        version.lockstate = 0
        version.rejected = 0
        db.session.commit()
        return jsonify(message="Item has been validated successfully"), 201
    version.rejected = 1
    db.session.commit()
    return jsonify(message="Item has been successfully rejected"), 201


# DELETE
# cross-reference should be handled here
# if there's only one single version, main info and stored file versions should be deleted as well
def delete(item_id: int):
    version = ItemVersion.query.filter_by(item_id=item_id).first()
    if version:
        db.session.delete(version)
        db.session.commit()
        return jsonify(Message="Version has been deleted"), 202
    else:
        return jsonify(Message="An error happened, version not found"), 404


# #################################################################
# OTHER
# #################################################################

def get_versions(itemmain_id):
    version_list = ItemVersion.query.filter_by(itemmain_id=itemmain_id)
    result = version_list.dump(version_list)
    return jsonify(result), 200
