# 📋 Archivos generados para despliegue

## Archivos NUEVOS creados ✨

### Frontend (Vercel)
```
├── vercel.json                          ← Configuración de Vercel
├── frontend/
│   ├── .env.local.example              ← Variables de ejemplo para desarrollo
│   └── assets/js/
│       └── config.js                   ← Configuración dinámica de API URL
├── index.html (actualizado)            ← Ahora incluye config.js
```

### Backend (Render)
```
├── Dockerfile                           ← Para containerizar la app
├── render.yaml                         ← Configuración de Render (opcional)
├── backend/
│   ├── RENDER_ENV_VARS.txt            ← Variables de entorno a copiar
│   └── .env.example (actualizado)     ← Ejemplo completo de variables
```

### Documentación
```
├── DEPLOYMENT.md                        ← Guía paso a paso completa
└── .gitignore (actualizado)            ← Archivos a ignorar
```

---

## ✅ Checklist antes de desplegar

### Paso 1: Preparar repositorio
- [ ] Actualizar `backend/requirements.txt` (run: `pip freeze > backend/requirements.txt`)
- [ ] Verificar que todos los archivos estén en Git
- [ ] Hacer commit: `git add . && git commit -m "Preparación para despliegue"`
- [ ] Push: `git push origin main`

### Paso 2: Configurar Frontend (Vercel)
- [ ] Crear cuenta en https://vercel.com
- [ ] Conectar tu repositorio GitHub
- [ ] En Vercel Settings → Environment Variables:
  ```
  API_BASE_URL = https://tu-backend-render.onrender.com/api
  ```
- [ ] Habilitar auto-deploy en cada push

### Paso 3: Configurar Backend (Render)
- [ ] Crear cuenta en https://render.com
- [ ] Crear nuevo Web Service
- [ ] Root Directory: `backend`
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] En Environment Variables, agregar todas las variables de RENDER_ENV_VARS.txt

### Paso 4: Configurar Base de Datos
- [ ] Verificar DATABASE_URL en Neon (desde neon.tech)
- [ ] Copiar URL completa en Render environment variables
- [ ] Incluir `?sslmode=require` en la URL

### Paso 5: Conectar Frontend con Backend
- [ ] Actualizar `ALLOWED_ORIGINS` en Backend con tu URL de Vercel
- [ ] Actualizar `config.js` con tu URL de Render
- [ ] Probar que el login funciona

---

## 🔐 Variables de Entorno - IMPORTANTE

### Para el Backend (en Render):
Usar `RENDER_ENV_VARS.txt` como referencia, pero ACTUALIZAR:
- `SECRET_KEY` → Generar una aleatoria segura
- `DATABASE_URL` → Obtener de tu dashboard Neon
- `ALLOWED_ORIGINS` → Tu URL de frontend en Vercel

### Para el Frontend (en Vercel):
Solo necesita:
- `API_BASE_URL` → Tu URL de backend en Render

**NUNCA** subir `.env` a Git (ya está en `.gitignore`)

---

## 📊 Resumen de tecnologías

| Componente | Tecnología | Despliegue |
|-----------|-----------|-----------|
| Frontend | HTML/CSS/JavaScript | Vercel (gratis) |
| Backend | FastAPI + Python | Render (gratis) |
| BD | PostgreSQL | Neon (gratis) |
| ORM | SQLAlchemy | ✓ |
| Auth | JWT + PyJWT | ✓ |

---

## 🚀 Después del primer despliegue

Cada vez que hagas un cambio:

```bash
# 1. Hacer cambios en el código
# 2. Commit y push
git add .
git commit -m "Descripción del cambio"
git push origin main

# 3. Vercel y Render despliegan automáticamente
# ¡Listo! Sin hacer nada más 🎉
```

---

## 🆘 Soporta y recursos

- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **Neon Docs**: https://neon.tech/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com

Ver `DEPLOYMENT.md` para guía detallada.
