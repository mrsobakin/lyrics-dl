import argparse
from pathlib import Path

from lyrics_dl.config import LyricsDlConfig
from lyrics_dl.logger import DefaultLogger
from lyrics_dl import LyricsDl


parser = argparse.ArgumentParser()
parser.add_argument("path", type=Path, help="Path to the song file or directory")
parser.add_argument("-c", "--config", type=Path, help="Config file for lyrics-dl")
parser.add_argument("-e", "--extensions", type=str, help="Music files extensions, separated by a comma. For example: wav,flac,mp3")
parser.add_argument("-f", "--force-override", action="store_true", help="Force override .lrc file, if it already exists")
args = parser.parse_args()


logger = DefaultLogger()

if args.config:
    config = LyricsDlConfig.from_file(args.config)
else:
    config = LyricsDlConfig()

lyrics_dl = LyricsDl(config=config, logger=logger)


if args.path.is_dir():
    if not args.extensions:
        extensions = ["flac", "alac", "mp3", "m4a", "mp4", "aac", "wav", "opus", "ogg"]
    else:
        extensions = args.extensions.split(",")

    lyrics_dl.process_directory(args.path, extensions, args.force_override)
else:
    lyrics_dl.process_file(args.path, args.force_override)
