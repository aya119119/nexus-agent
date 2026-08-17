"""Sandboxed file-system tools for the agent.

The file tools deliberately enforce a single writable/readable directory so that
future tool expansion can remain secure without relying on conventions alone.
"""
from pathlib import Path

from agent.config import SANDBOX_DIR
from tools.base import Tool


def resolve_safe_path(filename: str, sandbox_dir: str | Path | None = None) -> Path:
    """Resolve a filename against a sandbox and reject any path traversal attempts."""
    base_dir = Path(sandbox_dir) if sandbox_dir is not None else SANDBOX_DIR
    base_dir = base_dir.resolve()

    if not filename or not isinstance(filename, str):
        raise ValueError("A filename string is required.")

    if ".." in filename or filename.startswith("/") or Path(filename).is_absolute():
        raise ValueError(f"Rejected path outside the sandbox: {filename}")

    candidate = (base_dir / filename).resolve()
    if base_dir not in candidate.parents and candidate != base_dir:
        raise ValueError(f"Rejected path outside the sandbox: {filename}")

    return candidate


class FileReadTool(Tool):
    name = "file_read"
    description = "Read a file from the sandbox directory."
    input_schema = {
        "type": "object",
        "properties": {
            "filename": {"type": "string", "description": "Relative path to a file inside the sandbox."}
        },
        "required": ["filename"],
    }

    def run(self, **kwargs) -> str:
        filename = kwargs.get("filename")
        sandbox_dir = kwargs.get("sandbox_dir", SANDBOX_DIR)
        try:
            path = resolve_safe_path(str(filename), sandbox_dir=sandbox_dir)
        except ValueError as exc:
            return f"File read rejected: {exc}"

        if not path.exists():
            return f"File read failed: '{filename}' does not exist inside the sandbox."

        try:
            return path.read_text(encoding="utf-8")
        except Exception as exc:
            return f"File read failed: {exc}"


class FileWriteTool(Tool):
    name = "file_write"
    description = "Write a file inside the sandbox directory."
    input_schema = {
        "type": "object",
        "properties": {
            "filename": {"type": "string", "description": "Relative path to a file inside the sandbox."},
            "content": {"type": "string", "description": "Text content to write to the file."},
        },
        "required": ["filename", "content"],
    }

    def run(self, **kwargs) -> str:
        filename = kwargs.get("filename")
        content = kwargs.get("content")
        sandbox_dir = kwargs.get("sandbox_dir", SANDBOX_DIR)

        if content is None:
            return "File write failed: content must be a string."

        try:
            path = resolve_safe_path(str(filename), sandbox_dir=sandbox_dir)
        except ValueError as exc:
            return f"File write rejected: {exc}"

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(str(content), encoding="utf-8")
            return f"File written successfully to: {path}"
        except Exception as exc:
            return f"File write failed: {exc}"
