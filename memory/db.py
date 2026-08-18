"""SQLite-backed session persistence for short-term agent memory.

The database keeps a lightweight conversation history: one row per session and one
row per message. Message content is stored as JSON so structured Anthropic payloads
(tool_use blocks, tool_result blocks, and mixed text payloads) remain round-trippable
without losing metadata.
"""
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agent.config import DB_PATH


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _connect(db_path: str | Path = DB_PATH):
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str | Path = DB_PATH) -> None:
    """Create the sessions and messages tables if they do not already exist."""
    with _connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                title TEXT DEFAULT 'Untitled'
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            )
            """
        )
        conn.commit()


def create_session(title: str = "Untitled", db_path: str | Path = DB_PATH) -> str:
    """Create a new session and return the generated session_id."""
    session_id = str(uuid.uuid4())
    created_at = _now_iso()
    with _connect(db_path) as conn:
        conn.execute(
            "INSERT INTO sessions (id, created_at, title) VALUES (?, ?, ?)",
            (session_id, created_at, title),
        )
        conn.commit()
    return session_id


def save_message(session_id: str, role: str, content: Any, db_path: str | Path = DB_PATH) -> None:
    """Persist one message to SQLite, serializing structured content to JSON."""
    content_json = json.dumps(content, ensure_ascii=False)
    created_at = _now_iso()
    with _connect(db_path) as conn:
        conn.execute(
            "INSERT INTO messages (session_id, role, content, created_at) VALUES (?, ?, ?, ?)",
            (session_id, role, content_json, created_at),
        )
        conn.commit()


def load_messages(session_id: str, db_path: str | Path = DB_PATH) -> list[dict]:
    """Return messages in chronological order, deserializing JSON content back to Python objects."""
    with _connect(db_path) as conn:
        rows = conn.execute(
            "SELECT id, role, content FROM messages WHERE session_id = ? ORDER BY id ASC",
            (session_id,),
        ).fetchall()

    messages: list[dict] = []
    for row in rows:
        payload = json.loads(row["content"]) if row["content"] else ""
        messages.append({"role": row["role"], "content": payload})
    return messages


def list_sessions(db_path: str | Path = DB_PATH) -> list[dict]:
    """List all sessions, newest first."""
    with _connect(db_path) as conn:
        rows = conn.execute(
            "SELECT id, title, created_at FROM sessions ORDER BY created_at DESC"
        ).fetchall()
    return [
        {"id": row["id"], "title": row["title"], "created_at": row["created_at"]}
        for row in rows
    ]


def delete_session(session_id: str, db_path: str | Path = DB_PATH) -> None:
    """Delete a single session and all of its messages."""
    with _connect(db_path) as conn:
        conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
        conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        conn.commit()


def update_session_title(session_id: str, title: str, db_path: str | Path = DB_PATH) -> None:
    """Update the title for a session."""
    with _connect(db_path) as conn:
        conn.execute("UPDATE sessions SET title = ? WHERE id = ?", (title, session_id))
        conn.commit()
