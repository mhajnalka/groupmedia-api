import datetime
import os
from flask import jsonify, request, send_file
from marshmallow import ValidationError
from werkzeug.utils import secure_filename
from logic import employeemng, eventmng, itemmng, rolemng, mailsender
from schemas import ItemMainSchema, ItemVersionSchema
from models import *
from app import db, app

version_schema = ItemVersionSchema()
versions_schema = ItemVersionSchema(many=True)


# #################################################################
# FOR ITEM REQUESTS
# #################################################################

# ADD
# Identified by name, so can be handled together with the main object
def add(req):
    print(req.files)
    print(req.form)
    # return jsonify(message="An error happened: event with wrong state"), 200

    if 'name' in req.form:
        name = req.form['name']
        item = ItemMain.query.filter_by(name=name).first()
        version = ItemVersion()
        version.desc = req.form['desc'] if 'desc' in req.form else ""
        version.lockstate = 1
        version.rejected = 0
        version.islastver = 0
        version.creadate = datetime.datetime.now()
        # checking project and it's state, which must be modifiable
        if 'project_id' in req.form and eventmng.exists(req.form['project_id']):
            if eventmng.is_wip(req.form['project_id']):
                version.project_id = req.form['project_id']
            else:
                return jsonify(message="An error happened: event with wrong state"), 404
        else:
            return jsonify(message="An error happened, event not found."), 404
        # checking creator
        employee = employeemng.find_user(req.form['creator_id'])
        if 'creator_id' in req.form and employee:
            version.creator_id = employee.emp_id
        else:
            return jsonify(message="An error happened, creator not found."), 404
        # checking roles
        if not rolemng.exists(version.creator_id, version.project_id, 2):

            print('ERROR HERE II')
            return jsonify(message="Role not found, permission denied."), 404
        # item is true when it exists with the param of name
        if item:
            try:
                # version only
                # checking main item's connected last version, if not locked, then it has to be updated as well
                # we have to raise the major part of the version number, minor part is not handled
                prev_version = ItemVersion.query.filter_by(itemmain_id=item.itemmain_id,
                                                           islastver=True).first()
                if not prev_version:
                    return jsonify(message="Previous version hasn't been validated yet."), 401
                if prev_version.lockstate:
                    return jsonify(message="Item cannot be modified when previous version is locked."), 401
                version.version = prev_version.version + 1
                version.itemmain_id=item.itemmain_id

                # needs to be stored (also renamed)
                if 'file2upload' not in req.files:
                    return jsonify(message="Missing file."), 401
                file = req.files['file2upload']
                if file.filename == '':
                    return jsonify(message="Missing file."), 401
                version.filename = process_file(file=file,
                                                name=item.name,
                                                version=version.version)
                db.session.add(item)
                db.session.add(version)
                db.session.commit()
                mailsender.upload(item_data=repr(item)+repr(version),
                                  uploader_data=repr(employee))
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
            new_item = itemmng.add(req.form)
            if isinstance(new_item, str):
                print('itt a hiba')
                return jsonify(message=new_item), 401
            version.itemmain_id = new_item.itemmain_id
            try:
                # needs to be stored (also renamed)
                if 'file2upload' not in req.files:
                    return jsonify(message="File missing."), 401
                file = req.files['file2upload']
                if file.filename == '':
                    return jsonify(message="File missing."), 401
                version.filename = process_file(file=file,
                                                name=new_item.name,
                                                version=version.version)
                db.session.add(version)
                db.session.commit()
                mailsender.upload(item_data=repr(new_item) + repr(version),
                                  uploader_data=repr(employee))
            except (TypeError, ValidationError) as err:
                return jsonify(message=list(eval(str(err)).values())[0][0]), 401
            except ValueError as err:
                return jsonify(message=err), 401
            except KeyError as err:
                return jsonify(message="Missing data: " + err.args[0]), 401
    else:
        return jsonify(message="Name cannot be empty"), 404
    return jsonify(message="Item has been created"), 201


# UPDATE
def update(req):
    if 'item_id' and 'desc' in req.form:
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


# returns the stored file by item_id, so that it can be displayed/downloaded
def show_file(item_id):
    version = ItemVersion.query.filter_by(item_id=item_id).first()
    if path_exists(chk_only=True):
        try:
            return send_file(os.path.join(app.config['UPLOAD_DIR'], version.filename),
                             attachment_filename=version.filename), 200
        except FileNotFoundError as err:
            return 'File not found error', 400
    # os.path.join(app.config['UPLOAD_DIR'], version.filename)
    return 'Directory does not exist, contact the developer', 400


# checks for validation role, unlocks version, so it becomes the last/active version in the system
# or when set_valid is false then sets reject attribute to TRUE
def validate(req, set_valid):
    print(req)
    print(req.json)
    if 'item_id' in req.json:
        item_id = req.json['item_id']
        version = ItemVersion.query.filter_by(item_id=item_id).first()
    elif 'itemname' in req.json:
        itemname = req.json['itemname']
        main_item = ItemMain.query.filter_by(name=itemname).first()
        version = ItemVersion.query.filter_by(itemmain_id=main_item.itemmain_id,
                                              lockstate=1).first()
        print(itemname)
        print(main_item.itemmain_id)
        print(version.filename)
    else:
        print('Bad request')
        return jsonify(message="Bad request."), 404
    if not version:
        print(version)
        print('NOT FOUNDt')
        return jsonify(message="Version not found"), 404
    # checking permission
    validator_id = 0
    if 'username' in req.json:
        emp = employeemng.find_user(req.json['username'])
        validator_id = emp.emp_id
    else:
        print('VALIDATOR NOT FOUND')
        return jsonify(message="An error happened, validator user not found."), 404
    print(emp.create)
    if not emp.create and \
            (not rolemng.exists(validator_id, version.project_id, 3) or EventProj.query.filter_by(
                event_id=version.project_id,
                responsible_id=validator_id)):

        print('ROLE NOT FOUND')
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
        creator = employeemng.find_user_id(version.creator_id)
        mailsender.item_validate(uploader_mail=creator.email,
                                 item_data=repr(version))
        return jsonify(message="Item has been validated successfully"), 201
    version.rejected = 1
    delete(item_id=version.item_id,
           reject=True)
    db.session.commit()
    creator = employeemng.find_user_id(version.creator_id)
    mailsender.item_reject(uploader_mail=creator.email,
                           item_data=repr(version))
    return jsonify(message="Item has been successfully rejected"), 201


# receives an item ID which by restores version if the container event is still in WIP status
def restore(item_id):
    version = ItemVersion.query.filter_by(item_id=item_id).first()
    if not version:
        return jsonify(message="Version not found"), 404
    if not eventmng.is_wip(version.project_id):
        return jsonify(message="Version cannot be restored within a non WIP state event"), 400

    version_list = \
        ItemVersion.query.filter((ItemVersion.itemmain_id == version.itemmain_id)
                                 & (ItemVersion.version > version.version))
    bigger_versions = versions_schema.dump(version_list)
    for v in bigger_versions:
        bv = ItemVersion.query.filter_by(item_id=v['item_id']).first()
        db.session.delete(bv)
    version.islastver = 1
    db.session.commit()
    return jsonify(message="Version has been restored"), 200


# DELETE function
def delete(item_id: int, reject=False):
    version = ItemVersion.query.filter_by(item_id=item_id).first()
    if version:
        db.session.delete(version)
        db.session.commit()
        if reject:
            return
        return jsonify(message="Version has been deleted"), 202
    else:
        return jsonify(message="An error happened, version not found"), 404


# #################################################################
# OTHER
# #################################################################

# handles received files separately from administration
# in order to be able to manage files, file name has to be the same as defined in the add method
def process_file(file, name="item", version=1):
    try:
        if file and name_chk(file.filename):
            filename = secure_filename(file.filename)
            path_exists()
            new_name = name + str(version) + '.' + filename.rsplit('.', 1)[1].lower()
            file.save(os.path.join(app.config['UPLOAD_DIR'], new_name))
        return new_name
    except:
        return False


# checks filename if it's extension is in the array of the allowed ones
def name_chk(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['UPLOAD_EXTENSIONS']


# checks if the given path exists, creates upload directory if not
def path_exists(chk_only=False):
    if not os.path.exists(os.path.join(app.config['UPLOAD_DIR'])):
        if chk_only:
            return False
        else:
            os.makedirs(os.path.join(app.config['UPLOAD_DIR']))
    return True


# returns version by ID--
def get_versions(itemmain_id):
    version_list = ItemVersion.query.filter((ItemVersion.itemmain_id == itemmain_id))
    print(version_list)
    result = versions_schema.dump(version_list)
    print(result)
    return result
