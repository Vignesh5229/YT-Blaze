import yt_dlp
import os
import threading
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.live import Live
from rich.markdown import Markdown
from rich.style import Style
from rich.box import ROUNDED
import shutil

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

console = Console()

def animated_banner():
    banner = """
[bold purple]_____.___.___________     __________.__                        [/bold purple]
[bold cyan]\__  |   |\__    ___/     \______   \  | _____  ________ ____  [/bold cyan]
[bold green] /   |   |  |    |  ______ |    |  _/  | \__  \ \___   // __ \ [/bold green]
[bold yellow] \____   |  |    | /_____/ |    |   \  |__/ __ \_/    /\  ___/ [/bold yellow]
[bold red] / ______|  |____|         |______  /____(____  /_____ \\___  >[/bold red]
[bold magenta] \/                               \/          \/      \/    \/ [/bold magenta]
[bold blue] YT-Blaze 🔥 (Fast & powerful YouTube downloader)[/bold blue]
"""
    console.print(banner)

def download_video(url, format_choice, resolution_choice, custom_path=None):
    # Set the output path
    output_path = custom_path if custom_path else "downloads"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    ydl_opts = {
        'progress_hooks': [progress_hook],
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    
    if format_choice == 'mp3':
        quality = Prompt.ask("🎵 Choose audio quality", choices=["low", "medium", "high"])
        quality_map = {"low": "64", "medium": "128", "high": "192"}
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality_map[quality],
            }],
        })
    else:
        ydl_opts.update({'format': f'bestvideo[height<={resolution_choice}]+bestaudio/best'})
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    console.print(f"✅ [bold green]Download complete! Saved in: {output_path}[/bold green]")

def progress_hook(d):
    if d['status'] == 'downloading':
        console.print(f"⏳ [bold yellow]Downloading:[/bold yellow] {d['_percent_str']} - {d['_eta_str']} remaining", end='\r')
    elif d['status'] == 'finished':
        console.print("✅ [bold green]Download complete. Processing...[/bold green]")

def batch_download(file_path, format_choice, resolution_choice, custom_path=None):
    if not os.path.exists(file_path):
        console.print("❌ [bold red]File not found![/bold red]")
        return
    
    with open(file_path, 'r') as f:
        urls = f.read().splitlines()
    
    threads = []
    for url in urls:
        thread = threading.Thread(target=download_video, args=(url, format_choice, resolution_choice, custom_path))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

def display_dashboard():
    table = Table(title="🚀 Download Options", border_style="bold magenta", box=ROUNDED)
    table.add_column("🔹 Option", justify="left", style="cyan", no_wrap=True)
    table.add_column("📌 Description", style="magenta")
    
    table.add_row("🎥 Single Download", "Download a single video with format and resolution choice")
    table.add_row("📂 Batch Download", "Download multiple videos from a list file")
    table.add_row("🎵 MP3 Format", "Download audio-only version of a video with quality selection")
    table.add_row("📺 Resolution Selection", "Choose video resolution (1080p, 720p, etc.)")
    table.add_row("📂 Custom Download Path", "Choose a custom directory to save downloads")
    table.add_row("📊 Progress Tracking", "Displays clean and enhanced progress updates dynamically")
    
    console.print(table)

def main():
    clear_screen()
    animated_banner()
    console.print(Panel.fit("Welcome to YT-Blaze 🔥 - Your Fast & Powerful YouTube Downloader", style="bold blue"))
    display_dashboard()
    
    choice = Prompt.ask("⚡ Choose an option", choices=["single", "batch"])
    
    # Ask for custom download path
    custom_path = Prompt.ask("📂 Enter custom download path (leave blank for default 'downloads' folder)", default="downloads")
    
    if choice == "single":
        url = Prompt.ask("🔗 Enter video URL")
        format_choice = Prompt.ask("🎬 Choose format", choices=["mp3", "mp4", "webm"])
        if format_choice != "mp3":
            resolution_choice = Prompt.ask("📺 Choose resolution (e.g., 1080, 720, 480)")
        else:
            resolution_choice = ""
        download_video(url, format_choice, resolution_choice, custom_path)
    
    elif choice == "batch":
        file_path = Prompt.ask("📂 Enter batch file path")
        format_choice = Prompt.ask("🎬 Choose format", choices=["mp3", "mp4", "webm"])
        if format_choice != "mp3":
            resolution_choice = Prompt.ask("📺 Choose resolution (e.g., 1080, 720, 480)")
        else:
            resolution_choice = ""
        batch_download(file_path, format_choice, resolution_choice, custom_path)
    
    console.print(Panel.fit("Thank you for using YT-Blaze 🔥", style="bold green"))

if __name__ == "__main__":
    main()