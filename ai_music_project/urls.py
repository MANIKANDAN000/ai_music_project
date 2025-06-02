# ai_music_project/ai_music_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from music import views as music_views # Import views from your music app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('music/', include('music.urls')), # This sets up the 'music:' namespace
    path('', music_views.index_view, name='home'), # Root path directly to the music index view
                                                 # No 'music:' namespace here for the root itself.
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)