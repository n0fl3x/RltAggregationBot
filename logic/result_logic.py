from datetime import datetime

from pandas import date_range, DataFrame


def create_timestamps_list(
        start_dt: str,
        end_dt: str,
        frequency: str,
) -> list[str]:
    datetime_range = date_range(
        start=start_dt,
        end=end_dt,
        freq=frequency,
    )
    return [str(timestamp) for timestamp in datetime_range]


async def create_result_dict(
        timestamps_list: list[str],
        collection: list,
) -> dict[str, list[str | int]]:
    dataframe = DataFrame(data=list(collection))
    result_dict = {}
    for ts in timestamps_list:
        dt_item = datetime.fromisoformat(ts)
        if dt_item not in dataframe.to_numpy():
            result_dict[dt_item.isoformat()] = 0
        else:
            result_dict[dt_item.isoformat()] = dataframe.loc[dataframe["_id"] == dt_item, "total"].iloc[0]
    return {
        "dataset": [val for val in result_dict.values()],
        "labels": [dt for dt in result_dict.keys()],
    }
