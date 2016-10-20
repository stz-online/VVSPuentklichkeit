from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from vvs_map.views import VVSDataViewSet

urlpatterns = [
    # Examples:
    # url(r'^$', 'vvs_crawler.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),

]

router = DefaultRouter()
router.register(r'users', VVSDataViewSet)