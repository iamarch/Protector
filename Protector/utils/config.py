"""Protector's Configuration"""

import os
from dataclasses import dataclass
from typing import Union

from dotenv import load_dotenv


__all__ = ["BotConfig"]


@dataclass
class BotConfig:
    """
    Bot configuration
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(self) -> Union[str, int]:
        if os.path.isfile("config.env"):
            load_dotenv("config.env")

        # Core config
        self.api_id = int(os.environ.get("API_ID", 0))
        self.api_hash = os.environ.get("API_HASH")
        self.bot_token = os.environ.get("BOT_TOKEN")
        self.db_uri = os.environ.get("DB_URI")

        # Optional
        self.download_path = os.environ.get("DOWNLOAD_PATH", "./downloads/")
        self.log_channel = int(os.environ.get("LOG_CHANNEL", 0))
        self.spamwatch_api = os.environ.get("SW_API", None)

        # Manager required
        self.owner_id = int(os.environ.get("OWNER_ID", 0))
