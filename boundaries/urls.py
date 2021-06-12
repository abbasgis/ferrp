from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', bounaries_browser, name='boundaries_browser'),
]
