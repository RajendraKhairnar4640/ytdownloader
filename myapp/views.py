from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# import youtube_dl
import yt_dlp as youtube_dl
from .forms import DownloadForm
import re

# Create your views here.
def download_vedio(request):
    form = DownloadForm(request.POST or None)

    if form.is_valid():
        video_url = form.cleaned_data.get("url")
        regex = r"^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+"

        if not re.match(regex, video_url):
            return HttpResponse("Enter a correct URL.")

        ydl_opts = {
            'format': 'best',  # Get the best available format
            'noplaylist': True,  # Download only the single video
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                meta = ydl.extract_info(video_url, download=False)

            if meta:
                video_audio_streams = []
                for m in meta.get("formats", []):
                    if m.get("acodec") and m.get("acodec") != 'none':  # Filter for formats with audio
                        file_size = m.get("filesize")
                        if file_size is not None:
                            file_size = f"{round(int(file_size) / 1000000, 2)} mb"

                        resolution = "Audio"
                        if m.get("height") is not None:
                            resolution = f"{m.get('height')}x{m.get('width')}"
                        
                        video_audio_streams.append(
                            {
                                "resolution": resolution,
                                "extension": m.get("ext"),
                                "file_size": file_size,
                                "video_url": m.get("url"),
                            }
                        )
                
                # If no combined audio and video formats are found, fetch separate streams
                if not video_audio_streams:
                    video_streams = [m for m in meta.get("formats", []) if m.get("vcodec") != 'none']
                    audio_streams = [m for m in meta.get("formats", []) if m.get("acodec") and m.get("acodec") != 'none']
                    
                    if video_streams and audio_streams:
                        video_audio_streams.append({
                            "resolution": "Video + Audio",
                            "extension": "mp4",
                            "video_url": video_streams[0].get("url"),
                            "audio_url": audio_streams[0].get("url"),
                        })

                video_audio_streams = video_audio_streams[::-1]  # Reverse the list for better order
                context = {
                    "form": form,
                    "title": meta.get("title", "No Title"),
                    "streams": video_audio_streams,
                    "description": meta.get("description", "No Description"),
                    "thumb": meta.get("thumbnails", [{}])[3].get("url", "No Thumbnail"),
                    "duration": round(int(meta.get("duration", 0)) / 60, 2),
                    "views": f'{int(meta.get("view_count", 0)):,}',
                }
            else:
                context = {
                    "form": form,
                    "error": "Unable to extract video information. Please check the URL and try again.",
                }
        except Exception as e:
            context = {
                "form": form,
                "error": f"An error occurred: {str(e)}",
            }

        return render(request, "myapp/download.html", context)

    return render(request, "myapp/download.html", {"form": form})