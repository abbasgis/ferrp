from ferrp.local_settings import *
from ferrp.utils import DB_Query


class SpatialDatabaseHandling(object):
    # # default_apps = ['auth', 'admin', 'sessions', 'contenttypes']
    #
    def db_for_read(self, model, **hints):
        connection_name =DB_Query.get_connection_name(model._meta.app_label,model._meta.model_name)
        return connection_name

    def db_for_write(self, model, **hints):
        # if model._meta.app_label in SPATIAL_APPS or model._meta.model_name in SPATIAL_TABLES:
        #     return SPATIAL_DB
        # return 'default'
        connection_name =DB_Query.get_connection_name(model._meta.app_label,model._meta.model_name)
        return connection_name


    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in SPATIAL_APPS or model_name in SPATIAL_TABLES:
            if db == SPATIAL_DB:
                return True
            else:
                return False
        else:
            if db == SPATIAL_DB:
                return False
            else:
                return True
        return None

