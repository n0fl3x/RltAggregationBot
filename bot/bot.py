import asyncio
import json

from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ContentType
from aiogram.methods import DeleteWebhook
from aiogram.exceptions import AiogramError

from bot_config import (
    bot,
    disp,
    COMMANDS,
)
from bot_text_data import (
    START_HELP_TEXT,
    NON_TEXT_MSG,
    JSON_DECODE_AND_VALIDATION_ERROR,
    MSG_TOO_LONG,
)
from logic.validators import (
    validate_msg_dict,
    validate_tg_msg_type,
    validate_msg_dict_datetimes,
)
from logic.exceptions import ValidationError
from logic.result_logic import create_timestamps_list, create_result_dict
from logic.enums import EnumDataKeys, EnumGroupTypes
from db.aggregation import create_aggregation_pipeline, aggregate_collection
from db.db_config import start_collection
from filters import NonTextTypeFilter


@disp.message(Command(*COMMANDS))
async def start_and_help_commands_handler(message: Message):
    await message.answer(text=START_HELP_TEXT)


@disp.message(NonTextTypeFilter(msg_type=ContentType.TEXT))
async def non_text_messages_handler(message: Message):
    await message.answer(text=NON_TEXT_MSG)


@disp.message()
async def send_result_message(message: Message):
    if len(message.text) > 4096:
        await message.answer(text=MSG_TOO_LONG)

    try:
        decoded = json.loads(message.text)
    except json.decoder.JSONDecodeError as dc_er:
        await message.answer(text=JSON_DECODE_AND_VALIDATION_ERROR + str(dc_er))
    else:
        try:
            validated_type = validate_tg_msg_type(decoded)
            validated_dict = validate_msg_dict(validated_type)
            validated_data = validate_msg_dict_datetimes(validated_dict)
        except ValueError as val_er:
            await message.answer(text=JSON_DECODE_AND_VALIDATION_ERROR + str(val_er))
        except ValidationError as vld_er:
            await message.answer(text=JSON_DECODE_AND_VALIDATION_ERROR + str(vld_er))
        else:
            start = validated_data[EnumDataKeys.dt_from.value]
            end = validated_data[EnumDataKeys.dt_upto.value]
            group_type = validated_data[EnumDataKeys.group_type.value]
            frequency = EnumGroupTypes[group_type].value
            ts_list = create_timestamps_list(
                start_dt=start,
                end_dt=end,
                frequency=frequency,
            )
            ag_pl = create_aggregation_pipeline(
                dt_from=start,
                dt_upto=end,
                group_type=group_type,
            )
            ag_col = await aggregate_collection(
                collection=start_collection,
                pipeline=ag_pl,
            )
            res = await create_result_dict(
                timestamps_list=ts_list,
                collection=ag_col,
            )

            str_res = str(res)
            if len(str_res) < 4096:
                await message.answer(text=str_res.replace("'", "\""))
            else:
                for piece in range(0, len(str_res), 4096):
                    try:
                        await bot.send_message(
                            chat_id=message.chat.id,
                            text=str_res[piece: piece + 4096].replace("'", "\""),
                        )
                    except AiogramError as aiogr_er:
                        bot.send_message(
                            chat_id=message.chat.id,
                            text=str(aiogr_er),
                        )


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await disp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
