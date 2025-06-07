import logging
import os

os.makedirs("logs",exist_ok=True)

logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler=logging.StreamHandler()
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

info_handler=logging.FileHandler("logs/info.log")
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)

error_handler=logging.FileHandler("logs/error.log")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)



warn_handler=logging.FileHandler("logs/warn.log")
warn_handler.setLevel(logging.WARN)
warn_handler.setFormatter(formatter)



logger.addHandler(info_handler)
logger.addHandler(error_handler)
logger.addHandler(warn_handler)
