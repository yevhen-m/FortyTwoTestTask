from django.conf.urls import patterns, include, url

from django.contrib import admin

from apps.hello import views


admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', views.home, name='home'),
    url(r'^requests/$', views.requests, name='requests'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
