"""Main entry point for ai-playground."""

import argparse
from ai_playground import __version__


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ai-playground",
        description="A simple terminal-based hobby app.",
    )
    parser.add_argument(
        "--name",
        default="World",
        help="Name to greet.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"ai-playground {__version__}",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(f"Hello, {args.name}!")
