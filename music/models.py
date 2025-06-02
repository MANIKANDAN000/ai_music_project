from django.db import models
from django.utils import timezone

class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200, blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    audio_file = models.FileField(upload_to='songs/') # Stored in MEDIA_ROOT/songs/
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # Consider adding:
    # duration = models.DurationField(blank=True, null=True)
    # cover_art = models.ImageField(upload_to='covers/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.artist}" if self.artist else self.title

class AIModelLog(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    prompt_text = models.TextField(help_text="The text prompt used for generation")
    # generated_song could be a FileField if the AI generates an audio file directly
    # For simplicity, let's assume it links to a Song entry or stores a path/ID.
    # If the AI generates a new song file, you'd create a new Song instance.
    generated_song = models.ForeignKey(Song, on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_generations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    # You might add:
    # model_name = models.CharField(max_length=100, blank=True, null=True)
    # parameters = models.JSONField(blank=True, null=True) # To store AI parameters
    # error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"AI Log ({self.id}) for: {self.prompt_text[:50]}..."