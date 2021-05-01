from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
import initdata

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
jwt = JWTManager(app)
mail = Mail(app)

from controllers import routes_blueprint
app.register_blueprint(routes_blueprint)
CORS(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    db.session.commit()
    print('Database created')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    db.session.commit()
    print('Database dropped')


@app.cli.command('db_seed')
def db_seed():
    app_company = initdata.company
    app_admin = initdata.admin
    app_validator = initdata.test_validator
    app_test_user = initdata.test_user
    app_permission_r = initdata.read_permission
    app_permission_w = initdata.write_permission
    app_permission_v = initdata.validate_permission

    db.session.add(app_company)
    db.session.add(app_admin)
    db.session.add(app_validator)
    db.session.add(app_test_user)
    db.session.add(app_permission_r)
    db.session.add(app_permission_w)
    db.session.add(app_permission_v)
    db.session.commit()
    print('Database has been successfully seeded')


if __name__ == '__main__':
    app.run(debug=True)
