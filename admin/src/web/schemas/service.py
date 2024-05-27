from marshmallow import Schema
from marshmallow import fields

class ServiceSchema(Schema):
    id=fields.Integer()
    name=fields.Str()
    description=fields.Str()
    keywords=fields.Str() 

    def get_type_of_service(self, obj):
        return obj.type_of_service.value

    type_of_service = fields.Method("get_type_of_service")
    enabled=fields.Bool()


services_schema=ServiceSchema(many=True)
service_schema=ServiceSchema()
