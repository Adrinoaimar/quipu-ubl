"""Command-line interface for Quipu UBL."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from . import __version__
from .validator import ValidationResult, validate_stream


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="latam-einvoice",
        description="Offline baseline validator for UBL Invoice XML.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate", help="Validate one or more XML files.")
    validate.add_argument("paths", nargs="+", metavar="PATH", help="XML file path, or - for stdin.")
    validate.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    return parser


def _read(path: str) -> tuple[ValidationResult | None, str | None]:
    if path == "-":
        return validate_stream(sys.stdin), None
    try:
        with Path(path).open("r", encoding="utf-8") as stream:
            return validate_stream(stream, source=path), None
    except OSError as exc:
        return None, f"{path}: cannot read file: {exc}"


def _text_output(results: list[ValidationResult], errors: list[str]) -> str:
    lines: list[str] = []
    for result in results:
        status = "VALID" if result.valid else "INVALID"
        lines.append(f"{status} {result.source}")
        for issue in result.issues:
            lines.append(f"  [{issue.severity.upper()}] {issue.code}: {issue.message}")
    for error in errors:
        lines.append(f"ERROR {error}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command != "validate":
        return 2

    results: list[ValidationResult] = []
    errors: list[str] = []
    for path in args.paths:
        result, error = _read(path)
        if result is not None:
            results.append(result)
        if error is not None:
            errors.append(error)

    if args.json:
        payload = [result.as_dict() for result in results]
        for error in errors:
            source = error.split(": cannot read file:", 1)[0]
            payload.append(
                {
                    "source": source,
                    "valid": False,
                    "issues": [
                        {"code": "IO_ERROR", "message": error, "severity": "error"}
                    ],
                }
            )
        import json

        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(_text_output(results, errors))

    return 2 if errors else (0 if all(result.valid for result in results) else 1)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
