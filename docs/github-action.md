# GitHub Action

Quipu UBL puede ejecutarse como action reutilizable. Crea `.github/workflows/ubl.yml` en tu repositorio:

```yaml
name: Validate UBL

on:
  pull_request:

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: Adrinoaimar/quipu-ubl@v0.2.0
        with:
          files: examples/valid-invoice.xml
```

La action instala el paquete localmente y ejecuta validación offline. Usa rutas sin espacios o cita una única ruta cuando tu shell lo requiera. Fija una versión (`@v0.2.0`) para builds reproducibles.
