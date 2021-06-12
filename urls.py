"""ferrp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from ferrp import settings, views_account
from ferrp.views_account import account_redirect

from ferrp.meeting_management.admin import meetings_initiatives_site
from ferrp.views import *

from ferrp.projects.admin import admin_site

urlpatterns = [
                  url(r'^ferrp/$', TemplateView.as_view(template_name='index_ferrp.html'), name='home'),
                  url(r'^dimension_modeling/$', TemplateView.as_view(template_name='dimension_modeling.html'),
                      name='dim_model'),
                  url('^', include('django.contrib.auth.urls')),
                  url(r'^$', TemplateView.as_view(template_name='index_dch.html'), name='home_dch'),

                  url(r'^account_login/$', account_login, name='account_login'),
                  url(r'^accounts/', include('allauth.urls')),
                  # url(r'^accounts/profile/$', account_redirect, name='profile'),
                  url(r'^accounts/profile/$', account_profile, name="account_profile"),
                  url(r'^accounts/setpassword/$', set_new_password, name="set_new_password"),

                  url(r"^confirm-email/(?P<key>[-:\w]+)/$", views_account.confirm_email,
                      name="account_confirm_email"),
                  url(r'^login_linkedin/', login_linkedin, name='login_linkedin'),
                  url(r'^account_logout/$', account_logout, name='account_logout'),
                  # url(r'^accounts/login/$', 'django.contrib.auth.views.login'),

                  url('^searchableselect/', include('searchableselect.urls')),
                  url('^searchableselect/', include('searchableselect.urls')),
                  url(r'^tinymce/', include('tinymce.urls')),
                  url(r'^get_user_department_list/', user_department_list, name='user_department'),
                  url(r'^get_attribute_list/', attribute_list, name='attribute_list'),
                  url(r'^get_attribute_distinct_value/', attribute_distinct_value, name='attribute_distinct_value'),
                  url(r'^get_raster_summary/', raster_summary, name='raster_summary'),
                  url(r'^get_layer_info/', get_layer_info, name='get_layer_info'),

                  url(r'^get_model_fields/', model_fields_list, name='model_fields_list'),

                  url(r'^admin/', admin.site.urls),
                  url(r'^admin_dch/', admin_site.urls),
                  url(r'^layers/', include('ferrp.layers.urls')),
                  url(r'^web_services/', include('ferrp.web_services.urls')),
                  url(r'^maps/', include('ferrp.maps.urls')),
                  url(r'^map_3d/', include('ferrp.map_3d.urls')),
                  url(r'^documents/', include('ferrp.documents.urls')),
                  url(r'^projects/', include('ferrp.projects.urls')),
                  url(r'^indus_basin/', include('ferrp.indus_basin.urls')),
                  url(r'^irrigation/', include('ferrp.irrigation.urls')),
                  url(r'^adp/', include('ferrp.adp.urls')),
                  url(r'^ing/', include('ferrp.integration.urls')),
                  url(r'^survey_stats/', include('ferrp.survey_stats_app.urls')),
                  # url(r'^rsma/', include('ferrp.rsma.urls')),
                  url(r'^climate/', include('ferrp.climate_change.urls')),
                  url(r'^ssa/', include('ferrp.site_selection.urls')),
                  url(r'^pc1/', include('ferrp.pc1.urls')),
                  url(r'^mm/', include('ferrp.meeting_management.urls')),
                  url(r'^dia/', include('ferrp.dia.urls')),
                  url(r'^admin_meetings/', meetings_initiatives_site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
