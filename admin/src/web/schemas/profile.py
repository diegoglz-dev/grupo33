from marshmallow import Schema
from marshmallow import fields

class ProfileSchema(Schema):
    username=fields.Str()
    first_name=fields.Str()
    email=fields.Email()

    """ {
    "user": "usarname",
  "email": "username@mail.com",
  "document_type": "DNI",
  "document_number": "35.555.555",
  "gender": "Masculino",
  "gender_other": "transgénero",
  "address": "120 y 50",
  "phone": "221 1212-123"
}
"""


profile_schema=ProfileSchema()