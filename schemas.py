from flask_marshmallow import Marshmallow

ma = Marshmallow()


class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('emp_ID', 'username', 'password', 'firstname', 'lastname', 'email', 'phone',
                  'fax', 'address', 'city', 'region', 'postcode', 'country', 'lastlogin')


class WorkItem(ma.Schema):
    class Meta:
        fields = ('item_ID', 'emp_ID', 'workiteminfo_ID', 'filename', 'version', 'lockstate',
                  'islastver', 'creadate')


class WorkItemInfo(ma.Schema):
    class Meta:
        fields = ('workiteminfo_ID', 'name', 'desc', 'extension', 'type')


class Role(ma.Schema):
    class Meta:
        fields = ('role_ID', 'event_ID', 'emp_ID', 'perm_ID')


class Permission(ma.Schema):
    class Meta:
        fields = ('perm_ID', 'name')


class ItemOfEvent(ma.Schema):
    class Meta:
        fields = 'ioe_ID', 'event_ID', 'item_ID'


class EventProj(ma.Schema):
    class Meta:
        fields = ('event_ID', 'name', 'desc', 'publicity', 'state', 'responsible_ID',
                  'deputy_ID', 'duedate')