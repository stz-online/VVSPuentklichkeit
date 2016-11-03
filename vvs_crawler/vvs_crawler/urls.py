from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from vvs_map.views import VVSDataViewSet

router = DefaultRouter()
router.register(r'vvs_data', VVSDataViewSet)

urlpatterns = [
    # Examples:
    # url(r'^$', 'vvs_crawler.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^delays/', VVSDataViewSet.as_view({'get': 'list_delays'})),


]

urlpatterns += router.urls

