from enum import Enum


class TrainingType(str, Enum):
    HOURLY = "histohour"
    DAILY = "histoday"
    MINUTE = "histominute"
