import re
from playsound3 import playsound

part_splitter = re.compile('([a-z])')


def play_time_sound(timer):
    if "alarm-sound" not in timer:
        try:
            timer["alarm-sound"] = playsound(
                timer["sound"], block=False)
        except:
            timer["alarm-sound"] = None
            print("\a")

def update_display_time(now, timer):
    diff = int((timer["start"] + timer["duration"] - now).total_seconds())
    seconds = diff % 60
    minutes = (diff // 60) % 60
    hours = diff // 60 // 60
    if diff <= 0:
        timer["time-left"] = "Done"
        return True
    else:
        if hours > 0:
            timer["time-left"] = f"{hours}h {minutes:02}m"
        else:
            timer["time-left"] = f"{minutes}:{seconds:02}"
        return False

def convert_times_to_durations(raw_times):
    return [convert_time_to_durations(time) for time in raw_times]

def convert_time_to_durations(raw_time):
    """ converts times like 100m 5h 30s into
    durations in seconds

    also accepts durations in seconds without units
    """
    time_parts = part_splitter.split(raw_time.lower())
    if len(time_parts) == 1:
        return int(raw_time)
    duration = 0
    for i in range(0, (len(time_parts) // 2) * 2, 2):
        time_code = time_parts[i+1]
        if time_code == 'h':
            duration += int(time_parts[i]) * 60 * 60
        elif time_code == 'm':
            duration += int(time_parts[i]) * 60
        elif time_code == 's':
            duration += int(time_parts[i])
    return duration


def get_nth(lst, n, repeat = True):
    if n < len(lst):
        return lst[n]
    if repeat:
        return lst[-1]
    return lst[n%len(lst)]
