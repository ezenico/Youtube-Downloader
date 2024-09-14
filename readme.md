# YouTube Video Downloader and Converter

## Description

This program is a desktop application developed with Python and Tkinter that allows you to download YouTube videos and convert them to different formats. The main functionality includes downloading videos via individual URLs or from a text file and converting downloaded videos from MP4 to AVI.

## Motivation

The creation of this program arose from the need to have a simple and efficient tool for downloading and converting YouTube videos. My father wanted to download YouTube videos, but online tools have download limits and some might not be trustworthy. This program ensures a reliable and unlimited way to download and convert videos.

## Features

### Download YouTube Videos

1. **Download by URL**: Allows the user to enter a YouTube URL to download a specific video.
2. **Download from File**: Allows the user to download multiple videos specified in a text file (`videos.txt`).

### Video Conversion

1. **Convert MP4 to AVI**: Once downloaded, the MP4 videos can be converted to AVI with a button in the interface. Currently disabled because I have not been able to convert mp4 files to avi, nor am I sure if that is what my father is looking for. Also, there is a lot more information on converting from avi to mp4 than vice versa, which makes me doubt that the media player my father uses only supports avi.

### User Interface

1. **Progress Bar**: Displays the download progress in real-time.
2. **Logs Box**: Records messages and errors during the download and conversion process, providing the user with information about the operations' status.
3. **Modern Design**: Uses custom styles to enhance the user experience with a modern and attractive interface.

## Requirements

- Python 3.6 or higher
- Tkinter
- Pytube
- MoviePy
- FFMPEG
- ttkbootstrap

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/your-repository.git
    ```
2. Navigate to the project directory:
    ```bash
    cd your-repository
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the program**:
    ```bash
    python main.py
    ```
2. **Download videos**:
   - Enter a YouTube URL and click "Download video" to download a single video.
   - Place URLs in `videos.txt`, separated by commas, and click "Download videos using a txt file" to download multiple videos.

3. **Convert videos to AVI**:
   - Click the "Convert to AVI" button to convert downloaded MP4 videos to AVI and save them in the `converted_videos` folder.

## Creating the Executable

To create an executable (.exe) file for Windows:

1. Install PyInstaller:
    ```bash
    pip install pyinstaller
    ```
2. Create the .spec file with the command:
    ```bash
    pyi-makespec --onefile your_script.py
    ```
3. Modify the .spec file to include the application icon:
    ```python
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='YouTubeDownloader',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=True,
        icon='images/youtube_logo.ico'
    )
    ```
4. Compile the executable:
    ```bash
    pyinstaller your_script.spec
    ```

This will generate an executable file in the `dist` folder that can be distributed and run on Windows systems.

## Contributions

Contributions are welcome. Please open an issue or a pull request for any improvements or corrections.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
