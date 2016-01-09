from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^/(?P<txid>)$', views.info, name='info')
        ]
