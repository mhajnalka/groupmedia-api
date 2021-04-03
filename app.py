import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
jwt = JWTManager(app)

from controllers import routes_blueprint
app.register_blueprint(routes_blueprint)

import initdata


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
    app_test_user = initdata.test_user
    app_permission_r = initdata.read_permission
    app_permission_w = initdata.write_permission

    db.session.add(app_company)
    db.session.add(app_test_user)
    db.session.add(app_permission_r)
    db.session.add(app_permission_w)
    db.session.commit()
    print('Database has been successfully seeded')


if __name__ == '__main__':
    app.run(debug=True)
