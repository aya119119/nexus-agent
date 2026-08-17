from pathlib import Path

from tools.file_io import FileReadTool, FileWriteTool, resolve_safe_path


def test_write_and_read_file_round_trip(tmp_path):
    sandbox = tmp_path / "sandbox"
    sandbox.mkdir()

    file_path = sandbox / "notes.txt"
    content = "hello from file tool"

    result = FileWriteTool().run(filename="notes.txt", content=content, sandbox_dir=sandbox)
    assert "written" in result.lower()
    assert FileReadTool().run(filename="notes.txt", sandbox_dir=sandbox) == content


def test_rejects_path_traversal_attempt(tmp_path):
    sandbox = tmp_path / "sandbox"
    sandbox.mkdir()

    result = FileReadTool().run(filename="../../etc/passwd", sandbox_dir=sandbox)
    assert "rejected" in result.lower() or "sandbox" in result.lower()


def test_read_missing_file_returns_clear_error(tmp_path):
    sandbox = tmp_path / "sandbox"
    sandbox.mkdir()

    result = FileReadTool().run(filename="missing.txt", sandbox_dir=sandbox)
    assert "not found" in result.lower() or "does not exist" in result.lower()


def test_resolve_safe_path_rejects_escape(tmp_path):
    sandbox = tmp_path / "sandbox"
    sandbox.mkdir()

    try:
        resolve_safe_path("../../etc/passwd", sandbox_dir=sandbox)
        assert False, "Expected ValueError for sandbox escape"
    except ValueError:
        pass
