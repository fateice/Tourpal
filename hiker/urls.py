from django.conf.urls import patterns, include, url
import  settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hiker.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^ClassRoom/add/$', 'hiker.hithiker.views.ClassroonAdd'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'hiker.hithiker.views.welcome'),
    url(r'^index.html/$', 'hiker.hithiker.views.index'),
    url(r'^destinations.html/$', 'hiker.hithiker.views.destinations'),
    url(r'^criuses.html/$', 'hiker.hithiker.views.criuses'),
    url(r'^contact.html/$', 'hiker.hithiker.views.contact'),
    url(r'^blog.html/$', 'hiker.hithiker.views.blog'),
    url( r'^static/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root':settings.STATIC_ROOT }),
)
