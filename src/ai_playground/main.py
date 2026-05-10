"""Main entry point for ai-playground."""

import argparse
from ai_playground import __version__


def parse_args():
    parser = argparse.ArgumentParser(
        prog="ai-playground",
        description="A simple terminal-based AI hobby app.",
    )

    return parser.parse_args()


def main():
    args = parse_args()
