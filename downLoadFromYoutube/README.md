# YouTube Video Downloader

A Python application with a graphical user interface for downloading YouTube videos and playlists.

## Features

- Download single YouTube videos
- Download entire playlists
- Select video quality (1080p, 720p, 480p, 360p)
- Choose file format (MP4, MP3)
- Progress bar showing download status
- Modern dark-themed GUI

## Requirements

- Python 3.6 or higher
- Required packages listed in `requirements.txt`

## Installation

1. Clone or download this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:

```bash
python youtube_downloader.py
```

2. Enter a YouTube URL (video or playlist)
3. Select the desired format (MP4 or MP3)
4. Choose the video quality
5. Click the "Download" button

The downloaded files will be saved in a `downloads` folder in the same directory as the script.

## Notes

- For MP3 downloads, only audio will be downloaded
- The application automatically creates a `downloads` folder if it doesn't exist
- Downloads are performed in a separate thread to keep the GUI responsive
- Progress is shown in real-time using the progress bar
