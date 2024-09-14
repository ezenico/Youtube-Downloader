#%% 
from pytubefix import YouTube
from tkinter import messagebox, ttk, scrolledtext, filedialog, Frame
# import tkinter as tb
import ttkbootstrap as tb
from PIL import Image
import threading
import os
import re
import queue
from moviepy.editor import VideoFileClip
import ffmpeg


# Create a queue to handle communication between threads
message_queue = queue.Queue()
wrong_url_flag = False  # Initialize the flag to track wrong URLs

def sanitize_filename(filename):
    """Replace invalid characters in a filename with underscores."""
    return re.sub(r'[\/:*?"<>|]', '_', filename)

def schedule_check(t):
    """Schedule the execution of the `check_if_done()` function within one second."""
    window.after(100, check_if_done, t)

def check_if_done(t):
    """Check if the download thread has finished and update the UI accordingly."""
    global wrong_url_flag
    if not t.is_alive():
        download_button["state"] = "normal"
        download_entry_button["state"] = "normal"
        # convert_button["state"] = "normal"
        entry["state"] = "normal"
        if not wrong_url_flag:
            output_text.config(text="Process complete!")
        else:
            output_text.config(text="There was an error with a URL. Please check the logs")
            wrong_url_flag = False
        progress_bar.grid_forget()
    else:
        schedule_check(t)

def on_progress_callback(stream, chunk, bytes_remaining):
    """Update the progress bar based on the download progress."""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    message_queue.put(percentage)

def download_video(video_url):
    """Download a video from YouTube given its URL."""
    global wrong_url_flag
    try:
        yt = YouTube(video_url, on_progress_callback=on_progress_callback)
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path="videos")
        message_queue.put(f"Successfully downloaded {yt.title}")
    except OSError:
        filename = sanitize_filename(yt.title)
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path="videos", filename=filename + ".mp4")
        message_queue.put(f"Successfully downloaded {yt.title}")
    except Exception as e:
        wrong_url_flag = True
        message_queue.put(f"Error downloading video from {video_url}: {e}")

def read_urls_from_file():
    """Read URLs from a text file and download each video."""
    global wrong_url_flag
    try:
        with open(f'{file_path}', 'r') as file:
            content = file.read()
        urls = [url.strip() for url in content.split(',')]
        for url in urls:
            download_video(url)
    except Exception as e:
        wrong_url_flag = True
        message_queue.put(f"Error reading {file_path.split('/')[-1]}: {e}")
    except NameError:
        message_queue.put(f"Please select a file")

def start_entry_download():
    """Start the download process for a single video URL entered by the user."""
    global wrong_url_flag
    wrong_url_flag = False
    output_text.grid(row=6, column=1, columnspan=2, padx=10, pady=10)
    if entry.get():
        download_button["state"] = "disabled"
        download_entry_button["state"] = "disabled"
        # convert_button["state"] = "disabled"
        entry["state"] = "disabled"
        progress_bar.grid(row=7, column=1, columnspan=2, padx=10, pady=10)
        output_text.config(text="Downloading!")
        t2 = threading.Thread(target=download_video, args=(entry.get(),))
        t2.start()
        schedule_check(t2)
    else:
        output_text.config(text="Please enter a Youtube URL")


def start_file_download():
    """Start the download process for multiple video URLs from a file."""
    global wrong_url_flag
    wrong_url_flag = False
    output_text.grid(row=6, column=1, columnspan=2, padx=10, pady=10)

    try:
        # Check if file_path exists
        file_path

        download_button["state"] = "disabled"
        download_entry_button["state"] = "disabled"
        # convert_button["state"] = "disabled"
        entry["state"] = "disabled"
        progress_bar.grid(row=7, column=1, columnspan=2, padx=10, pady=10)
        output_text.config(text="Downloading!")
        t = threading.Thread(target=read_urls_from_file)
        t.start()
        schedule_check(t)
    except NameError:
        output_text.config(text="The input value is empty!")
    
        


def convert_to_avi(filename):
    """Convert a downloaded MP4 video to AVI format."""
    try:
        input_path = os.path.join("videos", f"{filename}.mp4")
        output_path = os.path.join("converted_videos", f"{filename}.avi")
        clip = VideoFileClip(input_path)
        # clip.write_videofile(output_path, codec='png')
        clip.write_videofile(output_path)
        message_queue.put(f"Successfully converted {filename} to AVI")
    except Exception as e:
        message_queue.put(f"Error converting {filename} to AVI: {e}")

def convert_all_to_avi():
    """Convert all MP4 videos in the 'videos' folder to AVI format."""
    try:
        os.makedirs('converted_videos', exist_ok=True)
        for filename in os.listdir('videos'):
            if filename.endswith('.mp4'):
                convert_to_avi(filename.rsplit('.', 1)[0])
    except Exception as e:
        message_queue.put(f"Error converting videos: {e}")

def start_conversion():
    """Start the conversion process for all MP4 videos to AVI."""
    output_text.grid(row=6, column=1, columnspan=2, padx=10, pady=10)
    download_button["state"] = "disabled"
    download_entry_button["state"] = "disabled"
    # convert_button["state"] = "disabled"
    entry["state"] = "disabled"
    progress_bar.grid(row=7, column=1, columnspan=2, padx=10, pady=10)
    output_text.config(text="Converting!")
    t = threading.Thread(target=convert_all_to_avi)
    t.start()
    schedule_check(t)

def open_file():
    global file_path
    file_path = filedialog.askopenfilename(
        title="Select a Text File", filetypes=[("Text files", "*.txt")])
    if file_path:
            text_widget.config(state=tb.NORMAL)
            text_widget.delete(0, tb.END)  # Clear previous content
            text_widget.insert(0,file_path)
            # text_widget.config(state=tb.DISABLED)

def process_message_queue():
    """Process messages from the queue and update the UI."""
    while not message_queue.empty():
        message = message_queue.get_nowait()
        if isinstance(message, str):
            log_message(message)
        elif isinstance(message, float):
            progress_bar['value'] = message
    window.after(100, process_message_queue)

def log_message(message):
    """Log a message to the logs box."""
    logs_box.config(state=tb.NORMAL)
    logs_box.insert(tb.END, message + '\n')
    logs_box.yview(tb.END)
    logs_box.config(state=tb.DISABLED)

def create_gui():
    """Create and display the GUI."""
    global window, output_text, download_button, progress_bar, logs_box, download_entry_button
    global convert_button, entry, entryurl, wrong_url_flag, text_widget, open_button, file_path

    window = tb.Window(themename='darkly')
    window.title("YouTube Video Downloader")
    
    # Simplified row and column configuration
    for i in range(3):
        window.columnconfigure(i, weight=1)
    for i in range(6):
        window.rowconfigure(i, weight=1)

    # Load and set the icon for the window
    icon_path = 'images/youtube_logo.png'
    if os.path.exists(icon_path):
        img = Image.open(icon_path)
        img.save('images/youtube_logo.ico', format='ICO')
        window.iconbitmap('images/youtube_logo.ico')
    
    # style = ttk.Style()
    # style.configure('TButton', font=('Helvetica', 12), padding=10, borderwidth=0)
    # style.configure('TLabel', background='#282828', foreground='#FFFFFF', font=('Helvetica', 12))
    # style.configure('Header.TLabel', background='#282828', foreground='#FFFFFF', font=('Helvetica', 14))
    # style.configure('TProgressbar', thickness=20, troughcolor='#404040', background='#1DB954')
    
    # Create a Text widget to display the content
    text_widget = tb.Entry(window, state="readonly")
    text_widget.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

    # Create a button to open the file
    open_button = tb.Button(window, text="Select a file", command=open_file)
    open_button.grid(row=0, column=2, padx=10, pady=10, sticky='we')
    
    # Button for multiple URLs download
    download_button = tb.Button(window, text="Download videos using a txt file", command=start_file_download)
    download_button.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
    
    # Label for single URL download
    # single_url_label = tb.Label(window, text="Enter a URL to download a single video", style='Header.TLabel')
    single_url_label = tb.Label(window, text="Enter a URL to download a single video")
    single_url_label.grid(row=2, column=1, columnspan=2, padx=10, pady=10)
    
    # Entry for single URL
    entryurl = tb.StringVar()
    entry = tb.Entry(window, textvariable=entryurl, width=50)
    entry.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky='ew')
    
    # Button for single URL download
    # download_entry_button = tb.Button(window, text="Download video", command=start_entry_download, style='TButton')
    download_entry_button = tb.Button(window, text="Download video", command=start_entry_download)
    download_entry_button.grid(row=4, column=1, columnspan=2, padx=10, pady=10)
    
    # ScrolledText for logs
    logs_box = scrolledtext.ScrolledText(window, height=10, state=tb.DISABLED, bg='#404040', fg='#FFFFFF', font=('Helvetica', 10))
    logs_box.grid(row=5, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')
    
    # Progress bar
    # progress_bar = tb.Progressbar(window, orient="horizontal", mode="determinate", style='TProgressbar')
    progress_bar = tb.Progressbar(window, orient="horizontal", mode="determinate")

    
    # Label for output text
    # output_text = tb.Label(window, style='TLabel')
    output_text = tb.Label(window)


    # Schedule the message queue processing
    process_message_queue()
    
    window.mainloop()

if __name__ == "__main__":
    create_gui()