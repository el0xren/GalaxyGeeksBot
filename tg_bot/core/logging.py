import logging
from pathlib import Path

# Ensure log directory exists
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "galaxygeeksbot.log"

# Configure logging
logging.basicConfig(
    format="[%(asctime)s] [%(filename)s:%(lineno)s %(levelname)s] %(funcName)s: %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(),
    ],
    level=logging.INFO,
    force=True,  # Ensure this configuration overrides any previous ones
)

# Set levels for noisy loggers
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram.ext").setLevel(logging.WARNING)
logging.getLogger("telegram.bot").setLevel(logging.WARNING)

# Create a logger for the bot
logger = logging.getLogger("GalaxyGeeksBot")

# Convenience logging functions
LOGD = logger.debug
LOGI = logger.info
LOGE = logger.error
LOGW = logger.warning