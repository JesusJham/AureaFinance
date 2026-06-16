# 🚀 Guía de Despliegue - AureaFinance

## Requisitos Previos

- Cuenta en [Vercel](https://vercel.com) (para Frontend)
- Cuenta en [Render](https://render.com) (para Backend)
- Cuenta en [Neon](https://neon.tech) (Base de datos PostgreSQL)
- Repositorio Git (GitHub, GitLab o Gitbucket)

---

## 📱 FRONTEND - Vercel

### Paso 1: Preparar el repositorio

```bash
# Asegúrate de que todo esté en Git
git add .
git commit -m "Preparación para despliegue"
git push origin main
```

### Paso 2: Conectar Vercel

1. Ve a [vercel.com](https://vercel.com)
2. Haz clic en **"New Project"**
3. Selecciona tu repositorio (autoriza si es necesario)
4. En **Project settings**:
   - **Framework Preset**: `Other` (es un sitio estático)
   - **Root Directory**: `./` (raíz del proyecto)
   - **Build Command**: `echo "Frontend estático"`
   - **Output Directory**: `.` (actual)

### Paso 3: Configurar variables de entorno

En el dashboard de Vercel, ve a **Settings → Environment Variables**:

```
API_BASE_URL = https://tu-backend-render.onrender.com/api
```

(Reemplaza con tu URL real de Render)

### Paso 4: Deploy

Haz clic en **Deploy**. Vercel debería desplegar automáticamente.

### Verificación

- URL de Vercel: `https://tu-proyecto.vercel.app`
- Abre la URL y verifica que la aplicación carga

---

## ⚙️ BACKEND - Render

### Paso 1: Preparar el backend

Asegúrate de que tu `requirements.txt` esté actualizado:

```bash
cd backend
pip freeze > requirements.txt
```

### Paso 2: Conectar Render

1. Ve a [render.com](https://render.com)
2. Haz clic en **"New +"** → **"Web Service"**
3. Conecta tu repositorio GitHub
4. Llena los datos:
   - **Name**: `aurea-finance-api`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: `Python 3.11`

### Paso 3: Configurar variables de entorno

En Render, ve a **Settings → Environment Variables** y agrega:

```
DEBUG = false
SECRET_KEY = (genera una clave segura de al menos 32 caracteres)
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALLOWED_ORIGINS = ["https://project-wk0hp.vercel.app"]
DATABASE_URL = postgresql://usuario:password@host/basedatos?sslmode=require
```

**Importante**: El `DATABASE_URL` debe venir de tu dashboard de Neon.

### Paso 4: Deploy

Haz clic en **Create Web Service**. Render desplegará automáticamente.

### Verificación

- URL de Render: `https://tu-backend-render.onrender.com`
- Abre `https://tu-backend-render.onrender.com/docs` para ver la documentación de FastAPI
- Verifica que todos los endpoints funcionan

---

## 🔗 Conectar Frontend y Backend

### 1. Actualizar CORS en backend

En `backend/main.py`, asegúrate de que CORS incluya tu dominio Vercel:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tu-proyecto.vercel.app"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Actualizar URL de API en frontend

El archivo `frontend/assets/js/config.js` detecta automáticamente:
- Si estás en `localhost` → usa `http://localhost:8000/api`
- Si estás en producción → usa la URL de Render

Asegúrate de actualizar la URL en `config.js`:

```javascript
window.API_BASE_URL = 'https://tu-backend-render.onrender.com/api';
```

### 3. Prueba la conexión

1. Abre tu frontend en Vercel
2. Intenta hacer login
3. Verifica en la consola del navegador (F12) que se conecta al backend correcto

---

## 🗄️ Base de Datos - Neon PostgreSQL

### Ya configurado ✅

Tu `DATABASE_URL` ya viene de Neon. Solo asegúrate de:

1. Que la conexión incluya `?sslmode=require` (necesario para Neon)
2. Que la contraseña sea correcta en el `.env.example`
3. Que no expongas credenciales en GitHub

---

## 🔒 Seguridad - Checklist

- [ ] **SECRET_KEY**: Cambiar a una clave aleatoria de 32+ caracteres
- [ ] **DEBUG**: Siempre `false` en producción
- [ ] **ALLOWED_ORIGINS**: Actualizar a tu dominio de Vercel
- [ ] **.env**: Nunca subir a GitHub (ya está en `.gitignore`)
- [ ] **DATABASE_URL**: Configurar como variable secreta en Render (no en código)

---

## 🆘 Solucionar problemas

### El frontend no conecta al backend

1. Verifica que `API_BASE_URL` sea correcto en `config.js`
2. Verifica que CORS esté configurado en el backend
3. Abre DevTools (F12) → Network → verifica las llamadas a la API

### Error 500 en el backend

1. Ve a Render → Logs → revisa los errores
2. Verifica que `DATABASE_URL` sea válido
3. Asegúrate de que Neon esté funcionando

### Timeout en Neon

- Neon puede hibernar después de inactividad (plan gratuito)
- Hace una llamada a la API para activarlo
- Luego debería funcionar

---

## 📊 URLs finales

Después del despliegue, tendrás:

- **Frontend**: `https://tu-proyecto.vercel.app`
- **Backend API**: `https://tu-backend-render.onrender.com`
- **Docs API**: `https://tu-backend-render.onrender.com/docs`
- **Base de datos**: Neon PostgreSQL

---

## 🔄 Despliegues futuros

Cada vez que hagas `push` a `main`:

1. **Vercel** despliega automáticamente el frontend
2. **Render** despliega automáticamente el backend

No hay que hacer nada más. ¡Automatizado! 🎉
