from pathlib import Path

from quipu_ubl.validator import UBL_INVOICE_NAMESPACE, validate_xml


VALID_XML = f'''<?xml version="1.0" encoding="UTF-8"?>
<Invoice xmlns="{UBL_INVOICE_NAMESPACE}">
  <ID>F001-00000001</ID>
  <IssueDate>2026-01-01</IssueDate>
  <AccountingSupplierParty><Party><PartyName><Name>Demo</Name></PartyName></Party></AccountingSupplierParty>
  <AccountingCustomerParty><Party><PartyName><Name>Buyer</Name></PartyName></Party></AccountingCustomerParty>
  <LegalMonetaryTotal><PayableAmount currencyID="PEN">10.00</PayableAmount></LegalMonetaryTotal>
</Invoice>'''


def test_valid_invoice():
    result = validate_xml(VALID_XML, "valid.xml")
    assert result.valid
    assert result.issues == ()


def test_missing_fields_are_reported():
    result = validate_xml(f'<Invoice xmlns="{UBL_INVOICE_NAMESPACE}"/>')
    assert not result.valid
    assert [issue.code for issue in result.issues] == ["REQUIRED_FIELD_MISSING"] * 5


def test_namespace_and_root_are_checked():
    result = validate_xml("<Invoice/>")
    assert not result.valid
    assert "ROOT_NAMESPACE" in {issue.code for issue in result.issues}


def test_malformed_xml():
    result = validate_xml("<Invoice>")
    assert result.issues[0].code == "XML_NOT_WELL_FORMED"


def test_dtd_is_rejected():
    result = validate_xml('<!DOCTYPE Invoice [<!ENTITY x "x">]><Invoice/>')
    assert result.issues[0].code == "UNSAFE_XML_DECLARATION"


def test_examples_exist():
    assert Path("examples/valid-invoice.xml").exists()
