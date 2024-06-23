from mongoengine import (
    connect,
    Document,
    StringField,
    EmailField,
    BooleanField,
    ReferenceField,
    ListField,
    CASCADE,
)


class Contact(Document):
    fullname = StringField(required=True, unique=True)
    phone = StringField(max_length=20, required=True)
    email = EmailField(max_length=50)
    email_sent = BooleanField(default=False)
    sms_sent = BooleanField(default=False)
    send_method = StringField(choices=["email", "sms"], default="email")
    meta = {"collection": "contacts"}
