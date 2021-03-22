from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
jwt = JWTManager(app)


from controllers import routes_blueprint
app.register_blueprint(routes_blueprint)


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


"""
@app.cli.command('db_seed')
def db_seed():
    test_user = Employee(emp_ID=1,
                         username='my_test_user',
                         password='12345',
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
    test_user2 = Employee(emp_ID=2,
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
    db.session.add(test_user)
    db.session.add(test_user2)
    db.session.commit()
    print('successful database seeding')

"""


if __name__ == '__main__':
    app.run(debug=True)
