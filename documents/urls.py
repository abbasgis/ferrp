from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', document_browser, name='document_browser'),
    url(r'^doc_upload/$', upload_document, name='upload_document'),
    url(r'^doc_view/$', view_document, name='view_document'),
    url(r'^doc_delete/$', delete_document, name='delete_document'),
    url(r'^doc_download/$', download_document, name='download_document'),
    url(r'^set_doc_permission/$', set_doc_permission, name='set_doc_permission'),
]
