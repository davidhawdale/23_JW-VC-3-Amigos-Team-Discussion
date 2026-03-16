#!/usr/bin/env python3
"""Shared helper functions for workflow verification scripts."""

import os


def file_exists(path: str) -> bool:
    return os.path.exists(path)


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def missing_headings(content: str, required_headings: list[str]) -> list[str]:
    return [heading for heading in required_headings if heading not in content]


def word_count(content: str) -> int:
    return len(content.split())

