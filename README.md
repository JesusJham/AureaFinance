# Aurea Finance — Plataforma de Carga y Gestión de Datos

## Estructura del proyecto

```
aurea-finance/
├── frontend/               # Páginas HTML estáticas
│   ├── pages/              # Vistas de la app
│   └── assets/             # CSS, JS e imágenes
└── backend/                # API REST en Python (FastAPI)
    ├── main.py
    ├── requirements.txt
    └── app/
        ├── api/routes/     # Endpoints REST
        ├── core/           # Config, BD, seguridad
        ├── models/         # Modelos SQLAlchemy
        ├── schemas/        # Esquemas Pydantic
        └── services/       # Lógica de negocio
```

## Requisitos

- Python 3.11+
- ODBC Driver 17 for SQL Server (para conectar a SQL Server)

## Inicio rápido — Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # edita las variables
uvicorn main:app --reload
```

La API queda disponible en `http://localhost:8000`  
Documentación interactiva: `http://localhost:8000/docs`

## Inicio rápido — Frontend

Abre `frontend/pages/login.html` con Live Server (VS Code) o cualquier servidor estático.

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | /api/auth/register | Registrar usuario |
| POST | /api/auth/login | Iniciar sesión |
| GET | /api/servidores/ | Listar servidores |
| POST | /api/servidores/ | Crear servidor |
| POST | /api/servidores/{id}/test | Probar conexión |
| GET | /api/cargas/ | Listar cargas |
| POST | /api/cargas/ | Crear configuración de carga |
| POST | /api/cargas/validar | Validar archivo (CSV/XLSX/TXT) |
| POST | /api/cargas/{id}/ejecutar | Ejecutar carga |

## Tests

```bash
cd backend
pytest tests/ -v
```
