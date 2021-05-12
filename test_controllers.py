import unittest
from flask import json

from app import app


class EmployeeMngTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_login(self):
        data = json.dumps({
            'username': 'testvalidator',
            'password': 'Pass123'
        })
        response = self.app.post('login',
                                 headers={'Content-Type': 'application/json'},
                                 data=data)
        self.assertEqual(200, response.status_code)

    def test_get_profile(self):
        response = self.app.get('get_profile/testuser', headers={'Content-Type': 'application/json'})
        self.assertEqual(200, response.status_code)

    def test_get_all_employees(self):
        response = self.app.get('get_all_employees', headers={'Content-Type': 'application/json'})
        self.assertEqual(200, response.status_code)

    def test_delete_employee(self):
        response = self.app.put('delete_employee/10', headers={'Content-Type': 'application/json'})
        self.assertEqual(202, response.status_code)


class EventMngTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_add_event(self):
        data = json.dumps({
            'name': 'Test Project',
            'desc': 'This is the description of my test project',
            'publicity': 1,
            'state': 'INPROGRESS',
            'duedate': '2021-05-30',
            'responsible_id': 'testvalidator'
        })
        response = self.app.post('add_event',
                                 headers={'Content-Type': 'application/json'},
                                 data=data)
        self.assertEqual(201, response.status_code)

    def test_get_all_events(self):
        response = self.app.get('get_all_events', headers={'Content-Type': 'application/json'})
        self.assertEqual(200, response.status_code)


class VersionTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_add_version(self):
        data = json.dumps({
            'filename': 'testfile',
            'extension': 'jpg',
            'type': 'img',
            'desc': 'Description of test file',
            'project_id': 1,
            'username': 'testuser'
        })

        response = self.app.post('add_version',
                                 headers={'Content-Type': 'application/json'},
                                 data=data)
        self.assertEqual(404, response.status_code)

    def test_show_file(self):
        response = self.app.post('show_file/1', headers={'Content-Type': 'application/json'})
        self.assertEqual(200, response.status_code)

    def test_get_item(self):
        response = self.app.get('get_item/1', headers={'Content-Type': 'application/json'})
        self.assertEqual(200, response.status_code)

    def test_get_all_item(self):
        response = self.app.get('get_all_item', headers={'Content-Type': 'application/json'})
        self.assertEqual(200, response.status_code)

    def test_get_versions(self):
        response = self.app.get('get_versions/newitem', headers={'Content-Type': 'application/json'})
        self.assertEqual(200, response.status_code)


class RoleMngTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_add_role(self):
        data = json.dumps({
            'username': 'testuser',
            'event_id': '1',
            'perm_id': 2,
        })

        response = self.app.post('add_role',
                                 headers={'Content-Type': 'application/json'},
                                 data=data)
        self.assertEqual(201, response.status_code)


class CompanyMngTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get_contact(self):
        response = self.app.get('get_contact', headers={'Content-Type': 'application/json'})
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
