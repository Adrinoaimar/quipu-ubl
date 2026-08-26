# Quipu UBL

[![CI](https://github.com/Adrinoaimar/quipu-ubl/actions/workflows/ci.yml/badge.svg)](https://github.com/Adrinoaimar/quipu-ubl/actions/workflows/ci.yml)

Validador offline, pequeño y reproducible para una línea base de facturas electrónicas UBL. El comando `latam-einvoice` ayuda a detectar errores estructurales antes de enviar un documento a un proveedor o autoridad.

> Quipu UBL no emite, firma ni certifica comprobantes. No reemplaza validación tributaria de SUNAT, DIAN, SAT u otra autoridad.

## Inicio rápido

Requiere Python 3.10 o superior.

```bash
# Desde el repositorio publicado
python -m pip install "quipu-ubl @ git+https://github.com/Adrinoaimar/quipu-ubl.git@v0.2.1"
latam-einvoice --version

# En GitHub Actions
# Consulta docs/github-action.md para el workflow completo.

# Para desarrollo local (después de clonar)
python -m pip install -e ".[test]"
latam-einvoice validate examples/valid-invoice.xml
latam-einvoice validate examples/invalid-invoice.xml --json
cat examples/valid-invoice.xml | latam-einvoice validate -
python -m pytest
```

Código de salida: `0` si todos los documentos son válidos, `1` si hay hallazgos de validación, `2` si no se pudo leer un archivo o hubo error de uso.

## Línea base validada

- XML bien formado.
- Raíz `Invoice` con namespace UBL Invoice-2.
- Hijos obligatorios: `ID`, `IssueDate`, `AccountingSupplierParty`, `AccountingCustomerParty` y `LegalMonetaryTotal`.
- Declaraciones `DOCTYPE` y `ENTITY` rechazadas para mantener validación offline segura.

Las reglas son intencionadamente mínimas. Perfiles de país pueden añadirse sin cambiar el núcleo. Consulta el contrato exacto en [SPEC.md](SPEC.md).

## Diseño y comunidad

Resultados tienen códigos estables (`ROOT_NAMESPACE`, `REQUIRED_FIELD_MISSING`, etc.) y formato JSON para CI. No se hacen llamadas de red ni se envían documentos. Issues y pull requests son bienvenidos; consulta [CONTRIBUTING.md](CONTRIBUTING.md).

También puedes usar la [GitHub Action](docs/github-action.md) para bloquear PRs con XML UBL estructuralmente inválido.

## API Python

```python
from quipu_ubl import validate_xml

result = validate_xml(xml_bytes, source="invoice.xml")
if not result.valid:
    for issue in result.issues:
        print(issue.code, issue.message)
```

La publicación en PyPI se prepara mediante GitHub Actions y Trusted Publishing. Consulta [docs/publishing.md](docs/publishing.md) para activar el publisher. Hasta entonces, instala desde GitHub o clona el repositorio.

La idea toma referencias públicas de estándares OASIS UBL y del ecosistema de proyectos como [Greenter](https://github.com/thegreenter/greenter), OpenUBL y DIAN Kit. No se copia código ni datos de esos proyectos.

## English

Quipu UBL is a small, deterministic offline validator for a baseline UBL Invoice XML shape. It catches structural mistakes before a document reaches a provider or tax authority.

It does **not** issue, sign, submit, or certify invoices. It is not a replacement for country-specific tax validation.

Install with `python -m pip install -e ".[test]"`; run `latam-einvoice validate examples/valid-invoice.xml`. Exit codes are `0` (all valid), `1` (validation findings), and `2` (I/O or usage error). JSON output supports CI. The validator makes no network calls and rejects DTD/entity declarations.

## Licencia

MIT. Consulta [LICENSE](LICENSE).
