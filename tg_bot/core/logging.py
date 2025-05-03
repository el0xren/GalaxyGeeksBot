from logging import (
    basicConfig,
    debug,
    info,
    error,
    warning,
    INFO,
    FileHandler,
    StreamHandler,
)
from pathlib import Path

# Ensure log directory exists
log_file = Path("log.txt")
log_file.parent.mkdir(exist_ok=True)

# Configure logging
basicConfig(
    format=
    "[%(asctime)s] [%(filename)s:%(lineno)s %(levelname)s] %(funcName)s: %(message)s",
    handlers=[FileHandler(log_file), StreamHandler()],
    level=INFO,
)

# Convenience logging functions
LOGD = debug
LOGI = info
LOGE = error
LOGW = warning
