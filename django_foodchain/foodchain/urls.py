from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'(?P<fromAddress>)/(?P<toAddress>)/(?P<assetHex>)/(?P<metaDataHex>)$', views.info, name='info')
        ]
