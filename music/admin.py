from django.contrib import admin
from .models import Song, AIModelLog

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'genre', 'uploaded_at')
    search_fields = ('title', 'artist', 'genre')
    list_filter = ('genre', 'uploaded_at')

@admin.register(AIModelLog)
class AIModelLogAdmin(admin.ModelAdmin):
    list_display = ('prompt_text', 'generated_song', 'created_at', 'status')
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at',) # If you have auto_now_add

# If you only want basic registration:
# admin.site.register(Song)
# admin.site.register(AIModelLog)