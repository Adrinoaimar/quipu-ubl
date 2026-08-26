"""Small, deterministic UBL Invoice validator.

The validator intentionally checks a portable baseline only. Country-specific
rules belong in separate profiles so this package never pretends to issue or
certify a real tax document.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import xml.etree.ElementTree as ET
from typing import Iterable, TextIO

UBL_INVOICE_NAMESPACE = "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"
REQUIRED_PATHS: tuple[tuple[str, ...], ...] = (
    ("ID",),
    ("IssueDate",),
    ("AccountingSupplierParty",),
    ("AccountingCustomerParty",),
    ("LegalMonetaryTotal",),
)


@dataclass(frozen=True)
class ValidationIssue:
    """One stable machine-readable finding."""

    code: str
    message: str
    severity: str = "error"

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "message": self.message, "severity": self.severity}


@dataclass(frozen=True)
class ValidationResult:
    """Validation result for one input document."""

    source: str
    valid: bool
    issues: tuple[ValidationIssue, ...] = ()

    def as_dict(self) -> dict[str, object]:
        return {
            "source": self.source,
            "valid": self.valid,
            "issues": [issue.as_dict() for issue in self.issues],
        }


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _namespace(tag: str) -> str | None:
    if tag.startswith("{") and "}" in tag:
        return tag[1:].split("}", 1)[0]
    return None


def _has_child(root: ET.Element, local_name: str) -> bool:
    return any(_local_name(child.tag) == local_name for child in root)


def validate_xml(xml: str | bytes, source: str = "<string>") -> ValidationResult:
    """Validate XML text against the portable UBL Invoice baseline.

    Parsing rejects DTD/entity declarations before using the standard-library
    parser. This keeps the offline CLI deterministic and avoids external
    entity resolution. No network requests are made.
    """

    if isinstance(xml, bytes):
        raw = xml
        text_for_checks = xml.decode("utf-8", errors="ignore")
    else:
        raw = xml.encode("utf-8")
        text_for_checks = xml

    if "<!DOCTYPE" in text_for_checks.upper() or "<!ENTITY" in text_for_checks.upper():
        return ValidationResult(
            source,
            False,
            (
                ValidationIssue(
                    "UNSAFE_XML_DECLARATION",
                    "DOCTYPE and ENTITY declarations are not allowed in offline validation.",
                ),
            ),
        )

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        return ValidationResult(
            source,
            False,
            (ValidationIssue("XML_NOT_WELL_FORMED", f"XML is not well-formed: {exc}"),),
        )

    issues: list[ValidationIssue] = []
    if _local_name(root.tag) != "Invoice":
        issues.append(
            ValidationIssue(
                "ROOT_ELEMENT",
                f"Root element must be Invoice; found {_local_name(root.tag)}.",
            )
        )
    if _namespace(root.tag) != UBL_INVOICE_NAMESPACE:
        found = _namespace(root.tag) or "(none)"
        issues.append(
            ValidationIssue(
                "ROOT_NAMESPACE",
                f"Root namespace must be {UBL_INVOICE_NAMESPACE}; found {found}.",
            )
        )

    for (field,) in REQUIRED_PATHS:
        if not _has_child(root, field):
            issues.append(
                ValidationIssue(
                    "REQUIRED_FIELD_MISSING",
                    f"Required Invoice/{field} element is missing.",
                )
            )

    return ValidationResult(source, not issues, tuple(issues))


def validate_stream(stream: TextIO, source: str = "<stdin>") -> ValidationResult:
    """Read and validate one text stream."""

    return validate_xml(stream.read(), source=source)


def results_as_json(results: Iterable[ValidationResult], *, indent: int = 2) -> str:
    """Serialize results for stable CLI/API consumption."""

    return json.dumps([result.as_dict() for result in results], ensure_ascii=False, indent=indent)
