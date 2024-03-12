from typing import Any
from datetime import datetime

from logic.exceptions import ValidationError
from logic.enums import EnumDataKeys, EnumGroupTypes


def validate_tg_msg_type(
        tg_msg: Any,
) -> Any:
    if type(tg_msg) is not dict:
        raise ValidationError("Valid decoded data can be dictionary type only")
    return tg_msg


def validate_msg_dict(
        msg_dict: dict,
) -> dict:
    if (len(d_keys := msg_dict.keys())) < len(EnumDataKeys):
        raise ValidationError("Not enough input data parameters")
    if not set(d_keys).issubset(set(EnumDataKeys)):
        raise ValidationError("Invalid input data key(-s)")
    if msg_dict.get(EnumDataKeys.group_type) not in [key.name for key in EnumGroupTypes]:
        raise ValidationError("Invalid 'group_type' value")
    return msg_dict


def validate_msg_dict_datetimes(
        msg_dict: dict,
) -> dict:
    start_dt = msg_dict.get(EnumDataKeys.dt_from)
    end_dt = msg_dict.get(EnumDataKeys.dt_upto)
    if datetime.fromisoformat(start_dt) > datetime.fromisoformat(end_dt):  # ValueError
        raise ValidationError("Parameter 'dt_from' can not be greater than 'dt_upto'")
    return msg_dict
