import argparse
from time_helpers import convert_time_to_durations

def parse_args(doc):
    parser = argparse.ArgumentParser(description=doc)
    parser.add_argument(
        '-s', '--alarm-sound',
        help='Audio file to be played back, including this argument '
        + 'multiple times will result in per-timer alarm sound',
        action='append',
        default=[])
    parser.add_argument(
        '-a', '--alarm',
        help="Alarm duration. e.g. '4h 30m 20s'. Numbers "
        + "without units like '100' will be interpreted as 100 seconds",
        action='append',
        type = convert_time_to_durations,
        default=[])
    
    parser.add_argument(
        '--escape-quits',
        help='Should the escape key quit this app',
        action=argparse.BooleanOptionalAction,
        default=True)
    return parser.parse_args()
