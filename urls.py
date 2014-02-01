from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'hellodjango.views.home', name='home'),
    url(r'^analyze', 'hellodjango.views.analyze', name='analyze'),
    url(r'^admin/', include(admin.site.urls)),
)
