"""Simple visual timer.

Play a sound after timer(s) count down.
"""

import slint
import sys
import os
import uuid
import datetime
from datetime import timedelta
from datetime import datetime
from time_helpers import get_nth, play_time_sound, update_display_time
from command_line_helpers import parse_args

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
    def __init__(self, timers = []):
        super().__init__()
        self.timers = []
        self.add_timers(timers)
        self.time_tick()

    def add_timers(self, timers):
        now = datetime.now()
        now = now - timedelta(microseconds=now.microsecond)

        new_timers = [{
            "id": str(uuid.uuid4()),
            "duration": timedelta(seconds=duration),
            "start": now,
            "sound": get_nth(args.alarm_sound, index)
        } for index, duration in enumerate(timers)]
        self.timers.extend(new_timers)

    def set_elapsed_time(self):
        now = datetime.now()
        micros = timedelta(microseconds=now.microsecond)
        now = now - micros
        for timer in self.timers:
            done = update_display_time(now, timer)
            if done:
                play_time_sound(timer)
        if self.timer_list.row_count() == len(self.timers):
            for i, timer in enumerate(self.timers):
                self.timer_list.set_row_data(i, {
                    "id": timer["id"],
                    "time-left": timer["time-left"],
                })
        else:
            self.timer_list = slint.ListModel()
            for timer in self.timers:
                self.timer_list.append({
                    "id": timer["id"],
                    "time-left": timer["time-left"],
                })

    def time_tick(self):
        now = datetime.now()
        micros = timedelta(microseconds=now.microsecond)

        self.set_elapsed_time()
        slint.Timer.single_shot(timedelta(seconds=1.01) - micros,
                                lambda: self.time_tick())

    @slint.callback
    def stop_timer(self, to_delete):
        i = next(
            (i
             for i, timer in enumerate(self.timers)
             if timer["id"] == to_delete.id),
            None)
        if i == None:
            return
        timer = self.timers.pop(i)
        sound = timer.get("alarm-sound", None)
        if sound is not None:
            sound.stop()
        self.set_elapsed_time()
        if len(self.timers) == 0:
            self.hide()

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
    args = parse_args(__doc__)
    if len(args.alarm) > 0:
        global_timers = args.alarm
    alarm_list_window = AlarmListWindow(global_timers)
    alarm_list_window.show()
    alarm_list_window.run()

