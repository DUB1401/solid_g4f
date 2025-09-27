import logging

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
	filename = "logs.log",
	encoding = "utf-8",
	level = logging.INFO,
	format = "%(asctime)s %(levelname)s: %(message)s",
	datefmt = "%Y-%m-%d %H:%M:%S"
)