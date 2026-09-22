# Canhuel SRL - Sistema de Gestión de Repartos (v1.0.0)

Una aplicación web progresiva y moderna diseñada para que los choferes de Canhuel SRL puedan registrar rápidamente sus remitos, cargas de combustible y gastos generales desde su teléfono móvil, y para que la administración pueda visualizar, filtrar y descargar estos comprobantes en tiempo real.

## 🚀 Características Principales (v1.0.0)

### Para el Chofer (Frontend Móvil)
- **Selección Rápida:** Ingreso mediante perfil de chofer (sin contraseñas complejas para agilizar el trabajo en ruta).
- **Carga de Comprobantes:** Soporte para tres categorías de registros:
  - **Remitos:** Detalle de lugar de carga, destino, empresa y número de remito.
  - **Combustible:** Registro de litros cargados.
  - **Gastos Generales:** Registro del importe gastado.
- **Evidencia Fotográfica:** Opción para subir hasta 2 fotos por registro, ya sea tomando la foto en el momento con la cámara del celular o eligiendo desde la galería.
- **Diseño Adaptable:** Interfaz moderna, rápida y "Glassmorphism", optimizada para uso con una sola mano en dispositivos móviles.

### Para la Administración (Panel de Control)
- **Dashboard Centralizado:** Tabla en vivo con todos los registros enviados por la flota.
- **Filtros Avanzados:** Búsqueda cruzada por Chofer, Categoría y Rango de Fechas (basado en el momento exacto en que el sistema recibió el registro en hora de Argentina).
- **Detalle Integral:** Visualización de toda la metadata del gasto y acceso a la descarga de las imágenes originales en alta resolución guardadas de forma segura.

## 🛠 Arquitectura y Tecnologías

El sistema está dividido en dos aplicaciones independientes:

### Backend (API REST)
- **Framework:** FastAPI (Python 3.12+).
- **Base de Datos:** PostgreSQL alojada en **Supabase** (usando *Transaction Pooler* por IPv4).
- **ORM:** SQLAlchemy 2.0 (usando el driver `psycopg3`).
- **Almacenamiento (Storage):** Supabase Storage Privado (acceso mediante URLs firmadas temporalmente por seguridad).
- **Alojamiento:** Desplegado en **Render** (Web Service).

### Frontend (SPA)
- **Framework:** React 18 (construido con Vite).
- **Enrutamiento:** React Router DOM (Single Page Application).
- **Estilos:** Vanilla CSS moderno con variables CSS puras.
- **Alojamiento:** Desplegado en **Vercel** (con reglas de reescritura configuradas en `vercel.json` para soportar navegación del lado del cliente).

## 📦 Estructura del Proyecto

```
delivery-managment/
├── backend/                  # API en FastAPI
│   ├── app/
│   │   ├── database/         # Configuración y conexión a PostgreSQL (Supabase)
│   │   ├── models/           # Tablas de SQLAlchemy (drivers, records, etc.)
│   │   ├── routers/          # Endpoints de la API
│   │   ├── schemas/          # Validaciones de Pydantic
│   │   └── services/         # Lógica de negocio (CRUD y filtros con Timezones)
│   ├── render.yaml           # Configuración de despliegue para Render
│   └── requirements.txt      # Dependencias de Python
└── frontend/                 # Aplicación en React
    ├── src/
    │   ├── api.js            # Cliente HTTP para conectarse al backend
    │   ├── pages/            # Vistas principales (DriverLogin, RecordForm, AdminDashboard)
    │   └── index.css         # Sistema de diseño, colores y animaciones
    ├── vercel.json           # Configuración de rutas para Vercel
    └── package.json          # Dependencias de Node.js
```

## ⚙️ Configuración y Despliegue

### Variables de Entorno Requeridas

**Para el Backend (Render):**
- `DATABASE_URL`: URL de conexión a Supabase (Pooler port 6543).
- `SUPABASE_URL`: URL del proyecto de Supabase.
- `SUPABASE_KEY`: Clave de servicio (Service Role Key) de Supabase para poder generar URLs firmadas del Storage.

**Para el Frontend (Vercel):**
- `VITE_API_URL`: URL pública del backend en Render (ej. `https://canhuel-api.onrender.com`).

---
*Desarrollado para la gestión logística de Canhuel SRL.*
