import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yt_dlp
import threading
import re
import os
from pathlib import Path

# Initialize with Downloads directory as default
DEFAULT_DOWNLOAD_DIR = str(Path.home() / "Downloads")

def clean_ansi_codes(text):
    """Remove ANSI escape sequences from a string."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def on_progress(d):
    if d['status'] == 'downloading':
        percent_str = clean_ansi_codes(d['_percent_str'])
        try:
            percent = float(percent_str.strip().replace('%', ''))
            progress_bar["value"] = percent
            window.update_idletasks()
        except ValueError:
            pass

def select_directory():
    """Open a dialog to select download directory."""
    directory = filedialog.askdirectory(initialdir=DEFAULT_DOWNLOAD_DIR)
    if directory:
        download_path.set(directory)
        directory_label.config(text=f"Download Location: {directory}")

def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return

    download_dir = download_path.get()
    if not download_dir:
        messagebox.showerror("Error", "Please select a download directory")
        return

    ydl_opts = {
        'format': f'bestvideo[height<={resolution_var.get().replace("p","")}]+bestaudio/best',
        'progress_hooks': [on_progress],
        'quiet': True,
        'no_warnings': True,
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", f"Download completed!\nSaved to: {download_dir}")
    except Exception as e:
        messagebox.showerror("Error", f"Download failed: {str(e)}")
    finally:
        progress_bar["value"] = 0

def start_download_thread():
    thread = threading.Thread(target=download_video, daemon=True)
    thread.start()

# --- Main Window Setup ---
window = tk.Tk()
window.title("YouTube Video Downloader")
window.geometry("500x350")
window.resizable(False, False)

# Download path variable (defaults to Downloads)
download_path = tk.StringVar(value=DEFAULT_DOWNLOAD_DIR)

# Main container frame
main_frame = tk.Frame(window, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# URL Input
tk.Label(main_frame, text="YouTube Video URL:").pack(anchor=tk.W)
url_entry = tk.Entry(main_frame, width=50)
url_entry.pack(pady=(0, 10), fill=tk.X)

# Resolution Selection
tk.Label(main_frame, text="Select Quality:").pack(anchor=tk.W)
resolution_var = tk.StringVar(value="720p")
resolution_dropdown = ttk.Combobox(
    main_frame, 
    textvariable=resolution_var, 
    values=["144p", "240p", "360p", "480p", "720p", "1080p"],
    state="readonly"
)
resolution_dropdown.pack(pady=(0, 10), fill=tk.X)

# Directory Selection
directory_frame = tk.Frame(main_frame)
directory_frame.pack(fill=tk.X, pady=(10, 5))

tk.Button(
    directory_frame, 
    text="Change Download Location", 
    command=select_directory
).pack(side=tk.LEFT)

directory_label = tk.Label(
    directory_frame, 
    text=f"Download Location: {DEFAULT_DOWNLOAD_DIR}",
    wraplength=350,
    anchor=tk.W
)
directory_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

# Progress Bar
progress_bar = ttk.Progressbar(main_frame, length=400, mode='determinate')
progress_bar.pack(pady=(10, 5), fill=tk.X)

# Download Button
download_button = tk.Button(
    main_frame, 
    text="Download Video", 
    command=start_download_thread,
    padx=20,
    pady=5
)
download_button.pack(pady=10)

window.mainloop()