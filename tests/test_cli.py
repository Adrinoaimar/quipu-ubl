from pathlib import Path

from quipu_ubl.cli import main


def test_cli_valid_text(capsys):
    code = main(["validate", "examples/valid-invoice.xml"])
    captured = capsys.readouterr()
    assert code == 0
    assert "VALID examples/valid-invoice.xml" in captured.out


def test_cli_invalid_json(capsys):
    code = main(["validate", "examples/invalid-invoice.xml", "--json"])
    captured = capsys.readouterr()
    assert code == 1
    assert '"valid": false' in captured.out
    assert "REQUIRED_FIELD_MISSING" in captured.out


def test_cli_io_error_has_exit_two(capsys, tmp_path: Path):
    missing = tmp_path / "missing.xml"
    code = main(["validate", str(missing), "--json"])
    captured = capsys.readouterr()
    assert code == 2
    assert '"code": "IO_ERROR"' in captured.out
    assert "missing.xml" in captured.out
