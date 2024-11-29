import os
import time
import yt_dlp 
from rich.console import Console 
from rich.table import Table 
from rich.panel import Panel 
from rich.progress import track 

console = Console()

# Function to show download progress


def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d['_percent_str'].strip()
        speed = d['_speed_str']
        eta = d['_eta_str']
        console.print(f"[blue]Downloading... {percent} at {speed} (ETA: {eta})[/blue]", end='\r')

# Function to get video information


def get_video_info(url):
    console.print("\n[bold green]Fetching video information...[/bold green]")
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    table = Table(title="[bold cyan]Video Information[/bold cyan]")
    table.add_column("Attribute", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    table.add_row("Title", info.get("title", "N/A"))
    table.add_row("Uploader", info.get("uploader", "N/A"))
    table.add_row("Duration", f"{info.get('duration', 0) // 60} min {info.get('duration', 0) % 60} sec")
    table.add_row("Views", str(info.get("view_count", "N/A")))
    table.add_row("Likes", str(info.get("like_count", "N/A")))
    table.add_row("URL", url)
    console.print(table)

# Function to download video/audio


def download_content(url, format_choice, quality=None, output_path=None):
    ydl_opts = {
        "progress_hooks": [progress_hook],
        "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s") if output_path else "%(title)s.%(ext)s"
    }

    if format_choice == "audio":
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192", }]
        })
    elif format_choice == "video":ydl_opts.update({"format": f"bestvideo[height<={quality}]+bestaudio/best" if quality else "bestvideo+bestaudio"})

    console.print(f"[bold yellow]Starting download as {format_choice}...[/bold yellow]")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    console.print(
        f"[bold green]{format_choice.capitalize()} download completed![/bold green]")

# Main menu


def main_menu():
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()
        handle_choice(choice)


def display_menu():
    menu_panel = Panel.fit(
        "[bold cyan]1. Download Video\n"
        "2. Download Audio\n"
        "3. Exit[/bold cyan]",
        title="[bold yellow]Main Menu[/bold yellow]",
        border_style="bright_magenta"
    )
    console.print(menu_panel)


def handle_choice(choice):
    if choice in ["1", "2"]:
        url = input("Enter YouTube URL: ").strip()
        get_video_info(url)
        format_choice = "video" if choice == "1" else "audio"
        quality = get_quality(format_choice)
        output_path = get_output_path()
        download_content(url, format_choice, quality, output_path)
    elif choice == "3":
        console.print("[bold green]Exiting program. Have a great day![/bold green]")
        exit()
    else:
        console.print("[bold red]Invalid choice. Please try again![/bold red]")


def get_quality(format_choice):
    if format_choice == "video":
        console.print("Select video quality:")
        console.print("1. 1080p\n2. 720p\n3. 480p\n4. Best available")
        quality_choice = input("Enter your choice (1-4): ").strip()
        quality_map = {"1": "1080", "2": "720", "3": "480", "4": None}
        return quality_map.get(quality_choice, None)
    return None


def get_output_path():
    output_path = input("Enter download path (or press Enter to use the current directory): ").strip()
    if not output_path:
        output_path = os.getcwd()
    elif not os.path.exists(output_path):
        os.makedirs(output_path)
    return output_path

# Show animated setup


def show_animated_setup():
    steps = ["Initializing...", "Preparing interface...",
             "Loading modules...", "Setup complete!"]
    for _ in track(steps, description="Setting up...", style="green"):
        time.sleep(1)


# Entry point
if __name__ == "__main__":
    console.clear()
    console.print(Panel.fit(
        "[bold white on blue] YOUTUBE DOWNLOADER [/bold white on blue]",
        title="[bold green]Welcome![/bold green]",
        border_style="bright_yellow",
    ))
    show_animated_setup()
    main_menu()

