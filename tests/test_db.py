import json

from memory.db import create_session, delete_session, init_db, list_sessions, load_messages, save_message


def test_create_session_and_list_sessions(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)

    session_id = create_session(title="Test Session", db_path=db_path)
    sessions = list_sessions(db_path=db_path)

    assert session_id
    assert any(item["id"] == session_id for item in sessions)
    assert any(item["title"] == "Test Session" for item in sessions)


def test_save_message_and_load_messages_round_trip(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)

    session_id = create_session(db_path=db_path)
    save_message(session_id, "user", "Hello there", db_path=db_path)
    save_message(session_id, "assistant", {"type": "text", "text": "Hi!"}, db_path=db_path)

    messages = load_messages(session_id, db_path=db_path)

    assert messages[0] == {"role": "user", "content": "Hello there"}
    assert messages[1] == {"role": "assistant", "content": {"type": "text", "text": "Hi!"}}


def test_delete_session_removes_messages(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)

    session_id = create_session(db_path=db_path)
    save_message(session_id, "user", "Test message", db_path=db_path)

    delete_session(session_id, db_path=db_path)

    assert list_sessions(db_path=db_path) == []
    assert load_messages(session_id, db_path=db_path) == []


def test_round_trip_with_tool_use_content(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)

    session_id = create_session(title="Tool test", db_path=db_path)
    structured = [
        {"type": "tool_use", "id": "toolu_1", "name": "web_search", "input": {"query": "python"}},
        {"type": "tool_result", "tool_use_id": "toolu_1", "content": "Search result"},
    ]

    save_message(session_id, "assistant", structured, db_path=db_path)
    loaded = load_messages(session_id, db_path=db_path)

    assert loaded == [{"role": "assistant", "content": structured}]
