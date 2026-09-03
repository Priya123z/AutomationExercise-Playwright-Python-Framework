from loguru import logger
from utils.artifact_manager import artifact

logger.remove()

logger.add(
    artifact.logs_dir / "framework.log",
    rotation="10 MB",
    retention="10 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)