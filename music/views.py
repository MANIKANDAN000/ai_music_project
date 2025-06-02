from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Song, AIModelLog
from .forms import SongUploadForm, MusicGenerationForm
from .services import generate_music_from_prompt, analyze_uploaded_song
from django.contrib import messages

def index_view(request):
    songs = Song.objects.order_by('-uploaded_at')[:10] # Get latest 10 songs
    ai_logs = AIModelLog.objects.order_by('-created_at')[:5] # Get latest 5 generation logs
    generation_form = MusicGenerationForm()
    upload_form = SongUploadForm()

    context = {
        'songs': songs,
        'ai_logs': ai_logs,
        'generation_form': generation_form,
        'upload_form': upload_form,
        'page_title': 'AI Music Home'
    }
    return render(request, 'music/index.html', context)

def upload_song_view(request):
    if request.method == 'POST':
        form = SongUploadForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save()
            messages.success(request, f"Song '{song.title}' uploaded successfully!")
            return redirect('music:song_detail', song_id=song.id)
        else:
            messages.error(request, "There was an error uploading the song. Please check the form.")
    else:
        form = SongUploadForm()

    context = {
        'form': form,
        'page_title': 'Upload Song'
    }
    return render(request, 'music/upload_song.html', context)


def generate_music_view(request):
    if request.method == 'POST':
        form = MusicGenerationForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt_text']
            # Create a log entry first
            log_entry = AIModelLog.objects.create(prompt_text=prompt)
            
            # In a real app, you might use Celery for long-running tasks
            # For now, call the service directly
            # service_result = generate_music_from_prompt(prompt, log_entry) # The service updates the log
            
            # For this example, let's redirect to a page that will show the status
            # and maybe auto-refresh or use JS to poll.
            # The actual generation happens in the service call, which is synchronous here.
            # In a real async setup, the service would be triggered, and this view would return quickly.
            generate_music_from_prompt(prompt, log_entry) # Synchronous call for simplicity

            messages.info(request, f"Music generation for '{prompt[:50]}...' has started. Check status below or on the result page.")
            return redirect('music:generation_result', log_id=log_entry.id)
        else:
            messages.error(request, "Invalid prompt. Please try again.")
            return redirect('music:index') # Or render the form again with errors
    return redirect('music:index') # Should not be accessed via GET directly typically


def generation_result_view(request, log_id):
    log_entry = get_object_or_404(AIModelLog, pk=log_id)
    context = {
        'log_entry': log_entry,
        'page_title': 'Generation Result'
    }
    return render(request, 'music/result.html', context)

def song_detail_view(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    context = {
        'song': song,
        'page_title': f"Song: {song.title}"
    }
    return render(request, 'music/song_detail.html', context)

def analyze_song_view(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    # In a real app, this might be an async task
    analysis = analyze_uploaded_song(song_id)
    if analysis.get("success"):
        messages.success(request, f"Analysis for '{song.title}' complete.")
    else:
        messages.error(request, f"Analysis failed: {analysis.get('message', 'Unknown error')}")
    
    context = {
        'song': song,
        'analysis': analysis.get("data") if analysis.get("success") else None,
        'page_title': f"Analysis for {song.title}",
        'analysis_message': analysis.get("message")
    }
    # return redirect('music:song_detail', song_id=song.id) # Or render a specific analysis result page
    return render(request, 'music/song_analysis_result.html', context)