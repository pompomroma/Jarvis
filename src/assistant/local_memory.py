from pathlib import Path
from typing import Optional


def load_local_memory(path: Optional[Path]) -> str:
    """
    Load a lightweight knowledge seed from disk to bias the assistant when offline.
    """
    if path is None:
        return ""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")
