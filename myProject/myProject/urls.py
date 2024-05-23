from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import login_view

urlpatterns = [
    #django自帶login
    path('login/', login_view, name='login'),
    path('admin/', admin.site.urls),
    path('', include("myApp.urls")),

]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 