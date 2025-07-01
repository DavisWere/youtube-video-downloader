# 🎥 YouTube Video Downloader (Tkinter + yt-dlp)

A simple, fast, and modern desktop YouTube video downloader built with **Python**, **Tkinter**, and **yt-dlp**. It allows you to select video resolution, choose your download directory, and monitor download progress via a progress bar — all in a clean and responsive GUI.

---

## 🚀 Features

- Download any public YouTube video
- Select resolution (144p to 1080p)
- Choose custom download folder
- View real-time progress bar
- Fast and reliable with `yt-dlp`
- Built as a standalone desktop app (no Python needed after packaging)

---

## 📦 Installation

### 1. Clone the repository

```bash
git https://github.com/DavisWere/youtube-video-downloader.git
cd youtube-video-downloader
```

### 2. Install Dependencies

Python 3.8+ is required

🔹 Windows

```bash
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

🔹 Linux / macOS

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### 🧪 Running the App (During Development)

```bash
python youtube_downloader.py
```

### 🖥️ Running the Standalone App

dist/youtube_downloader/

Windows: Double-click youtube_downloader.exe

Linux/macOS: Run ./youtube_downloader

✅ No Python or terminal needed — just click and run!

### ⚠️ Notes

Make sure ffmpeg is installed on your system or bundled alongside the app (needed for merging video and audio).

Install on Linux:

```bash
sudo apt install ffmpeg
```

Install on macOS:

```bash
brew install ffmpeg
```

Install on Windows:
Download from https://ffmpeg.org/download.html and add to PATH.

### 📁 Folder Structure

```bash
youtube-video-downloader/
├── youtube_downloader.py
├── youtube_downloader.spec
├── icon.ico
├── dist/
│   └── youtube_downloader/ (standalone app output)
└── requirements.txt
```
