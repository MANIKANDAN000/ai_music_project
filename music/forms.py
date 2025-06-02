from django import forms
from .models import Song, AIModelLog

class SongUploadForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'genre', 'audio_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Song Title'}),
            'artist': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Artist Name'}),
            'genre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Genre'}),
            'audio_file': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class MusicGenerationForm(forms.Form):
    prompt_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Describe the music you want to generate (e.g., "upbeat electronic dance track with a heavy bassline")'}),
        label="Music Prompt"
    )
    # You could add more fields here like duration, instruments, mood, etc.
    # Example:
    # duration_seconds = forms.IntegerField(min_value=10, max_value=300, label="Duration (seconds)", initial=60)

    # This form won't directly create an AIModelLog,
    # but its data will be used by the view to call the service and then log.