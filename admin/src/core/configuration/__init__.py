from src.core.database import db
from src.core.configuration.configuration import Configuration


def get_configuration():
    return Configuration.query.first()


def create_configuration(**kwargs):
    configuration = Configuration(**kwargs)
    db.session.add(configuration)
    db.session.commit()

    return configuration


def update_configuration(**kwargs):
    configuration = get_configuration()
    configuration.per_page = kwargs['per_page']
    configuration.contact = kwargs['contact']
    configuration.enabled_site = kwargs['enabled_site']
    configuration.maintenance_message = kwargs['maintenance_message']
    db.session.commit()

    return configuration
