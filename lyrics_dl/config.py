from typing import Self
import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class LyricsDlConfig:
    order: list[str] = field(default_factory=lambda: ["kugou", "youtube"])
    providers_configs: dict[str, dict] = field(default_factory=lambda: {})

    @classmethod
    def from_file(cls, path: Path) -> Self:
        with open(path, "rb") as f:
            config = tomllib.load(f)

        return cls(
            order=config["providers"].pop("order"),
            providers_configs=config["providers"],
        )
