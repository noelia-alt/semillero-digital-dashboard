# Semillero Digital Dashboard

Un dashboard completo para visualizar y gestionar información de Google Classroom, diseñado específicamente para el programa Semillero Digital.

## 🚀 Características

### 📊 **Dashboard Principal**
- **Autenticación OAuth 2.0** con Google Classroom
- **Dashboard interactivo** con 4 vistas principales:
  - Estado de entregas por estudiante
  - Lista completa de estudiantes y su progreso
  - Información de profesores y cursos asignados
  - Resumen detallado de cursos activos
- **Filtros avanzados** por cohorte, profesor y estado de entrega
- **Visualizaciones gráficas** interactivas con Chart.js
- **Exportación de datos** a CSV

### 🔔 **Sistema de Notificaciones Automáticas**
- **Notificaciones por email** con templates HTML profesionales
- **Verificación automática** de nuevas tareas cada hora
- **Recordatorios inteligentes** 24 horas antes del vencimiento
- **Configuración personalizable** por usuario
- **Notificaciones de prueba** para testing
- **Soporte futuro** para WhatsApp y Telegram

### 📈 **Reportes Gráficos Avanzados**
- **Métricas de rendimiento** por cohorte en tiempo real
- **Gráficos interactivos**: barras apiladas y donut charts
- **Estadísticas detalladas**: % entregas a tiempo vs tardías
- **Tablas de progreso** con visualización de barras
- **Exportación** de reportes

### 📅 **Módulo de Asistencia**
- **Integración con Google Calendar** para próximas clases
- **Filtrado automático** de eventos relacionados con educación
- **Vista especializada** para profesores y coordinadores
- **Información completa** de eventos: horario, ubicación, asistentes

### 👥 **Sistema de Roles y Permisos Inteligente**
- **Detección automática** de roles basada en participación en cursos
- **Cuatro roles con jerarquía**:
  - 🔴 **Administrador**: Dueño de cursos o enseña en 5+ cursos
  - 🟡 **Coordinador**: Enseña en 2+ cursos
  - 🟢 **Profesor**: Enseña en al menos 1 curso
  - 🔵 **Estudiante**: Inscrito como estudiante en cursos
  - ⚪ **Invitado**: Sin participación activa
- **Sistema de permisos jerárquico**: Roles superiores heredan permisos de inferiores
- **Funcionalidades por rol**:
  - **Administrador**: Acceso total, gestión de caché, notificaciones avanzadas
  - **Coordinador**: Reportes avanzados, verificación manual de notificaciones
  - **Profesor**: Dashboard completo, notificaciones básicas
  - **Estudiante**: Vista limitada a sus propias entregas
  - **Invitado**: Solo información básica
- **Badges visuales** que muestran el rol activo con colores distintivos

### 🎨 **Interfaz Moderna**
- **Bootstrap 5** con diseño responsivo
- **Bootstrap Icons** para una experiencia visual rica
- **Navegación intuitiva** por pestañas
- **Animaciones suaves** y efectos hover
- **Tema consistente** en todas las páginas

## 📋 Requisitos

- Python 3.8+
- Cuenta de Google con acceso a Google Classroom
- Proyecto en Google Cloud Console con APIs habilitadas

## 🛠️ Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd Proyecto-semillero-dashboard
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar Google Cloud Console**
   - Crear un proyecto en [Google Cloud Console](https://console.cloud.google.com/)
   - Habilitar las APIs:
     - Google Classroom API
     - People API
   - Crear credenciales OAuth 2.0 con estos **scopes obligatorios**:
     - `openid`
     - `https://www.googleapis.com/auth/userinfo.email`
     - `https://www.googleapis.com/auth/userinfo.profile`
     - `https://www.googleapis.com/auth/classroom.courses.readonly`
     - `https://www.googleapis.com/auth/classroom.rosters.readonly`
     - `https://www.googleapis.com/auth/classroom.student-submissions.students.readonly`
   - Configurar URI de redirección: `http://localhost:5001/oauth/callback`

4. **Configurar variables de entorno**
   Crear un archivo `.env` en la raíz del proyecto:
   ```env
   GOOGLE_CLIENT_ID=tu_client_id_aqui
   GOOGLE_CLIENT_SECRET=tu_client_secret_aqui
   SECRET_KEY=una_clave_secreta_muy_segura_aqui
   REDIRECT_URI=http://localhost:5001/oauth/callback
   
   # Configuración opcional para notificaciones por email
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=tu_email@gmail.com
   SMTP_PASSWORD=tu_password_de_aplicacion
   FROM_EMAIL=noreply@semillerodigital.com
   ```

## 🚀 Uso

1. **Ejecutar la aplicación**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 5001
   ```

2. **Acceder al dashboard**
   - Abrir navegador en `http://localhost:5001`
   - Hacer clic en "Login con Google"
   - Autorizar el acceso a Google Classroom
   - Explorar el dashboard

## 🌟 Páginas y Funcionalidades

### 📊 Dashboard Principal (`/dashboard`)
- Vista general con 4 pestañas: Entregas, Estudiantes, Profesores, Cursos
- Filtros dinámicos por cohorte, profesor y estado
- Gráficos de progreso por estudiante
- Exportación de datos a CSV

### 📈 Reportes Avanzados (`/reports`)
- Métricas de rendimiento en tiempo real
- Gráficos de barras y donut interactivos
- Estadísticas por cohorte: % entregas a tiempo
- Próximas clases (para profesores/coordinadores)
- Tablas detalladas con barras de progreso

### 🔔 Configuración de Notificaciones (`/notifications`)
- Configuración personalizable de notificaciones
- Envío de notificaciones de prueba
- Verificación manual de nuevas tareas (profesores/coordinadores)
- Historial de notificaciones

### 👤 Perfil de Usuario (`/me`)
- Información personal del usuario
- Rol automáticamente detectado
- Foto de perfil de Google

## 📊 Funcionalidades del Dashboard

### Vista de Entregas
- Tabla completa con todas las entregas
- **Estados completos de Google Classroom**:
  - ✅ **Entregado**: Tarea entregada a tiempo (`TURNED_IN`)
  - ⏰ **Entregado Tarde**: Tarea entregada después de la fecha límite (`TURNED_IN` + tardía)
  - 🔄 **Devuelta**: Tarea devuelta por el profesor para corrección (`RETURNED`)
  - 🚧 **En Progreso**: Estudiante trabajando en la tarea (`CREATED`)
  - ⚠️ **En Progreso Tarde**: Trabajando pero ya venció (`CREATED` + tardía)
  - 📋 **Asignada**: Tarea recién asignada, aún hay tiempo (`NEW`)
  - ❌ **No Entregada**: Tarea no entregada y ya venció (`NEW` + tardía)
  - 🔙 **Retirada**: Estudiante retiró su entrega (`RECLAIMED_BY_STUDENT`)
  - ⏰ **Retirada Tarde**: Retirada después del vencimiento (`RECLAIMED_BY_STUDENT` + tardía)

### Vista de Estudiantes
- Lista completa de estudiantes registrados
- Barra de progreso visual por estudiante
- Información de contacto y cursos asignados

### Vista de Profesores
- Lista de todos los profesores
- Cursos que imparten
- Información de contacto

### Vista de Cursos
- Tarjetas informativas de cada curso
- Estadísticas: número de estudiantes, profesores y tareas
- Descripción del curso

## 🔧 API Endpoints

### Autenticación
- `GET /login` - Iniciar proceso de autenticación
- `GET /oauth/callback` - Callback de OAuth
- `GET /logout` - Cerrar sesión

### Datos de Usuario
- `GET /me` - Información del usuario autenticado

### Datos de Classroom
- `GET /courses` - Lista de cursos
- `GET /students/{course_id}` - Estudiantes de un curso
- `GET /teachers/{course_id}` - Profesores de un curso
- `GET /coursework/{course_id}` - Tareas de un curso
- `GET /submissions/{course_id}/{coursework_id}` - Entregas de una tarea

### Dashboard
- `GET /dashboard` - Vista principal del dashboard
- `GET /dashboard-direct` - Dashboard directo sin redirecciones
- `GET /dashboard-simple-emails` - Dashboard enfocado en obtener emails
- `GET /dashboard-all-courses` - Dashboard con todos los cursos
- `GET /dashboard-force-real` - Dashboard forzando acceso a cursos reales

### Reportes
- `GET /reports` - Página de reportes avanzados
- `GET /reports-clean` - Reportes con datos reales filtrados

### Debugging y Diagnóstico
- `GET /debug-oauth` - Diagnosticar configuración OAuth
- `GET /debug-courses` - Análisis detallado de cursos y roles
- `GET /debug-students` - Debug específico de estudiantes y emails
- `GET /test-real-emails` - Probar métodos para obtener emails reales

## 🎨 Tecnologías Utilizadas

- **Backend**: FastAPI, Python
- **Frontend**: HTML5, Bootstrap 5, Chart.js
- **Autenticación**: Google OAuth 2.0
- **APIs**: Google Classroom API, People API
- **Base de datos**: Sesiones en memoria (para demo)

## 📝 Configuración de Filtros

El dashboard permite filtrar información usando los siguientes parámetros:

- **Cohorte**: Filtrar por nombre del curso
- **Email del profesor**: Mostrar solo cursos de un profesor específico
- **Estado de entrega**: Filtrar entregas por su estado

## 🔒 Seguridad

- Autenticación OAuth 2.0 segura
- Tokens de sesión encriptados
- Variables de entorno para credenciales sensibles
- Validación de permisos de Google Classroom

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Si tienes problemas o preguntas:

1. Revisa la documentación de [Google Classroom API](https://developers.google.com/classroom)
2. Verifica que las APIs estén habilitadas en Google Cloud Console
3. Asegúrate de que las variables de entorno estén configuradas correctamente
4. Revisa los logs de la aplicación para errores específicos

## ✅ Funcionalidades Implementadas

- ✅ **Dashboard completo** con 4 vistas principales
- ✅ **Sistema de notificaciones** por email con templates HTML
- ✅ **Reportes gráficos avanzados** con Chart.js
- ✅ **Exportación CSV** de datos
- ✅ **Filtros avanzados** por curso, profesor y estado
- ✅ **Integración completa** con Google Classroom API
- ✅ **Sistema de roles automático** (Estudiante, Profesor, Coordinador, Admin)
- ✅ **Autenticación OAuth 2.0** segura
- ✅ **Interfaz responsive** con Bootstrap 5
- ✅ **Scheduler automático** para verificaciones periódicas

## 🎯 Problemas Resueltos

Este dashboard resuelve los **3 problemas centrales** identificados en Semillero Digital:

### 1. ✅ **Seguimiento del progreso de estudiantes**
- **Vista consolidada** del avance por alumno, clase y profesor
- **Dashboard interactivo** con filtros avanzados
- **Estados detallados** de entregas en tiempo real
- **Exportación de datos** para análisis adicional

### 2. ✅ **Comunicación clara**
- **Sistema de notificaciones automáticas** por email
- **Templates HTML profesionales** para comunicaciones
- **Recordatorios inteligentes** 24h antes del vencimiento
- **Verificación periódica** de nuevas tareas cada hora

### 3. ✅ **Métricas ágiles**
- **Reportes en tiempo real** con gráficos interactivos
- **Extracción automática** de datos desde Google Classroom
- **Visualizaciones avanzadas** (barras, donut charts, tablas)
- **Exportación CSV** para el equipo coordinador

## 📈 Roadmap Futuro

- [ ] Integración con base de datos persistente (PostgreSQL/MySQL)
- [ ] Notificaciones por WhatsApp y Telegram
- [ ] Integración con Google Drive para archivos
- [ ] Dashboard móvil nativo
- [ ] API REST completa para integraciones
- [ ] Tests automatizados (pytest)
- [ ] Deployment en la nube (AWS/GCP)
- [ ] Módulo de asistencia con reconocimiento facial
