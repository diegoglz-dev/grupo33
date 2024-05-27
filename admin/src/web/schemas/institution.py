from marshmallow import Schema
from marshmallow import fields

class InstitutionSchema(Schema):
    name=fields.Str()
    info=fields.Str()
    direccion=fields.Str() 
    localizacion= fields.Str()
    web=fields.Str()
    dias_horarios= fields.Str()
    contacto=fields.Str()
    habilitado= fields.Bool()


institution_schema=InstitutionSchema(many=True)
