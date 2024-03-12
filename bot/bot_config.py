import os
import logging

from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher


load_dotenv(find_dotenv())

COMMANDS = [
    "start",
    "help",
]

logging.basicConfig(
    level=logging.INFO,
    # filename="logs.log",
)

bot = Bot(token=os.getenv("BOT_TOKEN"))
disp = Dispatcher()
