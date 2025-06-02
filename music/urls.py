from django.urls import path
from . import views

app_name = 'music' # For namespacing URLs

urlpatterns = [
    path('', views.index_view, name='index'),
    path('upload/', views.upload_song_view, name='upload_song'),
    path('generate/', views.generate_music_view, name='generate_music'),
    path('result/<int:log_id>/', views.generation_result_view, name='generation_result'),
    path('song/<int:song_id>/', views.song_detail_view, name='song_detail'),
    path('song/<int:song_id>/analyze/', views.analyze_song_view, name='analyze_song'),
]