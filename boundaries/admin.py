
# Register your models here.
from django.contrib.admin import AdminSite

from ferrp.boundaries.admin_boundaries import BoundariesInfoAdmin
from ferrp.boundaries.models import BoundariesInfo

class BoundariesAdminSite(AdminSite):
    site_title = 'Boundaries Management'
    site_header = 'P&D Department'

boundaries_admin_site = BoundariesAdminSite(name='admin_boundaries')
boundaries_admin_site.register(BoundariesInfo, BoundariesInfoAdmin)


