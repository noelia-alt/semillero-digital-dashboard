# 🎓 EduFlow Dashboard - Semillero Digital

<p align="center">
  <img src="images/LOGO.png" alt="EduFlow Logo" width="150"/>
</p>

**EduFlow: Optimizando el flujo de Trabajo, información y comunicación en el ecosistema educativo de Semillero Digital.**

---

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

**Demo en vivo:** [https://semillero-digital-dashboard.onrender.com](https://semillero-digital-dashboard.onrender.com)

Un dashboard de análisis y gestión en tiempo real para Google Classroom, diseñado para potenciar la experiencia educativa de Semillero Digital con automatización, métricas avanzadas y una interfaz profesional.

## 🖼️ Galería del Proyecto

<table>
  <tr>
    <td align="center"><strong>Página de Inicio</strong></td>
    <td align="center"><strong>Dashboard Principal</strong></td>
  </tr>
  <tr>
    <td><img src="images/HOME.png" alt="Página de Inicio de EduFlow"></td>
    <td><img src="images/DASHBOARD.png" alt="Dashboard Principal de EduFlow"></td>
  </tr>
  <tr>
    <td align="center"><strong>Reportes Avanzados</strong></td>
    <td align="center"><strong>Gestión de Notificaciones</strong></td>
  </tr>
  <tr>
    <td><img src="images/REPORTES.png" alt="Sección de Reportes de EduFlow"></td>
    <td><img src="images/NOTIFICACIONES.png" alt="Sección de Notificaciones de EduFlow"></td>
  </tr>
</table>

## 🛠️ Tecnologías Utilizadas

| Categoría | Tecnologías |
| :--- | :--- |
| **Backend** | Python, FastAPI, APScheduler |
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js, Jinja2 |
| **APIs y Autenticación** | Google Classroom API, Google People API, Google Calendar API, OAuth 2.0 |
| **Despliegue** | Docker, Render, Gunicorn |
| **Base de Datos** | En memoria (para sesiones y caché) |

## 🚀 Setup Guide - Configuración Completa

### Step 1: Google Cloud Console Setup ⚠️ **CRÍTICO**

Esta es la parte más importante. Sigue estos pasos cuidadosamente:

#### 1.1 Create Google Cloud Project
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Haz clic en "Select a project" → "New Project"
3. Ingresa el nombre del proyecto: `semillero-digital-dashboard`
4. Haz clic en "Create"
5. Espera a que se cree el proyecto y selecciónalo

#### 1.2 Enable Required APIs
1. Ve a **APIs & Services** → **Library**
2. Busca y habilita estas APIs:
   - **Google Classroom API** ⚠️ **CRÍTICO**
   - **Google People API** (para perfiles de usuario)
3. Haz clic en "Enable" para cada API

#### 1.3 Configure OAuth Consent Screen
⚠️ **Este paso es esencial para evitar errores 403 access_denied**

1. Ve a **APIs & Services** → **OAuth consent screen**
2. Elige "External" user type (a menos que tengas Google Workspace)
3. Completa la información de la aplicación:
   - **App name:** Semillero Digital Dashboard
   - **User support email:** Tu dirección de email
   - **App logo:** Opcional
   - **App domain:** Dejar en blanco para desarrollo
   - **Developer contact information:** Tu dirección de email
4. Haz clic en "Save and Continue"
5. **Agregar Scopes** (Haz clic en "Add or Remove Scopes"):
   ```
   https://www.googleapis.com/auth/classroom.courses.readonly
   https://www.googleapis.com/auth/classroom.rosters.readonly
   https://www.googleapis.com/auth/classroom.student-submissions.students.readonly
   https://www.googleapis.com/auth/userinfo.email
   https://www.googleapis.com/auth/userinfo.profile
   openid
   ```
6. Haz clic en "Update" → "Save and Continue"
7. **Agregar Test Users** (para desarrollo):
   - Agrega tu dirección de email
   - Agrega cualquier otro usuario que necesite acceso durante el desarrollo
8. Haz clic en "Save and Continue"
9. Revisa y haz clic en "Back to Dashboard"

#### 1.4 Create OAuth 2.0 Credentials
1. Ve a **APIs & Services** → **Credentials**
2. Haz clic en "+ Create Credentials" → "OAuth 2.0 Client IDs"
3. Elige "Web application"
4. **Name:** Semillero Digital Dashboard
5. **Authorized redirect URIs** - Agrega las URIs EXACTAS, por ejemplo:
   ```
   http://localhost:5001/oauth/callback
   http://127.0.0.1:5001/oauth/callback
   https://tu-dominio.on.render.com/oauth/callback
   ```
6. Haz clic en "Create"
7. **IMPORTANTE:** Copia el Client ID y Client Secret inmediatamente

#### 1.5 Environment Configuration
Edita el archivo `.env` con tus credenciales de Google:

```bash
# Google OAuth Configuration (from Step 1.4)
GOOGLE_CLIENT_ID=856042286573-your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your-client-secret
SECRET_KEY=tu-clave-secreta-muy-larga-y-aleatoria
REDIRECT_URI=http://localhost:5001/oauth/callback
```

### 🚨 Common Issues & Solutions

#### Issue: `AttributeError: 'Config' object has no attribute 'GOOGLE_CLIENT_ID'`
**Solution:** Variables de entorno no se cargan correctamente
```bash
# Verificar formato del archivo .env (sin comillas, sin espacios alrededor de =)
cat .env
```

#### Issue: `Error 403: access_denied`
**Causas y Soluciones:**
1. **OAuth consent screen no configurado**
   - Completa el Step 1.3 arriba
   - Agrega tu email como test user
2. **URI de redirección incorrecta**
   - Asegúrate de que coincida exactamente: `http://localhost:5001/oauth/callback`
   - Verifica el número de puerto (5001)
3. **APIs no habilitadas**
   - Habilita Google Classroom API en Google Cloud Console

#### Issue: `localhost redirected you too many times`
**Solution:** Limpiar datos del navegador
```bash
# Chrome/Safari: Cmd + Shift + Delete
# O usar ventana incógnito/privada
# Reiniciar la aplicación
```

#### Issue: `The credentials do not contain the necessary fields`
**Solution:** Re-autenticarse para obtener refresh token
1. Limpiar cookies del navegador completamente
2. Reiniciar la aplicación
3. Pasar por el flujo OAuth nuevamente
4. La aplicación ahora fuerza el consentimiento para obtener credenciales apropiadas

#### Issue: `Scope mismatch errors`
**Solution:** Ya corregido en el código
- La aplicación usa flujo OAuth consistente
- Scopes simplificados para evitar conflictos
- Limpiar caché del navegador si aún ves este error

### 🔒 Security Notes
- Nunca hagas commit del archivo `.env` al control de versiones
- Usa una `SECRET_KEY` fuerte en producción
- Configura URIs de redirección OAuth apropiadas para tu dominio

## 🚀 Despliegue y Configuración

### 1. Despliegue con Render
La forma más sencilla de desplegar este proyecto es usando el botón "Deploy to Render". Render clonará el repositorio y usará el `Dockerfile` para construir y desplegar la aplicación automáticamente.

### 2. Configuración de Variables de Entorno
Para que la aplicación funcione, debes configurar las siguientes variables de entorno en tu servicio de hosting (ej. Render):

#### Credenciales de Google:
- `GOOGLE_CLIENT_ID`: El Client ID de tu aplicación en Google Cloud Console.
- `GOOGLE_CLIENT_SECRET`: El Client Secret correspondiente.
- `SECRET_KEY`: Una clave secreta larga y aleatoria para firmar las sesiones.
- `REDIRECT_URI`: La URL de callback de OAuth (ej: `https://tu-app.on.render.com/oauth/callback`).

#### Configuración de Notificaciones por Email (SMTP):
Para que el envío de emails funcione, necesitas configurar un servidor SMTP.

| Variable | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `MAIL_USERNAME` | Tu dirección de correo (Gmail, etc.) | `tu.email@gmail.com` |
| `MAIL_PASSWORD` | **Contraseña de Aplicación** generada | `abcd efgh ijkl mnop` |
| `MAIL_FROM` | El mismo email que el username | `tu.email@gmail.com` |
| `MAIL_SERVER` | Servidor SMTP | `smtp.gmail.com` |
| `MAIL_PORT` | Puerto del servidor (TLS) | `587` |
| `MAIL_TLS` | Habilitar TLS | `True` |
| `MAIL_SSL` | Habilitar SSL | `False` |

> **Nota sobre la Contraseña de Aplicación:** Si usas Gmail con verificación en dos pasos, debes generar una "Contraseña de Aplicación" desde la configuración de seguridad de tu cuenta de Google. No uses tu contraseña principal.
