import argparse
from pathlib import Path

from lyrics_dl.core import Song
from lyrics_dl.config import LyricsDlConfig
from lyrics_dl.logger import DefaultLogger
from lyrics_dl import LyricsDl


logger = DefaultLogger()
config = LyricsDlConfig()
lyrics_dl = LyricsDl(config=config, logger=logger)


def process_file(path, force=False):
    lyrics_path = path.with_suffix(".lrc")

    if lyrics_path.exists() and not force:
        logger.error("[lyrics-dl] Lyrics file already exists!")
        return

    # TODO handle errors
    try:
        song = Song.from_file(path)
    except Exception as e:
        logger.error(f"[lyrics-dl] {path}: {e}")
        return

    lyrics = lyrics_dl.fetch_lyrics(song)

    if not lyrics:
        logger.error("[lyrics-dl] No lyrics was found!")
        return

    with open(lyrics_path, "w") as f:
        f.write(lyrics)


def process_directory(path, extensions):
    for file_path in path.rglob("*"):
        if file_path.suffix[1:] not in extensions:
            continue

        process_file(file_path)


parser = argparse.ArgumentParser()
parser.add_argument("path", type=Path, help="Path to the song file or directory")
parser.add_argument("-e", "--extensions", type=str, help="Music files extensions, separated by a comma. For example: wav,flac,mp3")
parser.add_argument("-f", "--force-override", action="store_true", help="Force override .lrc file, if it already exists")

args = parser.parse_args()

if args.path.is_dir():
    if not args.extensions:
        extensions = ["flac", "alac", "mp3", "m4a", "mp4", "aac", "wav", "opus", "ogg"]
    else:
        extensions = args.extensions.split(",")

    process_directory(args.path, extensions)
else:
    process_file(args.path)
