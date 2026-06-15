// Configuración dinámmica de la API base URL
// Se puede sobrescribir con window.API_BASE_URL
if (!window.API_BASE_URL) {
  // Detectar automáticamente si está en desarrollo o producción
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    window.API_BASE_URL = 'http://localhost:8000/api';
  } else {
    // En producción, reemplaza con tu URL de Render
    window.API_BASE_URL = 'https://aurea-finance-api.onrender.com/api';
  }
}

console.log('API Base URL:', window.API_BASE_URL);
