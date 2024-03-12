from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorCollection


def create_aggregation_pipeline(
        dt_from: str,
        dt_upto: str,
        group_type: str,
) -> list[dict]:
    aggr_pl = [
        {
            "$match": {
                "dt": {
                    "$gte": datetime.fromisoformat(dt_from),
                    "$lte": datetime.fromisoformat(dt_upto),
                },
            },
        },
        {
            "$project": {
                "_id": 1,
                "truncated_datetime": {
                    "$dateTrunc": {
                        "date": "$dt",
                        "unit": group_type,
                        "startOfWeek": "Monday",
                    },
                },
                "value": 1,
            },
        },
        {
            "$group": {
                "_id": "$truncated_datetime",
                "total": {
                    "$sum": "$value",
                },
            },
        },
        {
            "$sort": {
                "_id": 1,
            },
        },
    ]
    return aggr_pl


async def aggregate_collection(
        collection: AsyncIOMotorCollection,
        pipeline: list[dict],
) -> list:
    aggr_col = collection.aggregate(pipeline=pipeline)
    return [doc async for doc in aggr_col]
