# 🔍 Comparativa y Guía de Corrección: Video Tutorial vs. Proyecto Actual

Este documento explica en detalle **por qué el código original del video tutorial presentaba errores al ejecutarse hoy en día**, cuáles fueron las **correcciones aplicadas** en este repositorio y cómo utilizar esta información para redactar la documentación oficial de tu proyecto.

---

## 📌 Resumen de Cambios Clave

| Aspecto | Video Tutorial (Original) | Proyecto Actual (Corregido) | ¿Por qué cambió? / Motivo del Error |
| :--- | :--- | :--- | :--- |
| **Versiones de Actions** | `@v2` / `@v3` desactualizadas | `@v4` (`checkout`), `@v5` (`setup-python`), `@v3` (`docker/login`), `@v5` (`docker/build-push`) | GitHub retiró el soporte para Node 12 y Node 16 en los *runners*. Las versiones viejas lanzan advertencias o fallan. |
| **Permisos de `GITHUB_TOKEN`** | No especificaba permisos en el archivo `.yml` | Se agregó `permissions: { contents: read, packages: write }` | GitHub cambió la política por defecto a **Solo Lectura**. Sin este bloque, la publicación en GHCR da error `403 Forbidden`. |
| **Mayúsculas en Nombre de Imagen** | Usaba `${{ github.repository }}` directamente | Se agregó un paso bash que convierte la variable a minúsculas (`tr '[:upper:]' '[:lower:]'`) | Los registros de contenedores Docker (GHCR, Docker Hub) **exigen minúsculas**. Si el usuario tiene mayúsculas en su perfil/repo, falla con `invalid reference format`. |
| **Rutas e Importaciones de Python** | `from calculator import add` (falla fuera de directorio) | `from app.calculator import add` + resolución dinámica de `sys.path` | Evita el error `ModuleNotFoundError: No module named 'app'` al ejecutar desde la raíz del proyecto o en pytest. |
| **`PYTHONPATH` en Docker** | Sin variable de entorno | `ENV PYTHONPATH=/app` en el `Dockerfile` | Permite que la imagen de Docker ejecute los módulos de Python sin importar el directorio de trabajo. |
| **Publicación en Pull Requests** | Se intentaba publicar en cada disparo | Se condicionó con `if: github.event_name == 'push' && github.ref == 'refs/heads/main'` | Evita que un Pull Request (código en revisión no aprobado) genere o sobreescriba imágenes en producción. |

---

## 🛠️ Explicación Detallada de los 6 Errores del Tutorial y sus Soluciones

### 1. Error de Permisos (`403 Forbidden` / `denied: permission_denied`)

* **Problema del Video**:
  En tutoriales antiguos se asumía que `secrets.GITHUB_TOKEN` tenía permisos totales de escritura en el registro de paquetes.
* **Causa**:
  GitHub actualizó la seguridad global y ahora asigna permisos de solo lectura por defecto a los flujos de trabajo.
* **Solución Aplicada**:
  En [`.github/workflows/ci-cd.yml`](file:///.github/workflows/ci-cd.yml) incluimos explícitamente:
  ```yaml
  permissions:
    contents: read
    packages: write
  ```

---

### 2. Error de Formato Docker (`invalid reference format: repository name must be lowercase`)

* **Problema del Video**:
  Si el nombre de usuario de GitHub o el repositorio contiene mayúsculas (por ejemplo `Franklincordoba2001-ops/CI_CD`), usar directamente `ghcr.io/${{ github.repository }}` hace que Docker falle.
* **Causa**:
  La especificación oficial de nombres de imagen de Docker prohíbe caracteres en mayúscula.
* **Solución Aplicada**:
  Creamos un paso que transforma el texto antes de compilar:
  ```yaml
  - name: Convertir Nombre de Repositorio a Minúsculas
    id: prep
    run: |
      REPO_LOWER=$(echo "${{ github.repository }}" | tr '[:upper:]' '[:lower:]')
      IMAGE_TAG="ghcr.io/${REPO_LOWER}"
      echo "image_tag=${IMAGE_TAG}" >> $GITHUB_OUTPUT
  ```

---

### 3. Versiones Obsoletas de GitHub Actions (`Node 12/16 Deprecation`)

* **Problema del Video**:
  El video utiliza versiones antiguas como `actions/checkout@v2` o `actions/setup-python@v2`.
* **Causa**:
  GitHub Actions retiró las versiones antiguas de Node.js en los servidores virtuales (*runners*).
* **Solución Aplicada**:
  Actualizamos todas las acciones a sus versiones más recientes y estables de 2026:
  * `actions/checkout@v4`
  * `actions/setup-python@v5`
  * `docker/setup-buildx-action@v3`
  * `docker/login-action@v3`
  * `docker/build-push-action@v5`

---

### 4. Error de Importación de Módulos en Python (`ModuleNotFoundError`)

* **Problema del Video**:
  Al organizar la estructura en carpetas `app/` y `tests/`, ejecutar `pytest` o `python app/main.py` directamente falla porque Python no encuentra la ruta raíz del paquete.
* **Solución Aplicada**:
  * Incluimos `ENV PYTHONPATH=/app` en el [`Dockerfile`](file:///Dockerfile).
  * Incluimos resolución dinámica de ruta en [`app/main.py`](file:///app/main.py) y paquetes `__init__.py`.

---

### 5. Fallos de Linteado (`Flake8`) Rompiendo el Pipeline

* **Problema del Video**:
  Si no se configura una tolerancia de longitud de línea o reglas ignoradas, `flake8` detiene el proceso por detalles estéticos menores.
* **Solución Aplicada**:
  Creamos el archivo de configuración [`.flake8`](file:///.flake8) definiendo `max-line-length = 100` y exclusiones claras (`.git`, `__pycache__`, `venv`).

---

### 6. Publicación Innecesaria en Pull Requests

* **Problema del Video**:
  El job de compilación Docker se ejecutaba sin verificar si los cambios pertenecían a una rama en revisión (PR) o a la rama principal aprobada (`main`).
* **Solución Aplicada**:
  Añadimos la regla condicional en el job `build-and-push`:
  ```yaml
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
  ```

---

## 📝 Estructura Recomendada para tu Documentación Final / Presentación

Si necesitas presentar este proyecto o defender la documentación ante tu profesor o equipo, utiliza este esquema:

1. **Introducción**: Definición de CI/CD e importancia en la automatización de software moderno.
2. **Arquitectura del Pipeline**: Explicación de los dos jobs (`lint-and-test` y `build-and-push`).
3. **Mejoras y Correcciones Técnicas**: Explicación de por qué se actualizaron las versiones de Actions, los permisos de `GITHUB_TOKEN` y la conversión de minúsculas para Docker.
4. **Guía de Pruebas Locales**: Comandos para probar con `flake8`, `pytest` y `docker build`.
5. **Resultado Final**: Publicación exitosa de la imagen en **GitHub Container Registry (GHCR)**.
