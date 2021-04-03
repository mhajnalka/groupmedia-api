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


from models import Employee
from schemas import EmployeeSchema
from marshmallow import ValidationError


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

    test_user = Employee(emp_id=1,
                         username='my_test_user',
                         password='123',
                         firstname='My Test',
                         lastname='User',
                         email='mytestuser@faszertvanennyiadat.com',
                         phone='06306660000',
                         fax='0612223344',
                         address='Teszt utca 124.',
                         city='Budapest',
                         region='Pest megye',
                         postcode='1034',
                         country='Magyarország',
                         lastlogin=datetime.datetime.strptime('2020/03/20', '%Y/%m/%d')
                         )
    test_user2 = Employee(emp_id=2,
                          username='my_test_user2',
                          password='12345',
                          firstname='My Test',
                          lastname='User2',
                          email='mytestuser2@faszertvanennyiadat.com',
                          phone='06306660000',
                          fax='0612223344',
                          address='Teszt utca 124.',
                          city='Budapest',
                          region='Pest megye',
                          postcode='1034',
                          country='Magyarország',
                          lastlogin=datetime.datetime.strptime('2020/03/20', '%Y/%m/%d')
                          )
    """
    request_data = dict()
    request_data['emp_id'] = "3"
    request_data['username'] = "TestUser"
    request_data['password'] = "12344"
    request_data['firstname'] = "Test"
    request_data['lastname'] = "User"
    request_data['email'] = "marhajo@gmail"
    request_data['phone'] = "0612234455"
    request_data['fax'] = ""
    request_data['address'] = "Pilis u. 9."
    request_data['city'] = "Budapest"
    request_data['region'] = "Pest megye"
    request_data['postcode'] = "1034"
    request_data['country'] = "Hungary"

    employee_schema = EmployeeSchema()
    try:
        valid_test = employee_schema.load(request_data)  # load validates the input
        db.session.add(valid_test)
    except ValidationError as err:
        print(err)

"""
    db.session.add(test_user)
    db.session.add(test_user2)
    db.session.commit()
    print('successful database seeding')


if __name__ == '__main__':
    app.run(debug=True)
