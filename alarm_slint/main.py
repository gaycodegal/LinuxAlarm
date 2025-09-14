import slint
import sys
import os

try:
    slint.loader.ui.alarm_list_window.AlarmListWindow
except slint.CompileError as e:
    print(e.message)
    for diagnostic in e.diagnostics:
        print(diagnostic)
    sys.exit(1)

class AlarmListWindow(slint.loader.ui.alarm_list_window.AlarmListWindow):
    def __init__(self):
        super().__init__()
        #self.data.append({})

        


    @slint.callback
    def key_pressed(self, event):
        control_or_meta = (event.modifiers.control or event.modifiers.meta)
        is_q_quit = (event.text == "q" and control_or_meta)
        if event.text == "\x1b" or is_q_quit:
            self.hide()
            return True
        return False
    
alarm_list_window = AlarmListWindow()
alarm_list_window.show()
alarm_list_window.run()
