from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hiker.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^v/$', 'hiker.hithiker.views.index'),
    url(r'^ClassRoom/add/$', 'hiker.hithiker.views.ClassroonAdd'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
