from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('home.urls')),
    path('api/auth/', include('authentication.urls')),
]

admin.site.site_header = "15 Percent Club"
admin.site.site_title = "15 Percent Club"
admin.site.index_title = "15 Percent Club"