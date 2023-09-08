from typing import Optional
import traceback

# Initialize classes from lyrics_dl/providers
import lyrics_dl.providers
from lyrics_dl.core import Song
from lyrics_dl.registry import Registry
from lyrics_dl.config import LyricsDlConfig
from lyrics_dl.logger import DefaultLogger, AbstractLogger


class LyricsDl:
    logger: AbstractLogger

    def __init__(self, config: LyricsDlConfig = LyricsDlConfig(), logger: AbstractLogger = DefaultLogger()):
        self.logger = logger

        providers_classes = Registry.get_synced_providers()

        self.providers = []

        for name in config.order:
            Provider = providers_classes[name]
            provider_config = config.providers_configs.get(name)

            if not provider_config:
                provider_config = {}

            try:
                provider = Provider(**provider_config)
            except TypeError as e:
                self.logger.error(f"[lyrics-dl] {e}")
                continue

            self.providers.append(provider)

    def fetch_lyrics(self, song: Song) -> Optional[str]:
        self.logger.info(f"[lyrics-dl] Fetching lyrics for \"{song.artist} - {song.title}\"")
        for provider in self.providers:
            self.logger.info(f"[{provider.name}] Fetching lyrics...")

            try:
                lyrics = provider.fetch_lyrics(song)
            except Exception as e:
                lyrics = None
                self.logger.error(f"[{provider.name}] Got exception while fetching lyrics! ({type(e).__name__}: {e})")
                self.logger.debug(f"[{provider.name}] {traceback.format_exc()}")

            if lyrics:
                self.logger.info(f"[{provider.name}] Found lyrics!")
                return lyrics

            self.logger.info(f"[{provider.name}] No lyrics was found!")

        return None
