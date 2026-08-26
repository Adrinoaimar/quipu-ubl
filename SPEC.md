# Quipu UBL — especificación 0.1

## Objetivo

Validar localmente una línea base estructural de documentos `Invoice` UBL 2.x antes de enviarlos a un proveedor o autoridad. Quipu UBL no emite, firma, envía ni certifica comprobantes.

## Entrada

- XML UTF-8 desde archivo o stdin (`-`).
- Raíz `Invoice` en `urn:oasis:names:specification:ubl:schema:xsd:Invoice-2`.
- Sin llamadas de red, carga de esquemas remotos ni resolución de entidades.

## Reglas 0.1

1. XML bien formado.
2. No se permiten `DOCTYPE` ni `ENTITY`.
3. Raíz local `Invoice` y namespace UBL Invoice-2.
4. Hijos directos obligatorios: `ID`, `IssueDate`, `AccountingSupplierParty`, `AccountingCustomerParty`, `LegalMonetaryTotal`.

Perfiles nacionales (SUNAT, DIAN, SAT y otros) quedan fuera de 0.1. Se añadirán como módulos versionados, sin alterar el núcleo.

## Salida estable

Cada hallazgo contiene `code`, `message` y `severity`. Códigos 0.1:

- `XML_NOT_WELL_FORMED`
- `UNSAFE_XML_DECLARATION`
- `ROOT_ELEMENT`
- `ROOT_NAMESPACE`
- `REQUIRED_FIELD_MISSING`
- `IO_ERROR`

CLI: `0` si todo es válido, `1` si hay hallazgos de validación, `2` si existe error de lectura o uso. `--json` devuelve una lista apta para CI.

## Compatibilidad y seguridad

Python 3.10+. Solo biblioteca estándar en runtime. Procesamiento offline y determinista. No incluir XML reales, credenciales, certificados ni PII en issues, fixtures o pull requests.

## Evolución

Cambios incompatibles requieren nueva versión mayor. Nuevas reglas deben incluir tests, código estable, documentación bilingüe y una fixture mínima. Próximas extensiones: perfiles de país, validación de `CreditNote`, Schematron local versionado y GitHub Action reutilizable.
