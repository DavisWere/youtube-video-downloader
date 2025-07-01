import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yt_dlp
import threading
import re
import os
from pathlib import Path
from itertools import cycle

# Initialize with Downloads directory as default
DEFAULT_DOWNLOAD_DIR = str(Path.home() / "Downloads")
DOWNLOAD_ACTIVE = False
CANCEL_REQUESTED = False
SPINNER_FRAMES = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
spinner = cycle(SPINNER_FRAMES)

def update_spinner():
    if DOWNLOAD_ACTIVE:
        spinner_label.config(text=next(spinner))
        window.after(100, update_spinner)

def clean_ansi_codes(text):
    """Remove ANSI escape sequences from a string."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def on_progress(d):
    if d['status'] == 'downloading' and not CANCEL_REQUESTED:
        percent_str = clean_ansi_codes(d['_percent_str'])
        try:
            percent = float(percent_str.strip().replace('%', ''))
            progress_bar["value"] = percent
        except ValueError:
            pass
        
        if '_speed_str' in d and '_eta_str' in d:
            speed = clean_ansi_codes(d['_speed_str'])
            eta = clean_ansi_codes(d['_eta_str'])
            status_label.config(text=f"Downloading... {speed} | ETA: {eta}")
        
        window.update_idletasks()

def toggle_controls(state):
    """Enable/disable controls during download"""
    for widget in [url_entry, resolution_dropdown, directory_button]:
        widget.config(state=state)

def select_directory():
    """Open a dialog to select download directory."""
    directory = filedialog.askdirectory(initialdir=DEFAULT_DOWNLOAD_DIR)
    if directory:
        download_path.set(directory)
        directory_label.config(text=f"Download Location: {directory}")

def cancel_download():
    global CANCEL_REQUESTED
    CANCEL_REQUESTED = True
    status_label.config(text="Cancelling...", fg="orange")
    cancel_button.config(state='disabled')  # Disable cancel button after clicking

def download_video():
    global DOWNLOAD_ACTIVE, CANCEL_REQUESTED
    DOWNLOAD_ACTIVE = True
    CANCEL_REQUESTED = False
    
    # UI changes for download start
    toggle_controls('disabled')
    download_button.pack_forget()
    cancel_button.config(state='normal')  # Enable cancel button
    cancel_button.pack(side=tk.LEFT, padx=5)
    status_label.config(text="Preparing download...", fg="blue")
    status_label.pack(pady=5)
    update_spinner()
    
    url = url_entry.get()
    download_dir = download_path.get()

    ydl_opts = {
        'format': f'bestvideo[height<={resolution_var.get().replace("p","")}]+bestaudio/best',
        'progress_hooks': [on_progress],
        'quiet': True,
        'no_warnings': True,
        'outtmpl': os.path.join(download_dir, '%(title)s.mp4'),
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if CANCEL_REQUESTED:
            messagebox.showinfo("Cancelled", "Download was cancelled")
        else:
            messagebox.showinfo("Success", f"Download completed as MP4!\nSaved to: {download_dir}")
    
    except Exception as e:
        if not CANCEL_REQUESTED:
            messagebox.showerror("Error", f"Download failed: {str(e)}")
    
    finally:
        # Reset UI
        DOWNLOAD_ACTIVE = False
        CANCEL_REQUESTED = False
        progress_bar["value"] = 0
        status_label.pack_forget()
        spinner_label.config(text="")
        cancel_button.pack_forget()
        download_button.pack(side=tk.LEFT, padx=5)
        toggle_controls('normal')

def start_download_thread():
    thread = threading.Thread(target=download_video, daemon=True)
    thread.start()

# --- Main Window Setup ---
window = tk.Tk()
window.title("YouTube Video Downloader")
window.geometry("550x400")
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

directory_button = tk.Button(
    directory_frame, 
    text="Change Download Location", 
    command=select_directory
)
directory_button.pack(side=tk.LEFT)

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

# Status and spinner
status_frame = tk.Frame(main_frame)
status_frame.pack(fill=tk.X)

spinner_label = tk.Label(status_frame, text="", font=("Arial", 14))
spinner_label.pack(side=tk.LEFT)

status_label = tk.Label(status_frame, text="", fg="blue")
status_label.pack(side=tk.LEFT, padx=5)

# Buttons
button_frame = tk.Frame(main_frame)
button_frame.pack(pady=10)

download_button = tk.Button(
    button_frame, 
    text="Download Video", 
    command=start_download_thread,
    padx=20,
    pady=5
)
download_button.pack(side=tk.LEFT, padx=5)

cancel_button = tk.Button(
    button_frame,
    text="Cancel Download",
    command=cancel_download,
    padx=20,
    pady=5,
    state='normal'  # Changed from 'disabled' to 'normal'
)

window.mainloop()