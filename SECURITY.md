# Seguridad

## Alcance

Quipu UBL procesa XML localmente. No abre conexiones de red y no debe recibir secretos, credenciales ni documentos reales con datos personales en issues o pull requests.

## Reportar una vulnerabilidad

No publiques detalles explotables en un issue. Contacta a los maintainers mediante una vía privada indicada en el perfil del repositorio. Incluye versión, sistema operativo, pasos mínimos para reproducir y una muestra sanitizada.

Hasta contar con un contacto privado configurado, abre un issue con el título `Security contact request` sin adjuntar payload sensible. Se coordinará un canal privado.

## Buenas prácticas

- Ejecuta la herramienta con el mínimo acceso de archivos necesario.
- Revisa y sanitiza XML antes de compartirlo.
- Mantén Python y dependencias actualizados.
- El rechazo de DTD/ENTITY es una defensa adicional; sigue validando entradas no confiables en un entorno aislado.
