# notifications.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any
import logging
from config import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.smtp_server = getattr(settings, 'smtp_server', 'smtp.gmail.com')
        self.smtp_port = getattr(settings, 'smtp_port', 587)
        self.smtp_username = getattr(settings, 'smtp_username', '')
        self.smtp_password = getattr(settings, 'smtp_password', '')
        self.from_email = getattr(settings, 'from_email', 'noreply@semillerodigital.com')
    
    def send_email(self, to_email: str, subject: str, html_content: str):
        """Enviar email usando smtplib estándar"""
        try:
            # Verificar que las credenciales estén configuradas
            if not self.smtp_username or not self.smtp_password:
                logger.warning("⚠️ Credenciales SMTP no configuradas. Simulando envío de email.")
                print(f"📧 SIMULACIÓN - Email a {to_email}: {subject}")
                return True
            
            # Crear mensaje
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.from_email
            message["To"] = to_email
            
            # Agregar contenido HTML
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Enviar email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(message)
            
            logger.info(f"✅ Email enviado exitosamente a {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error enviando email a {to_email}: {e}")
            print(f"📧 SIMULACIÓN (error) - Email a {to_email}: {subject}")
            return False
    
    def send_test_notification(self, to_email: str, user_name: str):
        """Enviar notificación de prueba"""
        subject = "🔔 Notificación de Prueba - Semillero Digital"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; color: #2c3e50; margin-bottom: 30px; }}
                .content {{ color: #34495e; line-height: 1.6; }}
                .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #7f8c8d; font-size: 14px; }}
                .button {{ display: inline-block; padding: 12px 24px; background-color: #3498db; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎓 Semillero Digital Dashboard</h1>
                    <h2>Notificación de Prueba</h2>
                </div>
                
                <div class="content">
                    <p>¡Hola <strong>{user_name}</strong>!</p>
                    
                    <p>Esta es una notificación de prueba para verificar que el sistema de notificaciones está funcionando correctamente.</p>
                    
                    <p><strong>✅ ¡Configuración exitosa!</strong></p>
                    
                    <p>Tu sistema de notificaciones está listo para:</p>
                    <ul>
                        <li>🆕 Notificar sobre nuevas tareas</li>
                        <li>⏰ Recordatorios antes del vencimiento</li>
                        <li>📊 Actualizaciones de calificaciones</li>
                        <li>📅 Recordatorios de clases</li>
                    </ul>
                    
                    <p>Fecha y hora: <strong>{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</strong></p>
                </div>
                
                <div class="footer">
                    <p>Este email fue enviado automáticamente por el Dashboard de Semillero Digital</p>
                    <p>No responder a este mensaje</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, html_content)

# Instancia global del servicio de notificaciones
notification_service = NotificationService()

# Funciones auxiliares para compatibilidad
def check_new_assignments():
    """Verificar nuevas tareas (placeholder)"""
    print("🔍 Verificando nuevas tareas...")
    return []

def check_due_reminders():
    """Verificar recordatorios de vencimiento (placeholder)"""
    print("⏰ Verificando recordatorios de vencimiento...")
    return []
    
    def create_assignment_notification_html(self, assignment_data: Dict[str, Any]) -> str:
        """Crear HTML para notificación de nueva tarea"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #0d6efd; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background: #f8f9fa; }}
                .assignment {{ background: white; padding: 15px; border-left: 4px solid #0d6efd; margin: 10px 0; }}
                .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
                .btn {{ display: inline-block; padding: 10px 20px; background: #0d6efd; color: white; text-decoration: none; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎓 Nueva Tarea Asignada</h1>
                </div>
                <div class="content">
                    <h2>¡Hola!</h2>
                    <p>Se ha asignado una nueva tarea en tu curso:</p>
                    
                    <div class="assignment">
                        <h3>{assignment_data.get('title', 'Sin título')}</h3>
                        <p><strong>Curso:</strong> {assignment_data.get('course_name', 'N/A')}</p>
                        <p><strong>Descripción:</strong> {assignment_data.get('description', 'Sin descripción')}</p>
                        <p><strong>Fecha límite:</strong> {assignment_data.get('due_date', 'Sin fecha límite')}</p>
                    </div>
                    
                    <p>No olvides completar tu tarea antes de la fecha límite.</p>
                    <a href="https://classroom.google.com" class="btn">Ver en Google Classroom</a>
                </div>
                <div class="footer">
                    <p>Este es un mensaje automático del Sistema Semillero Digital</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def create_reminder_notification_html(self, reminder_data: Dict[str, Any]) -> str:
        """Crear HTML para recordatorio de tarea"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #ffc107; color: #212529; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background: #fff3cd; }}
                .assignment {{ background: white; padding: 15px; border-left: 4px solid #ffc107; margin: 10px 0; }}
                .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
                .btn {{ display: inline-block; padding: 10px 20px; background: #ffc107; color: #212529; text-decoration: none; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⏰ Recordatorio de Entrega</h1>
                </div>
                <div class="content">
                    <h2>¡No olvides tu tarea!</h2>
                    <p>Tienes una tarea próxima a vencer:</p>
                    
                    <div class="assignment">
                        <h3>{reminder_data.get('title', 'Sin título')}</h3>
                        <p><strong>Curso:</strong> {reminder_data.get('course_name', 'N/A')}</p>
                        <p><strong>Fecha límite:</strong> {reminder_data.get('due_date', 'Sin fecha límite')}</p>
                        <p><strong>Estado:</strong> {reminder_data.get('status', 'Pendiente')}</p>
                    </div>
                    
                    <p>Te recomendamos completar tu tarea lo antes posible.</p>
                    <a href="https://classroom.google.com" class="btn">Completar Tarea</a>
                </div>
                <div class="footer">
                    <p>Este es un mensaje automático del Sistema Semillero Digital</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    async def send_assignment_notification(self, student_email: str, assignment_data: Dict[str, Any]):
        """Enviar notificación de nueva tarea"""
        subject = f"Nueva tarea: {assignment_data.get('title', 'Sin título')}"
        
        body = f"""
        ¡Hola!
        
        Se ha asignado una nueva tarea en tu curso:
        
        Título: {assignment_data.get('title', 'Sin título')}
        Curso: {assignment_data.get('course_name', 'N/A')}
        Fecha límite: {assignment_data.get('due_date', 'Sin fecha límite')}
        
        No olvides completar tu tarea antes de la fecha límite.
        
        Saludos,
        Sistema Semillero Digital
        """
        
        html_body = self.create_assignment_notification_html(assignment_data)
        
        return await self.send_email(student_email, subject, body, html_body)
    
    async def send_reminder_notification(self, student_email: str, reminder_data: Dict[str, Any]):
        """Enviar recordatorio de tarea"""
        subject = f"Recordatorio: {reminder_data.get('title', 'Tarea pendiente')}"
        
        body = f"""
        ¡No olvides tu tarea!
        
        Tienes una tarea próxima a vencer:
        
        Título: {reminder_data.get('title', 'Sin título')}
        Curso: {reminder_data.get('course_name', 'N/A')}
        Fecha límite: {reminder_data.get('due_date', 'Sin fecha límite')}
        Estado: {reminder_data.get('status', 'Pendiente')}
        
        Te recomendamos completar tu tarea lo antes posible.
        
        Saludos,
        Sistema Semillero Digital
        """
        
        html_body = self.create_reminder_notification_html(reminder_data)
        
        return await self.send_email(student_email, subject, body, html_body)
    
    async def send_bulk_notifications(self, notifications: List[Dict[str, Any]]):
        """Enviar múltiples notificaciones de forma asíncrona"""
        tasks = []
        
        for notification in notifications:
            if notification['type'] == 'assignment':
                task = self.send_assignment_notification(
                    notification['email'], 
                    notification['data']
                )
            elif notification['type'] == 'reminder':
                task = self.send_reminder_notification(
                    notification['email'], 
                    notification['data']
                )
            
            tasks.append(task)
        
        # Ejecutar todas las notificaciones en paralelo
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        successful = sum(1 for result in results if result is True)
        failed = len(results) - successful
        
        logger.info(f"Notificaciones enviadas: {successful} exitosas, {failed} fallidas")
        
        return {"successful": successful, "failed": failed}

# Instancia global del servicio de notificaciones
notification_service = NotificationService()

def check_new_assignments(classroom_service, last_check_time: datetime) -> List[Dict[str, Any]]:
    """Verificar nuevas tareas desde la última verificación"""
    new_assignments = []
    
    try:
        # Obtener todos los cursos
        courses_response = classroom_service.courses().list(pageSize=100).execute()
        courses = courses_response.get("courses", [])
        
        for course in courses:
            course_id = course["id"]
            course_name = course.get("name", "Sin nombre")
            
            try:
                # Obtener tareas del curso
                coursework_response = classroom_service.courses().courseWork().list(
                    courseId=course_id
                ).execute()
                coursework_items = coursework_response.get("courseWork", [])
                
                for coursework in coursework_items:
                    # Verificar si la tarea es nueva (creada después de la última verificación)
                    creation_time_str = coursework.get("creationTime")
                    if creation_time_str:
                        creation_time = datetime.fromisoformat(creation_time_str.replace("Z", "+00:00"))
                        
                        if creation_time > last_check_time:
                            # Obtener estudiantes del curso
                            try:
                                students_response = classroom_service.courses().students().list(
                                    courseId=course_id
                                ).execute()
                                students = students_response.get("students", [])
                                
                                # Crear notificación para cada estudiante
                                for student in students:
                                    student_email = student.get("profile", {}).get("emailAddress")
                                    if student_email:
                                        new_assignments.append({
                                            "type": "assignment",
                                            "email": student_email,
                                            "data": {
                                                "title": coursework.get("title", "Sin título"),
                                                "course_name": course_name,
                                                "description": coursework.get("description", "Sin descripción"),
                                                "due_date": coursework.get("dueDate", "Sin fecha límite"),
                                                "creation_time": creation_time_str
                                            }
                                        })
                            
                            except Exception as e:
                                logger.error(f"Error obteniendo estudiantes del curso {course_id}: {e}")
                                continue
            
            except Exception as e:
                logger.error(f"Error obteniendo tareas del curso {course_id}: {e}")
                continue
    
    except Exception as e:
        logger.error(f"Error verificando nuevas tareas: {e}")
    
    return new_assignments

def check_due_reminders(classroom_service) -> List[Dict[str, Any]]:
    """Verificar tareas próximas a vencer (24 horas antes)"""
    reminders = []
    tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
    
    try:
        # Obtener todos los cursos
        courses_response = classroom_service.courses().list(pageSize=100).execute()
        courses = courses_response.get("courses", [])
        
        for course in courses:
            course_id = course["id"]
            course_name = course.get("name", "Sin nombre")
            
            try:
                # Obtener tareas del curso
                coursework_response = classroom_service.courses().courseWork().list(
                    courseId=course_id
                ).execute()
                coursework_items = coursework_response.get("courseWork", [])
                
                for coursework in coursework_items:
                    due_date_dict = coursework.get("dueDate")
                    if due_date_dict:
                        try:
                            due_date = datetime(
                                due_date_dict.get("year"),
                                due_date_dict.get("month"),
                                due_date_dict.get("day"),
                                tzinfo=timezone.utc
                            )
                            
                            # Verificar si vence mañana
                            if due_date.date() == tomorrow.date():
                                coursework_id = coursework["id"]
                                
                                # Obtener entregas para verificar estado
                                try:
                                    submissions_response = classroom_service.courses().courseWork().studentSubmissions().list(
                                        courseId=course_id,
                                        courseWorkId=coursework_id
                                    ).execute()
                                    submissions = submissions_response.get("studentSubmissions", [])
                                    
                                    # Obtener estudiantes del curso
                                    students_response = classroom_service.courses().students().list(
                                        courseId=course_id
                                    ).execute()
                                    students = students_response.get("students", [])
                                    
                                    # Crear recordatorios para estudiantes con tareas pendientes
                                    for student in students:
                                        student_id = student.get("userId")
                                        student_email = student.get("profile", {}).get("emailAddress")
                                        
                                        if student_email and student_id:
                                            # Buscar la entrega del estudiante
                                            student_submission = next(
                                                (sub for sub in submissions if sub.get("userId") == student_id),
                                                None
                                            )
                                            
                                            # Solo enviar recordatorio si no ha entregado
                                            if not student_submission or student_submission.get("state") in ["CREATED", "NEW"]:
                                                reminders.append({
                                                    "type": "reminder",
                                                    "email": student_email,
                                                    "data": {
                                                        "title": coursework.get("title", "Sin título"),
                                                        "course_name": course_name,
                                                        "due_date": due_date.strftime("%d/%m/%Y"),
                                                        "status": "Pendiente"
                                                    }
                                                })
                                
                                except Exception as e:
                                    logger.error(f"Error verificando entregas para tarea {coursework_id}: {e}")
                                    continue
                        
                        except (TypeError, ValueError) as e:
                            logger.error(f"Error procesando fecha límite: {e}")
                            continue
            
            except Exception as e:
                logger.error(f"Error obteniendo tareas del curso {course_id}: {e}")
                continue
    
    except Exception as e:
        logger.error(f"Error verificando recordatorios: {e}")
    
    return reminders
