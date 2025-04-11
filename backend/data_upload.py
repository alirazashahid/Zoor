import youtube_dl
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from pytesseract import image_to_string
from PIL import Image

def process_video(url):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'uploads/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3')
        
        transcript = transcribe_audio(filename)
        return transcript
    except Exception as e:
        print(f"Error processing video: {e}")
        return None

def process_screenshot(file):
    try:
        image = Image.open(file)
        text = image_to_string(image)
        return text
    except Exception as e:
        print(f"Error processing screenshot: {e}")
        return None

def process_text_file(file):
    try:
        content = file.read().decode('utf-8')
        return content
    except Exception as e:
        print(f"Error processing text file: {e}")
        return None

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return ""