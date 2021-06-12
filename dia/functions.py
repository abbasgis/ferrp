
from django.contrib.gis.geos import GEOSGeometry, Point
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
import datetime
from ferrp.dia.models import *
from geopy.geocoders import Nominatim, GoogleV3
from geopy.exc import GeocoderTimedOut
from ferrp.dia.forms import *
from ferrp.site_selection.models import *
from ferrp.models import Activity_Log
from ferrp.utils import date_handler, Log_Error
from django.contrib.auth.models import *

# google maps api key AIzaSyA354o2w3OXFrOvrVb4aWVS7a7wZ3U_KXg
def geom_to_point(projectid):
    try:

        latLong = SiteSelectionSelectedsites.objects.using('spatialds').filter(project_id=projectid)
        latlong=str(latLong[0].geom)
        # long=str(latLong[0].geom.x)
        # lat=str(latLong[0].geom.y)
        # pnt = GEOSGeometry('POINT(' + long + ' ' + lat + ')')
        # pnt.srid=3857
        # pnt=pnt.transform(4326,True)
        # print(latLong)
        return latlong
    except Exception as e:
        print(e)

def get_project_name(projectid):

    project_name = ''
    project_data_one = list(MhvraSectionOne.objects.filter(project_id=projectid).all())
    project_name = project_data_one[0].project_name
    return project_name

def get_address(lat, long):

    # long = request.GET.get('long')
    # lat = request.GET.get('lat')
    # geolocator = Nominatim(user_agent="ferrp/dia")

    # geo_locator_google= GoogleV3(api_key="AIzaSyA354o2w3OXFrOvrVb4aWVS7a7wZ3U_KXg", timeout=30)
    # location_google = geo_locator_google.reverse("" + lat + "," + long + "")
    # if(len(location_google)>0):
    #  print(location_google.address)
    #  location=location_google.address
    #  return location_google
    # else:
     geo_locator_osm = Nominatim(user_agent="ferrp/dia")
     try:
         location_osm = geo_locator_osm.reverse("" + lat + "," + long + "", timeout=None)
         print(location_osm)
         # location = location_osm.address
         return location_osm
     except Exception as e:
         print("Error: geocode failed on input",e)

def climate_classification(projectID):
    projectID = projectID
    geom_data_base = geom_to_point(projectID)

    print(geom_data_base)
    return geom_data_base





