import re
import tkinter as tk
from tkinter import ttk, messagebox
import yt_dlp
import threading

def clean_ansi_codes(text):
    """Remove ANSI escape sequences from a string."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def on_progress(d):
    if d['status'] == 'downloading':
        # Clean the percentage string before conversion
        percent_str = clean_ansi_codes(d['_percent_str'])
        try:
            percent = float(percent_str.strip().replace('%', ''))
            progress["value"] = percent
            root.update_idletasks()
        except ValueError:
            pass  

def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return

    ydl_opts = {
        'format': f'bestvideo[height<={res_var.get().replace("p","")}]+bestaudio/best',
        'progress_hooks': [on_progress],
        'quiet': True,  # Reduces console output
        'no_warnings': True,  # Suppress warnings
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Download completed!")
    except Exception as e:
        messagebox.showerror("Error", f"Download failed: {str(e)}")
    finally:
        progress["value"] = 0

def start_download_thread():
    thread = threading.Thread(target=download_video, daemon=True)
    thread.start()

# --- GUI Setup ---
root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("500x300")
root.resizable(False, False)

# URL Input
url_label = tk.Label(root, text="Enter Video URL:")
url_label.pack(pady=(10, 0))

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Resolution Dropdown
res_label = tk.Label(root, text="Resolution:")
res_label.pack(pady=(10, 0))

res_var = tk.StringVar(value="720p")
res_options = ttk.Combobox(root, textvariable=res_var, values=["144p", "240p", "360p", "480p", "720p", "1080p"])
res_options.pack(pady=5)

# Progress Bar
progress = ttk.Progressbar(root, length=400, mode='determinate')
progress.pack(pady=(10, 5))

# Download Button
download_button = tk.Button(root, text="Download Video", command=start_download_thread)
download_button.pack(pady=10)

root.mainloop()