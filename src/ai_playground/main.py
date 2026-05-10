from __future__ import annotations

import argparse

from ai_playground import hello


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ai-playground",
        description="A terminal-based hobby app built with native Python tooling.",
    )
    parser.add_argument(
        "--name",
        default="friend",
        help="Your name for the greeting.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="ai-playground 0.1.0",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    message = hello(args.name)
    print(message)


if __name__ == "__main__":
    main()
