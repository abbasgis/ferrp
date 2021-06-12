DB_HOST = '172.104.141.250'
DB_USER = 'postgres'
DB_PASSWORD = 'postpndgres7%6'  # 'postpndgres7%6', 'postgres'
DB_PORT = 5432

SPATIAL_DB = 'spatialds'
SPATIAL_TABLES = ['projection', 'gdal_pg_raster', 'tbladminhierarchy']
SPATIAL_APPS = ['gis', 'rst', 'indus_basin', 'site_selection']  # layers

ADP_DB = 'adp'
ADP_TABLES = []
ADP_APP = ['adp']

IRRIGATION_DB = 'irrigation'
IRRIGATION_TABLES = []
IRRIGATION_APP = ['irrigation']

ROADS_SCORING_DB = 'rsma'
ROADS_SCORING_TABLES = []
ROADS_SCORING_APP = ['rsma']

# LOCAL_MHVRA_APPS = ['local_MHVRA']
# LOCAL_MHVRA_TABLES = []
# LOCAL_MHVRA_DB = 'dmapp_local'
#
# REMOTE_MHVRA_APPS = ['remote_MHVRA']
# REMOTE_MHVRA_TABLES = []
# REMOTE_MHVRA_DB = 'dmapp'

SURVEY_STATS_APPS = ['survey_stats_app']
SURVEY_STATS_TABLES = []
SURVEY_STATS_DB = 'mhvra_local_db'

PC1_DB = 'pc1_db'
PC1_TABLES = []
PC1_APP = ['pc1']

DIA_DB = 'db_dia'
DIA_TABLES = []
DIA_APP = ['dia']

MEETINGS_DB = 'db_mm'
MEETINGS_TABLES = []
MEETINGS_APP = ['meeting_management']

DELSAP_DB = 'delsap'
DELSAP_TABLES = []
DELSAP_APP = ['delsap']

SHP_FILE_EXTENSIONS = ['.shp', '.dbf', '.shx', '.prj']

SPATIAL_EXTENT_4326 = (60.5000000000624, 23.4999999998205, 79.5000000003122, 37.5000000001664)
SPATIAL_EXTENT_3857 = (6734829.193000, 2692598.219300, 8849899.518100, 4509031.393100)
DEFAULT_PROJECTION = 3857

MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiYXRoZXJhc2hyYWYiLCJhIjoiY2llaGdzMmV4MDAyYnN2a2g2cjhma21lciJ9.9KGKcWYuXd8hojFP9HYrhQ'
BING_MAP_KEY = 'nIpvP3DE4KDIPD5rbvf8~tYqmHfqtK9FrpulnwqB6Ow~AlfsQeqqd1RiQqE5rzdQnrgwjgawr26TNXWuLLIrlyMRj2JEp_IhUATReKhb4rCt'

OVERVIEW_FACTOR = ['2', '4', '8']
MAP_SRID = 3857

PERMISSION_TYPE = (
    ('P', 'Public'),
    ('O', 'Owner'),
    ('V', 'View'),
    ('D', 'Download'),
    ('S', 'Save')
)
ENTITY_TYPE = (
    ('U', 'User'),
    ('D', 'Department'),
)
MIN_TEMP_VAL = -5
MAX_TEMP_VAL = 40

BOUNDARIES_TYPE={
    ('IB', 'Internation Boundaries' ),
    ('AB', 'Administration Boundaries'),
    ('BOR', 'Board of Revenue'),
    ('PID', 'Irrigation Boundaries'),
    ('LG', 'Local Government'),
    ('IndB', 'Indus Basin Catchments')
}
