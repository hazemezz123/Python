import customtkinter as ctk
from pytube import YouTube, Playlist
import os
from threading import Thread
import re
import time
import random
import string
import urllib.request
import ssl

class YouTubeDownloader:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("YouTube Video Downloader")
        self.window.geometry("1000x900")
        # Make window resizable
        self.window.resizable(True, True)
        # Set minimum window size
        self.window.minsize(800, 600)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Bypass SSL certificate verification (helps with some connection issues)
        ssl._create_default_https_context = ssl._create_unverified_context
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container frame that will expand with window
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # URL Entry
        url_frame = ctk.CTkFrame(main_frame)
        url_frame.pack(pady=20, padx=20, fill="x")
        
        url_label = ctk.CTkLabel(url_frame, text="YouTube URL:")
        url_label.pack(side="left", padx=10)
        
        self.url_entry = ctk.CTkEntry(url_frame, width=400)
        self.url_entry.pack(side="left", padx=10, fill="x", expand=True)
        
        # Format Selection
        format_frame = ctk.CTkFrame(main_frame)
        format_frame.pack(pady=20, padx=20, fill="x")
        
        format_label = ctk.CTkLabel(format_frame, text="Format:")
        format_label.pack(side="left", padx=10)
        
        self.format_var = ctk.StringVar(value="mp4")
        self.format_menu = ctk.CTkOptionMenu(
            format_frame,
            values=["mp4", "mp3"],
            variable=self.format_var
        )
        self.format_menu.pack(side="left", padx=10)
        
        # Quality Selection
        quality_frame = ctk.CTkFrame(main_frame)
        quality_frame.pack(pady=20, padx=20, fill="x")
        
        quality_label = ctk.CTkLabel(quality_frame, text="Quality:")
        quality_label.pack(side="left", padx=10)
        
        self.quality_var = ctk.StringVar(value="720p")
        self.quality_menu = ctk.CTkOptionMenu(
            quality_frame,
            values=["1080p", "720p", "480p", "360p", "highest", "lowest"],
            variable=self.quality_var
        )
        self.quality_menu.pack(side="left", padx=10)
        
        # Playlist Selection Frame - make it scrollable
        playlist_container = ctk.CTkFrame(main_frame)
        playlist_container.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.playlist_frame = ctk.CTkScrollableFrame(playlist_container)
        self.playlist_frame.pack(fill="both", expand=True)
        
        # Bottom frame for controls
        bottom_frame = ctk.CTkFrame(main_frame)
        bottom_frame.pack(pady=10, padx=20, fill="x", side="bottom")
        
        # Status Label
        self.status_label = ctk.CTkLabel(bottom_frame, text="")
        self.status_label.pack(pady=10)
        
        # Download Button
        self.download_btn = ctk.CTkButton(
            bottom_frame,
            text="Download",
            command=self.start_download
        )
        self.download_btn.pack(pady=10)
        
        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(bottom_frame)
        self.progress_bar.pack(pady=10, padx=20, fill="x")
        self.progress_bar.set(0)
        
        # Window control buttons
        control_frame = ctk.CTkFrame(main_frame)
        control_frame.pack(pady=5, padx=20, fill="x")
        
        # Add maximize/minimize buttons
        minimize_btn = ctk.CTkButton(
            control_frame,
            text="Minimize",
            width=100,
            command=self.window.iconify
        )
        minimize_btn.pack(side="left", padx=5)
        
        # Toggle fullscreen button
        self.is_fullscreen = False
        self.fullscreen_btn = ctk.CTkButton(
            control_frame,
            text="Maximize",
            width=100,
            command=self.toggle_fullscreen
        )
        self.fullscreen_btn.pack(side="left", padx=5)
        
    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.window.attributes("-fullscreen", self.is_fullscreen)
        self.fullscreen_btn.configure(text="Exit Fullscreen" if self.is_fullscreen else "Maximize")
        
    def is_playlist(self, url):
        return "playlist" in url or "&list=" in url
    
    def get_safe_filename(self, title):
        # Remove invalid characters from filename
        safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
        # If title is empty or None, generate a random filename
        if not safe_title:
            random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            return f"video_{random_str}"
        return safe_title
    
    def create_youtube_object(self, url):
        # Create YouTube object with additional parameters to help with connection issues
        return YouTube(
            url,
            use_oauth=False,
            allow_oauth_cache=False,
            on_progress_callback=self.update_progress
        )
        
    def get_video_info(self, url):
        max_retries = 3
        retry_count = 0
        
        # Check internet connection first
        try:
            urllib.request.urlopen("https://www.youtube.com", timeout=5)
        except:
            self.status_label.configure(text="No internet connection. Please check your network.")
            return []
        
        while retry_count < max_retries:
            try:
                if self.is_playlist(url):
                    try:
                        playlist = Playlist(url)
                        # Force initialization of playlist
                        _ = playlist.video_urls
                        
                        if not playlist.video_urls:
                            self.status_label.configure(text="Playlist is empty or could not be accessed.")
                            return []
                            
                        videos = []
                        for video_url in playlist.video_urls:
                            try:
                                yt = self.create_youtube_object(video_url)
                                # Test accessing title to ensure it works
                                _ = yt.title
                                videos.append(yt)
                            except Exception as e:
                                self.status_label.configure(text=f"Skipping video {video_url}: {str(e)}")
                                continue
                        return videos
                    except Exception as e:
                        self.status_label.configure(text=f"Error accessing playlist: {str(e)}")
                        retry_count += 1
                else:
                    # Clean the URL (remove unnecessary parameters)
                    if "youtube.com/watch" in url:
                        # Extract video ID
                        video_id = None
                        if "v=" in url:
                            video_id = url.split("v=")[1].split("&")[0]
                        
                        if video_id:
                            clean_url = f"https://www.youtube.com/watch?v={video_id}"
                        else:
                            clean_url = url
                    else:
                        clean_url = url
                        
                    video = self.create_youtube_object(clean_url)
                    # Test accessing title to ensure it works
                    _ = video.title
                    return [video]
            except Exception as e:
                retry_count += 1
                self.status_label.configure(text=f"Error: {str(e)}. Retrying ({retry_count}/{max_retries})...")
                time.sleep(2)  # Wait before retrying
        
        self.status_label.configure(text=f"Failed to access video information after {max_retries} attempts.")
        return []
            
    def update_progress(self, stream, chunk, bytes_remaining):
        if stream and stream.filesize:
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            percentage = bytes_downloaded / total_size
            self.progress_bar.set(percentage)
            self.window.update()
        
    def download_video(self, video, quality, format_type):
        try:
            # Try to get the title, if it fails, use a random filename
            try:
                video_title = video.title
            except:
                video_title = f"video_{random.randint(1000, 9999)}"
            
            safe_title = self.get_safe_filename(video_title)
            
            if format_type == "mp3":
                stream = video.streams.filter(only_audio=True).first()
            else:
                if quality in ["highest", "lowest"]:
                    # Get highest or lowest quality
                    streams = video.streams.filter(progressive=True, file_extension=format_type)
                    if not streams:
                        streams = video.streams.filter(file_extension=format_type)
                    
                    if quality == "highest":
                        stream = streams.order_by('resolution').desc().first()
                    else:
                        stream = streams.order_by('resolution').first()
                else:
                    # Try to get the requested quality
                    stream = video.streams.filter(
                        progressive=True,
                        file_extension=format_type,
                        resolution=quality
                    ).first()
                    
                    # If no stream with the exact quality is found, get the best available
                    if not stream:
                        stream = video.streams.filter(
                            progressive=True,
                            file_extension=format_type
                        ).order_by('resolution').desc().first()
                
            if not stream:
                # Last resort: try any available stream
                stream = video.streams.first()
                
            if not stream:
                self.status_label.configure(text=f"No suitable stream found for {safe_title}")
                return False
                
            # Create downloads folder if it doesn't exist
            if not os.path.exists("downloads"):
                os.makedirs("downloads")
                
            # Download the video
            file_path = stream.download(
                output_path="downloads",
                filename=f"{safe_title}.{format_type}",
                skip_existing=False
            )
            
            # For MP3 format, we need to rename the file if it's downloaded as MP4
            if format_type == "mp3" and file_path.endswith(".mp4"):
                mp4_path = file_path
                mp3_path = file_path.replace(".mp4", ".mp3")
                os.rename(mp4_path, mp3_path)
            
            return True
            
        except Exception as e:
            self.status_label.configure(text=f"Error downloading: {str(e)}")
            return False
            
    def start_download(self):
        url = self.url_entry.get()
        if not url:
            self.status_label.configure(text="Please enter a YouTube URL")
            return
            
        self.download_btn.configure(state="disabled")
        self.status_label.configure(text="Fetching video information...")
        
        # Start download in a separate thread
        Thread(target=self.download_thread, args=(url,)).start()
        
    def download_thread(self, url):
        try:
            videos = self.get_video_info(url)
            if not videos:
                self.status_label.configure(text="No videos found or unable to access video information")
                self.download_btn.configure(state="normal")
                return
                
            format_type = self.format_var.get()
            quality = self.quality_var.get()
            
            if len(videos) == 1:
                # Single video download
                video = videos[0]
                try:
                    video_title = video.title
                except:
                    video_title = "Unknown video"
                    
                self.status_label.configure(text=f"Downloading: {video_title}")
                success = self.download_video(video, quality, format_type)
                
                if success:
                    self.status_label.configure(text="Download completed!")
                else:
                    self.status_label.configure(text="Download failed!")
                    
            else:
                # Playlist download
                self.status_label.configure(text=f"Found {len(videos)} videos in playlist")
                successful_downloads = 0
                
                for i, video in enumerate(videos, 1):
                    try:
                        video_title = video.title
                    except:
                        video_title = f"Video #{i}"
                        
                    self.status_label.configure(text=f"Downloading video {i}/{len(videos)}: {video_title}")
                    if self.download_video(video, quality, format_type):
                        successful_downloads += 1
                    
                self.status_label.configure(text=f"Playlist download completed! {successful_downloads}/{len(videos)} videos downloaded successfully.")
                
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}")
            
        finally:
            self.download_btn.configure(state="normal")
            self.progress_bar.set(0)
            
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = YouTubeDownloader()
    app.run() 