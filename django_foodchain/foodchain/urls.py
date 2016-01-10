from django.conf.urls import url

from . import views


urlpatterns = [
		url(r'^$', views.info, name='info'),
		url(r'^(?P<txid>\w+)$', views.txid, name='txid'),
		url(r'^(?P<temp>\w+)/to/(?P<other>)\w+$', views.temp),
        url(r'^(?P<fromAddress>)\w+/(?P<toAddress>)\w+/(?P<assetNameHex>)\w+/(?P<assetQtyHex>)(.*)/(?P<metaDataHex>)(.*)$', views.producer, name='producer')
        ]
