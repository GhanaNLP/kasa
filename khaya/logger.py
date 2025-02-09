import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("khaya")
logger.setLevel(logging.DEBUG)

# add a console handler if none exists
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)
