import datetime
from ferrp.layers.models import Info
from ferrp.utils import Common_Utils, Model_Utils
from django.contrib.gis.db.models import Extent
from django.contrib.gis.db import models

class Integration_Utils:
    @classmethod
    def form_data_2_database_connections(cls, data):
        title = data["connection_title"]
        name = Common_Utils.add_timestamp_to_string(title)
        connection_string = {
            'ENGINE': data['database_type'],
            'NAME': data['database_name'],
            'USER': data['db_user'],
            'PASSWORD': data['db_password'],  # 'postr2vdhagres', 'postgres'
            'HOST': data['IP_address_v4'],
            'PORT': data['port'],
        }

        return {"name": name, "title": title, "conn_string": connection_string}


