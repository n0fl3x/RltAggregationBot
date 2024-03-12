from enum import Enum


class EnumDataKeys(str, Enum):
    dt_from = "dt_from"
    dt_upto = "dt_upto"
    group_type = "group_type"


class EnumGroupTypes(str, Enum):
    hour = "h"
    day = "D"
    month = "MS"
    year = "YS"
