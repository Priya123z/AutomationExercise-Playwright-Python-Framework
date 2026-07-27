from loguru import logger
import os
from utils.artifact_manager import artifact

os.makedirs("logs", exist_ok=True)

logger.remove()

logger.add(
    artifact.logs_dir / "framework.log",
    rotation="10 MB",
    retention="10 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)