# 🚀 Pipeline de CI/CD con GitHub Actions, Docker y Python

![CI/CD Pipeline](https://github.com/franklincordoba2001-ops/ci_cd/actions/workflows/ci-cd.yml/badge.svg)

Este proyecto implementa un pipeline completo de **Integración Continua y Despliegue Continuo (CI/CD)** utilizando **GitHub Actions**, **Docker** y **GitHub Container Registry (GHCR)** para una aplicación desarrollada en **Python**, siguiendo la arquitectura del tutorial de Emilio Carrión (*Product Crafter*).

---

## 📋 Tabla de Contenidos
1. [Descripción General](#-descripción-general)
2. [Estructura del Proyecto](#-estructura-del-proyecto)
3. [Requisitos Previos](#-requisitos-previos)
4. [Ejecución Local](#-ejecución-local)
   - [Instalación de Dependencias](#1-instalación-de-dependencias)
   - [Ejecutar la Aplicación](#2-ejecutar-la-aplicación)
   - [Ejecutar Análisis Estático (Flake8)](#3-ejecutar-análisis-estático-flake8)
   - [Ejecutar Pruebas Unitarias (Pytest)](#4-ejecutar-pruebas-unitarias-pytest)
5. [Contenedorización con Docker](#-contenedorización-con-docker)
6. [Flujo del Pipeline CI/CD en GitHub Actions](#-flujo-del-pipeline-cicd-en-github-actions)
7. [⚠️ Análisis de Errores Comunes y Soluciones](#️-análisis-de-errores-comunes-y-soluciones)
8. [📚 Guía para Documentar Proyectos CI/CD](#-guía-para-documentar-proyectos-cicd)

---

## 📖 Descripción General

El objetivo de este proyecto es automatizar el ciclo de vida del desarrollo de software:
- **Linting (Flake8)**: Garantiza que el código cumpla con los estándares de estilo PEP 8.
- **Testing (Pytest)**: Ejecuta pruebas unitarias automatizadas en cada cambio de código.
- **Build & Push (Docker + GHCR)**: Construye la imagen de contenedor y la publica automáticamente en **GitHub Container Registry (`ghcr.io`)** únicamente cuando las pruebas y el linteado han sido exitosos en la rama principal (`main`).

---

## 📁 Estructura del Proyecto

```
ci_cd/
├── app/
│   ├── __init__.py          # Convierte app en un paquete de Python
│   ├── calculator.py        # Módulo de lógica de negocio (operaciones matemáticas)
│   └── main.py              # Punto de entrada principal de la aplicación
├── tests/
│   ├── __init__.py          # Paquete de pruebas unitarias
│   └── test_calculator.py   # Pruebas con pytest
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # Definición del pipeline automatizado en GitHub Actions
├── .flake8                  # Reglas de linteado para Flake8
├── .gitignore               # Exclusión de archivos temporales y entornos virtuales
├── Dockerfile               # Configuración del contenedor Docker (Python 3.11-slim)
├── requirements.txt         # Lista de dependencias del proyecto
└── README.md                # Documentación oficial del proyecto
```

---

## 🔧 Requisitos Previos

- **Python 3.11+** instalado.
- **Docker Desktop** (opcional, para construir y probar contenedores localmente).
- Cuenta en **GitHub** con repositorio remoto.

---

## 💻 Ejecución Local

### 1. Instalación de Dependencias
Crea un entorno virtual y ejecuta:
```bash
pip install -r requirements.txt
```

### 2. Ejecutar la Aplicación
```bash
python app/main.py
```

### 3. Ejecutar Análisis Estático (Flake8)
```bash
flake8 app/ tests/
```
*Si la salida está vacía, significa que no hay errores de estilo PEP 8.*

### 4. Ejecutar Pruebas Unitarias (Pytest)
```bash
pytest --verbose
```

---

## 🐳 Contenedorización con Docker

### Construir la imagen localmente:
```bash
docker build -t mi-app-python:latest .
```

### Ejecutar el contenedor:
```bash
docker run --rm mi-app-python:latest
```

---

## ⚙️ Flujo del Pipeline CI/CD en GitHub Actions

El archivo [`.github/workflows/ci-cd.yml`](file:///.github/workflows/ci-cd.yml) se divide en dos **Jobs**:

### Job 1: `lint-and-test`
Se ejecuta en cada `push` y `pull_request` hacia la rama `main`:
1. Hace checkout del repositorio (`actions/checkout@v4`).
2. Configura Python 3.11 con caché de `pip` (`actions/setup-python@v5`).
3. Instala dependencias (`requirements.txt`).
4. Corre `flake8` para detectar violaciones de código.
5. Corre `pytest` para validar todas las pruebas unitarias.

### Job 2: `build-and-push`
Se ejecuta únicamente si `lint-and-test` termina con éxito y el evento es un `push` a `main`:
1. Hace checkout del código.
2. Convierte el nombre del repositorio a minúsculas (exigencia de GHCR).
3. Inicia sesión en GitHub Container Registry (`ghcr.io`) usando `docker/login-action@v3` y el token automático `secrets.GITHUB_TOKEN`.
4. Construye y publica la imagen Docker usando `docker/build-push-action@v5` etiquetándola como `:latest` y con el hash corto del commit (`:${{ steps.prep.outputs.sha_short }}`).

---

## ⚠️ Análisis de Errores Comunes y Soluciones

A continuación se detallan los principales errores que suelen ocurrir al configurar este pipeline de CI/CD y cómo corregirlos:

### ❌ Error 1: Permisos Insuficientes en `GITHUB_TOKEN` (`403 Forbidden` / `denied: permission_denied`)
- **Síntoma**: El paso de Docker login o push a GHCR falla con el mensaje `denied: permission_denied` o `403 Forbidden`.
- **Causa**: Por defecto, los workflows de GitHub Actions se ejecutan con permisos de solo lectura para el `GITHUB_TOKEN`.
- **Solución**:
  1. En el repositorio de GitHub, ve a **Settings -> Actions -> General -> Workflow permissions** y marca **"Read and write permissions"**.
  2. En el archivo `.github/workflows/ci-cd.yml`, incluye explícitamente el bloque de permisos:
     ```yaml
     permissions:
       contents: read
       packages: write
     ```

---

### ❌ Error 2: Nombre del Repositorio con Mayúsculas en Docker Registry (`invalid reference format: repository name must be lowercase`)
- **Síntoma**: La construcción o publicación del contenedor falla indicando formato inválido.
- **Causa**: Las imágenes de Docker en registros como GHCR (`ghcr.io/usuario/repositorio`) **exigen estrictamente letras minúsculas**, pero el repositorio de GitHub puede contener mayúsculas (ej: `Usuario/Mi_Proyecto`).
- **Solución**: Agregar un paso previo que transforme `${{ github.repository }}` a minúsculas usando `tr '[:upper:]' '[:lower:]'`:
  ```yaml
  - name: Convertir Nombre a Minúsculas
    id: prep
    run: |
      REPO_LOWER=$(echo "${{ github.repository }}" | tr '[:upper:]' '[:lower:]')
      echo "image_tag=ghcr.io/${REPO_LOWER}" >> $GITHUB_OUTPUT
  ```

---

### ❌ Error 3: Fallos en la etapa de Linting (`flake8`) bloquean la publicación
- **Síntoma**: El pipeline se cancela en la etapa de `Lint & Test` y no llega a construir la imagen Docker.
- **Causa**: `flake8` detecta errores de formato como líneas muy largas (>100 caracteres), importaciones no usadas o espacios innecesarios.
- **Solución**:
  - Ajustar el archivo `.flake8` según los criterios del equipo.
  - Ejecutar `flake8` localmente antes de hacer `git push`.

---

### ❌ Error 4: `ModuleNotFoundError` en Python en los Tests o en el Contenedor
- **Síntoma**: Pytest o Python reportan `ModuleNotFoundError: No module named 'app'`.
- **Causa**: La ruta base de la aplicación no está agregada al `PYTHONPATH` cuando se ejecutan los scripts fuera del directorio raíz.
- **Solución**:
  - En el `Dockerfile`, configurar la variable de entorno: `ENV PYTHONPATH=/app`.
  - En la aplicación, incluir archivos `__init__.py` en cada carpeta de paquetes.

---

### ❌ Error 5: Intentar publicar la imagen Docker en Pull Requests (`push: true` descontrolado)
- **Síntoma**: Se generan imágenes incompletas o no aprobadas en el registro de contenedores durante la revisión de un Pull Request.
- **Causa**: El job de `build-and-push` no valida si la rama actual es la rama de producción (`main`).
- **Solución**: Incluir la condición `if` en el job `build-and-push`:
  ```yaml
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
  ```

---

## 📚 Guía para Documentar Proyectos CI/CD

Para crear una documentación profesional en tus proyectos de CI/CD:

1. **Diagrama o Explicación Arquitectónica**: Explica qué desencadena el pipeline (triggers), qué herramientas se usan y dónde se despliega el resultado.
2. **Requisitos y Configuración de Entorno**: Especifica versiones de herramientas y variables de entorno/secretos requeridos (`GITHUB_TOKEN`, llaves de acceso).
3. **Instrucciones para Probar Localmente**: Muestra siempre cómo correr los tests y el linteado en la máquina del desarrollador antes de subir cambios.
4. **Sección de Troubleshooting (Diagnóstico de Errores)**: Enumera los errores comunes del pipeline (permisos, sintaxis YAML, fallos de contenedor) con sus respectivas soluciones.
5. **Insignia de Estado (Badge de GitHub Actions)**: Agrega un badge al inicio de tu `README.md` para mostrar el estado del pipeline en tiempo real:
   ```markdown
   ![CI/CD Pipeline](https://github.com/franklincordoba2001-ops/ci_cd/actions/workflows/ci-cd.yml/badge.svg)
   ```
