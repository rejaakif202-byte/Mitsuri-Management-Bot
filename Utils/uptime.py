import time

START_TIME = time.time()

def get_uptime():

    seconds = int(time.time() - START_TIME)

    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    return f"{days}d {hours}h {minutes}m {sec}s"
