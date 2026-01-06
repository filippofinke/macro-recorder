import argparse
import sys

from macro_recorder.commands import cmd_record, cmd_play, cmd_info
from macro_recorder.ui import RichUI


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="macro-recorder",
        description="Record and playback mouse macros"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    record_parser = subparsers.add_parser("record", help="Record a new macro")
    record_parser.add_argument("name", help="Name for the recording")
    record_parser.add_argument(
        "-o", "--output",
        default=".",
        help="Output directory (default: current directory)"
    )
    record_parser.add_argument(
        "-d", "--delay",
        type=int,
        default=3,
        help="Seconds to wait before recording starts (default: 3)"
    )
    record_parser.set_defaults(func=cmd_record)

    play_parser = subparsers.add_parser("play", help="Play a recorded macro")
    play_parser.add_argument("file", help="Path to the recording file")
    play_parser.add_argument(
        "-s", "--speed",
        type=float,
        default=1.0,
        help="Playback speed multiplier (default: 1.0)"
    )
    play_parser.add_argument(
        "-r", "--repeat",
        type=int,
        default=1,
        help="Number of times to repeat (0 for infinite)"
    )
    play_parser.set_defaults(func=cmd_play)

    info_parser = subparsers.add_parser("info", help="Show recording info")
    info_parser.add_argument("file", help="Path to the recording file")
    info_parser.set_defaults(func=cmd_info)

    args = parser.parse_args()

    if args.command is None:
        ui = RichUI()
        ui.header()
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
