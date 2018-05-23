from logging import getLogger

from .config import Config

logger = getLogger(__name__)


def start():
    config_type = "normal"

    config = Config(config_type=config_type)

    logger.info(f"config type: {config_type}")

    from .play_game import gui
    return gui.start(config)
