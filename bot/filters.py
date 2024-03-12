from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.enums import ContentType


class NonTextTypeFilter(BaseFilter):
    def __init__(self, msg_type: ContentType):
        self.msg_type = msg_type

    async def __call__(self, msg: Message):
        return msg.content_type != ContentType.TEXT
