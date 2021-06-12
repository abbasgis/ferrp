from django.contrib.gis.geos import GEOSGeometry

from ferrp.utils import DB_Query


class Spatial_Operations:
    def get_surface_profile(self, wkt, srid):
        dem_table_name = 'rst_aster_dem0_20180529223547239203' #rst_aster_dem_punjab rst_aster_dem0_20180529223547239203
        surface_profile = []
        dem_srid = 4326
        geom = GEOSGeometry(wkt)
        geom.set_srid(srid)
        length = geom.length
        num_of_points = round(length / 30)
        distance = 0
        for i in range(num_of_points):

            profile ={}
            profile['distance'] = distance
            query = "Select ST_LineInterpolatePoint('%s',%s)" % (geom, i/num_of_points)
            point = DB_Query.execute_query_as_one(query)
            geos_point = GEOSGeometry(point)
            profile['point']=geos_point.wkt
            geos_point.transform(dem_srid)
            query = "Select ST_Value(rast,'%s') from \"%s\"" \
                    " where st_intersects(envelope,'%s')" % (geos_point, dem_table_name, geos_point)
            value = DB_Query.execute_query_as_one(query)
            profile['value']=value
            surface_profile.append(profile)
            distance = distance + 30
        return surface_profile
