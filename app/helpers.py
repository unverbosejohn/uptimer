
seconds_in_minute = 60
seconds_in_hour = 3600
seconds_in_day = 86400


def hr_time(seconds: int, seconds_decimal: int = 3) -> str:
    """
    Returns a human readable string of the given number of seconds.

    :param seconds: Seconds to convert to human readable string.
    :param seconds_decimal: Number of decimal places to round seconds to.
    :return: Human readable string of the given number of seconds.
    """

    days, seconds = divmod(seconds, seconds_in_day)
    hours, seconds = divmod(seconds, seconds_in_hour)
    minutes, seconds = divmod(seconds, seconds_in_minute)

    time_str = ""
    if days > 0:
        time_str += f"{days} day{'s' if days > 1 else ''}, "
    if hours > 0:
        time_str += f"{hours} hour{'s' if hours > 1 else ''}, "
    if minutes > 0:
        time_str += f"{minutes} minute{'s' if minutes > 1 else ''}, "
    time_str += f"{round(seconds, seconds_decimal)} second{'s' if seconds != 1 else ''}"

    return time_str


if __name__ == '__main__':
    print(hr_time(60))