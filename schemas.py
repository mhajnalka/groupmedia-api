from flask_marshmallow import Marshmallow

ma = Marshmallow()


class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('emp_ID', 'username', 'password', 'firstname', 'lastname', 'email', 'phone',
                  'fax', 'address', 'city', 'region', 'postcode', 'country', 'lastlogin')


class WorkItemSchema(ma.Schema):
    class Meta:
        fields = ('item_ID', 'emp_ID', 'workiteminfo_ID', 'filename', 'version', 'lockstate',
                  'islastver', 'creadate')


class WorkItemInfoSchema(ma.Schema):
    class Meta:
        fields = ('workiteminfo_ID', 'name', 'desc', 'extension', 'type')


class RoleSchema(ma.Schema):
    class Meta:
        fields = ('role_ID', 'event_ID', 'emp_ID', 'perm_ID')


class PermissionSchema(ma.Schema):
    class Meta:
        fields = ('perm_ID', 'name')


class ItemOfEventSchema(ma.Schema):
    class Meta:
        fields = 'ioe_ID', 'event_ID', 'item_ID'


class EventProjSchema(ma.Schema):
    class Meta:
        fields = ('event_ID', 'name', 'desc', 'publicity', 'state', 'responsible_ID',
                  'deputy_ID', 'duedate')
