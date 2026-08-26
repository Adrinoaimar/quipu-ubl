# Publicar en PyPI

El repositorio incluye un workflow de publicación sin tokens persistentes.

1. En PyPI, crea el proyecto `quipu-ubl` o configura un Trusted Publisher para este repositorio.
2. Usa owner `Adrinoaimar`, repository `quipu-ubl`, workflow `publish.yml` y environment `pypi`.
3. En GitHub, crea variable de repositorio `PYPI_TRUSTED_PUBLISHER=true`.
4. Publica un release semver. El workflow construirá wheel y sdist, luego publicará con OIDC.

Antes de activar, comprueba localmente:

```bash
python -m pip install --upgrade build twine
python -m build
twine check dist/*
```

No compartas tokens ni credenciales en issues, commits o variables públicas.
