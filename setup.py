from setuptools import setup, find_packages

setup(
    name="ytdw",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "yt-dlp",
        "rich",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "ytdw=yt_downloader:main",
        ],
    },
)