# Contribuir

Gracias por ayudar a Quipu UBL.

1. Abre un issue para describir cambio o bug.
2. Crea una rama desde `main`.
3. Añade o actualiza tests para cada comportamiento.
4. Ejecuta `python -m pytest` y `python -m compileall src`.
5. Envía un pull request con contexto, impacto y compatibilidad.

Mantén el núcleo offline, determinista y sin datos tributarios reales. Las reglas nuevas deben tener códigos de error estables y documentación en español e inglés cuando sea posible. No incluyas secretos, PII, XML de clientes ni archivos generados.

## Estilo

- Python estándar, type hints y funciones pequeñas.
- Mensajes de usuario claros; no expongas rutas o contenido innecesario.
- Cambios incompatibles requieren nota en README y prueba de regresión.
