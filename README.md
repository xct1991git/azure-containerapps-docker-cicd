# CI/CD y Contenerización de Microservicios con Docker, Trivy y GitHub Container Registry (GHCR)

Pipeline automatizado de integración continua (CI) para empaquetado seguro de microservicios contenerizados, escaneo estático de vulnerabilidades y publicación de artefactos en GHCR con especificación de infraestructura para Azure Container Apps.

---

## Arquitectura y Flujo del Pipeline

El objetivo principal de este flujo es garantizar que ningún artefacto llegue a un registro de contenedores ni a producción con vulnerabilidades críticas o malas prácticas de seguridad:

1. **Construcción Aislada:** Generación de la imagen del contenedor mediante Docker Buildx a partir de un Dockerfile optimizado y sin privilegios de administrador.
2. **Auditoría de Vulnerabilidades (Shift-Left):** Escaneo de capas del sistema operativo y dependencias de la aplicación utilizando Aqua Security Trivy.
3. **Control de Artefactos:** Publicación y versionado semántico automatizado en GitHub Container Registry (`ghcr.io`) bajo autenticación.
4. **Infraestructura como Código (IaC):** Especificación modular en Terraform (`infra/main.tf`) preparada para aprovisionar el entorno serverless en Azure Container Apps dentro de la capa de consumo gratuito.

---

## Stack Tecnológico

| Componente | Tecnología | Rol en el Proyecto |
| :--- | :--- | :--- |
| **Aplicación** | FastAPI (Python 3.11) | Microservicio ligero con endpoints de métricas y healthcheck |
| **Contenedor** | Docker | Contenedorización multi-capa con usuario no privilegiado |
| **Escáner de Seguridad** | Trivy | Análisis de vulnerabilidades CVE (OS y librerías de aplicación) |
| **Registro de Imágenes** | GitHub Container Registry (GHCR) | Almacenamiento seguro y versionado de imágenes Docker |
| **Infraestructura** | HashiCorp Terraform | Definición IaC para el entorno de Azure Container Apps |
| **Automatización** | GitHub Actions | Orquestación completa del ciclo CI |

---

## Fases del Flujo de Trabajo CI

El pipeline configurado en `.github/workflows/container-ci.yml` se activa ante cada `push` o `pull_request` sobre la rama `main`:

```text
[ Git Push / Pull Request ]
            │
            ▼
    [ Docker Buildx ] ──────────► Compila la imagen en local
            │
            ▼
    [ Trivy Scanner ] ──────────► Audita paquetes (Bloquea/Reporta CVEs)
            │
            ▼
   [ Docker Login GHCR ] ───────► Autenticación mediante GITHUB_TOKEN
            │
            ▼
    [ Metadata Action ] ────────► Genera tags (latest y commit SHA)
            │
            ▼
     [ Push to GHCR ] ──────────► Publicación en GitHub Packages
