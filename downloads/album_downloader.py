import os
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from youtube_search import YoutubeSearch
from pytube import YouTube
from moviepy.editor import VideoFileClip
import eyed3
from PIL import Image
from mutagen.id3 import ID3, APIC
from pathlib import Path
from io import BytesIO

# Spotify API credentials
SPOTIPY_CLIENT_ID = '09c13e8f02cb44889677444f98abcf2a'
SPOTIPY_CLIENT_SECRET = 'fa31523465de4d2590950e3172c9748f'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET))

def download_image(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

def search_for_album(album_name, artist_name):
    # Search for the album on Spotify
    results = sp.search(q=f"album:{album_name} artist:{artist_name}", type='album')
    
    if not results['albums']['items']:
        print("Album not found.")
        return None
    
    for idx, item in enumerate(results['albums']['items']):
        print(f"{idx + 1}. {item['name']} by {', '.join(artist['name'] for artist in item['artists'])}")

    # Ask the user to select the correct album
    selected_idx = int(input("Enter the number corresponding to the correct album: ")) - 1
    
    if 0 <= selected_idx < len(results['albums']['items']):
        return results['albums']['items'][selected_idx]
    else:
        print("Invalid selection. Exiting.")
        return None

def get_album_info():
    album_name = input("Enter the name of the album on Spotify: ")
    artist_name = input("Enter the name of the artist: ")
    
    # Allow the user to select the correct album
    selected_album = search_for_album(album_name, artist_name)
    if not selected_album:
        return None, None
    
    album_id = selected_album['id']
    
    # Get the names of songs in the album
    album_info = sp.album_tracks(album_id)
    song_names = [track['name'] for track in album_info['items']]
    actual_album_name = selected_album['name']
    actual_artist_name = selected_album['artists'][0]['name']
    # Download the album art and save it to the desktop
    album_art_url = selected_album['images'][0]['url']
    album_art_filename = os.path.join(os.path.expanduser("~\\Desktop"), "album_art.jpg")
    download_image(album_art_url, album_art_filename)
    
    return song_names, album_art_filename, actual_album_name, actual_artist_name

def replace_slash_backslash_in_list(song_names):
    modified_list = []

    for item in song_names:
        # Replace "/" with "-"
        modified_item = item.replace("/", "-")
        # Replace "\" with "-"
        modified_item = modified_item.replace("\\", "-")
        modified_list.append(modified_item)
    
    song_names = modified_list
    
    return song_names

def download_youtube_audio(song_name, video_url, actual_album_name, actual_artist_name):
    # Download the video from YouTube
    mp4_file_path = os.path.join(os.path.expanduser("~\\Desktop"), f"{song_name}.mp4")
    downloader(video_url, song_name, os.path.expanduser("~\\Desktop"))
    
    # Convert the downloaded video to mp3
    mp3_file_path = os.path.join(os.path.expanduser("~\\Desktop"), f"{song_name}.mp3")
    convert_mp4_to_mp3(mp4_file_path, mp3_file_path)
    audiofile = eyed3.load(mp3_file_path)
    if audiofile:
        audiofile.tag.artist = actual_artist_name
        audiofile.tag.album = actual_album_name
        audiofile.tag.save()
    
    # Remove the original mp4 file
    os.remove(mp4_file_path)

def downloader(link, name, directory):
    yt = YouTube(link)
    video_stream = yt.streams.filter(file_extension="mp4").get_highest_resolution()  # Creates meta-data for download
    video_stream.download(output_path=directory, filename=name + ".mp4")  # Uses meta-data with stream function to download video

def convert_mp4_to_mp3(input_file, output_file):
    try:
        video_clip = VideoFileClip(input_file)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(output_file, codec='mp3', bitrate='192k') 
        video_clip.close()
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    song_names, album_art_url, actual_artist_name, actual_album_name = get_album_info()
    
    song_names = replace_slash_backslash_in_list(song_names)
    
    if not song_names or not album_art_url:
        return
    
    for song_name in song_names:
        print(f"Downloading {song_name}...")
        results = YoutubeSearch(f"{song_name} {actual_album_name} - Topic {actual_artist_name}", max_results=1).to_dict()
        
        if not results:
            print(f"No results found for {song_name} on YouTube.")
            continue
        
        video_url = f"https://www.youtube.com{results[0]['url_suffix']}"
        download_youtube_audio(song_name, video_url, actual_album_name, actual_artist_name)
        
        print(f"{song_name} downloaded successfully.")
    
    print("\nAll songs downloaded successfully.")

if __name__ == "__main__":
    main()

