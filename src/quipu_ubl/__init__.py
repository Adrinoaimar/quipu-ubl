"""Offline UBL conformance checks for Latin American e-invoicing projects."""

__version__ = "0.1.0"

from .validator import ValidationIssue, ValidationResult, validate_xml

__all__ = ["ValidationIssue", "ValidationResult", "validate_xml", "__version__"]
