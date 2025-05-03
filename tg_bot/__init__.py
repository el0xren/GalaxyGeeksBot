__version__ = "1.0.0"
from dotenv import load_dotenv
import os
from pathlib import Path

bot_path = Path(__file__).parent
modules_path = bot_path / "modules"
config_path = Path("galaxygeeksbot") / "config.env"

if config_path.exists():
    load_dotenv(str(config_path))
else:
    load_dotenv("config.env")


def get_config(key, default=None):
    value = os.environ.get(key, default)
    print(f"Loaded {key}: {value}")
    return value


print(f"Config path: {config_path}")
print(f"Config file exists: {config_path.exists()}")
