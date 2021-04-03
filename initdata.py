from models import Company, Employee, Permission


company = Company(comp_id=1,
                  name='Media Company',
                  email='testuser@testmail.com',
                  phone='06306660000',
                  fax='0612223344',
                  web='www.mediacompanytest.com',
                  address='Teszt utca 124.',
                  city='Budapest',
                  region='Pest megye',
                  postcode='1034',
                  country='Magyarország'
                  )

test_user = Employee(emp_id=1,
                     username='testuser',
                     password='Pw12345',
                     firstname='Test',
                     lastname='User',
                     email='testuser@testmail.com',
                     phone='06306660000',
                     fax='0612223344',
                     address='Teszt utca 124.',
                     city='Budapest',
                     region='Pest megye',
                     postcode='1034',
                     country='Magyarország',
                     create=1
                     )

read_permission = Permission(perm_id=1,
                             name='READ')

write_permission = Permission(perm_id=2,
                              name='WRITE')
