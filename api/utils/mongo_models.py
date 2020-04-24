from mongoengine import Document, EmbeddedDocument
from mongoengine import DateTimeField, IntField, FloatField
from mongoengine import StringField, ListField, EmbeddedDocumentField


class Stats(EmbeddedDocument):
    last_updated = DateTimeField(required=True)
    tested = IntField(required=False)
    confirmed = IntField(required=True)
    deaths = IntField(required=True)


class Country(Document):
    country = StringField(required=True)
    alpha2Code = StringField(max_length=2, required=True)
    lat = FloatField(required=True)
    lon = FloatField(required=True)
    population = IntField(required=False)
    area = FloatField(required=False)
    stats = ListField(EmbeddedDocumentField(Stats, required=True))


class State(Document):
    state = StringField(required=True)
    stateAbbr = StringField(max_length=2, required=True)
    lat = FloatField(required=True)
    lon = FloatField(required=True)
    population = IntField(required=False)
    area = FloatField(required=False)
    stats = ListField(EmbeddedDocumentField(Stats, required=True))


class County(Document):
    state = StringField(required=True)
    stateAbbr = StringField(max_length=2, required=True)
    county = StringField(require=True)
    fips = IntField(required=True)
    lat = FloatField(required=True)
    lon = FloatField(required=True)
    population = IntField(required=True)
    area = FloatField(required=True)
    hospitals = IntField(required=False)
    hospital_beds = IntField(required=False)
    medium_income = FloatField(required=True)
    stats = ListField(EmbeddedDocumentField(Stats, required=True))
