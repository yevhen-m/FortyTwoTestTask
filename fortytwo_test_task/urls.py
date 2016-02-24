from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import login
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from apps.hello import views


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
    url(r'^requests/$', views.requests, name='requests'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(
        r'^login/$',
        login,
        {'template_name': 'hello/login.html'},
        name='login'
    ),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
