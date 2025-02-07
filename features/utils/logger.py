import logging

logging.basicConfig(
    filename="reports/test_log.log",  # Log file
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)