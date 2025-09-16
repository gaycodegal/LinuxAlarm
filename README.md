# Linux Alarm

Simple Alarm setting tool for Linux

Sets one or more timers for N seconds that will display in a ui window. Plays a song of your choosing on alarm completion.

Presumably more features to come. Intended for use with other command line
programs that may wish to set an alarm programatically, like a digital
assistant, and have the alarm visually displayed to a user and manually
cancelable.

## Installation

pip3 install playsound3
pip3 install slint

## Running

Needs to be ran with this if you want SIGINT (^C) to kill the app.

```bash
./alarm_slint/run.sh --alarm 5 --alarm-sound ~/Music/alarm.mp3
```
