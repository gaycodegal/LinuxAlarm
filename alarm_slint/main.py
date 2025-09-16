import slint
from slint import slint as native
import sys
import os
import uuid
import datetime
from playsound3 import playsound
from datetime import timedelta
from datetime import datetime
import argparse


try:
    slint.loader.ui.alarm_list_window.AlarmListWindow
except slint.CompileError as e:
    print(e.message)
    for diagnostic in e.diagnostics:
        print(diagnostic)
    sys.exit(1)

args = None
global_timers = [5]

class AlarmListWindow(slint.loader.ui.alarm_list_window.AlarmListWindow):
    def __init__(self):
        super().__init__()
        now = datetime.now()
        self.timers = [{
            "id": str(uuid.uuid4()),
            "duration": timedelta(seconds=duration),
            "start": now,
        } for duration in global_timers]
        

        self.time_tick()

    def set_elapsed_time(self):
        now = datetime.now()
        for timer in self.timers:
            diff = int((timer["start"] + timer["duration"] - now).total_seconds())
            seconds = diff % 60
            minutes = (diff // 60) % 60
            hours = diff // 60 // 60
            if diff <= 0:
                timer["time-left"] = "Done"
                if "alarm-sound" not in timer:
                    try:
                        timer["alarm-sound"] = playsound(
                            args.alarm_sound, block=False)
                    except:
                        timer["alarm-sound"] = None
                        print("\a")
            else:
                if hours > 0:
                    timer["time-left"] = f"{hours}h {minutes:02}m"
                else:
                    timer["time-left"] = f"{minutes}:{seconds:02}"
        self.timer_list = slint.ListModel()
        for timer in self.timers:
            self.timer_list.append({
                "id": timer["id"],
                "time-left": timer["time-left"],
            })

    def time_tick(self):
        self.set_elapsed_time()
        slint.Timer.single_shot(timedelta(seconds=1),
                                lambda: self.time_tick())


    @slint.callback
    def key_pressed(self, event):
        control_or_meta = (event.modifiers.control or event.modifiers.meta)
        is_q_quit = (event.text == "q" and control_or_meta)
        is_escape_quit = args.escape_quits and event.text == "\x1b"
        if is_escape_quit or is_q_quit:
            self.hide()
            return True
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--alarm-sound',
        help='audio file to be played back',
        default="alarm.mp3")
    parser.add_argument(
        '--alarm',
        help='alarm duration in seconds',
        action='append',
        type=int)
    
    parser.add_argument(
        '--escape-quits',
        help='should the escape key quit this app',
        action=argparse.BooleanOptionalAction,
        default=True)
    args = parser.parse_args()
    if len(args.alarm) > 0:
        global_timers = args.alarm
    alarm_list_window = AlarmListWindow()
    alarm_list_window.show()
    alarm_list_window.run()

