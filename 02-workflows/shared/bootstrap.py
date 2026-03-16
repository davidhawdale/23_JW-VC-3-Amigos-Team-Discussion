#!/usr/bin/env python3
"""Shared import bootstrap helpers for workflow scripts."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module '{module_name}' from {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def import_shared(caller_file: str, module_name: str):
    """Import a module from 02-workflows/shared by file path."""
    caller = Path(caller_file).resolve()
    shared_dir = caller.parents[1] / "shared"
    target = shared_dir / f"{module_name}.py"
    return _load_module(f"workflow_shared_{module_name}", target)


def import_local(caller_file: str, module_name: str):
    """Import a sibling module from the caller's directory by file path."""
    caller = Path(caller_file).resolve()
    target = caller.parent / f"{module_name}.py"
    return _load_module(f"workflow_local_{module_name}", target)

