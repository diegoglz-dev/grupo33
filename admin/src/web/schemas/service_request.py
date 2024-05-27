from marshmallow import Schema
from marshmallow import fields

class ServiceRequestSchema(Schema):
    id=fields.Integer()
    
    title=fields.Str()
    
    description=fields.Str()
    
    def get_creation_date(self, obj):
        return obj.creation_date
    creation_date=fields.Method("get_creation_date")

    def get_close_date(self, obj):
        return obj.close_date
    close_date=fields.Method("get_close_date")
    
    def get_status_current(self, obj):
        status = obj.last_state
        if status:
            return status.name
        else:
            return ""
    status= fields.Method("get_status_current")


service_requests_schema=ServiceRequestSchema(many=True)
service_request_schema=ServiceRequestSchema()
