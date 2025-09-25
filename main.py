# main.py
from datetime import datetime, timezone
from urllib.parse import urlencode

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from config import settings   # 👈 importamos la configuración global

# -----------------------------
# Google OAuth scopes
# -----------------------------
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.rosters.readonly",
    "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly",
]

# -----------------------------
# FastAPI app
# -----------------------------
app = FastAPI(title="Semillero Digital Dashboard")
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
templates = Jinja2Templates(directory="templates")

# -----------------------------
# Google OAuth helpers
# -----------------------------
def _client_config():
    return {
        "web": {
            "client_id": settings.google_client_id,
            "project_id": "semillero-digital-dashboard",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": settings.google_client_secret,
            "redirect_uris": [settings.redirect_uri],
        }
    }

def build_flow(state: str | None = None):
    return Flow.from_client_config(
        _client_config(),
        scopes=SCOPES,
        redirect_uri=settings.redirect_uri,
        state=state,
    )

def get_creds_from_session(request: Request) -> Credentials:
    data = request.session.get("google_creds")
    if not data:
        raise HTTPException(status_code=401, detail="No autenticado")
    creds = Credentials.from_authorized_user_info(data, SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh_request = None
    return creds

def classroom_service(creds: Credentials):
    return build("classroom", "v1", credentials=creds)

def people_service(creds: Credentials):
    return build("people", "v1", credentials=creds)

# -----------------------------
# OAuth routes
# -----------------------------
@app.get("/login")
def login(request: Request):
    next_url = request.query_params.get("next", "/")
    state = urlencode({"next": next_url})
    flow = build_flow(state=state)
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )
    return RedirectResponse(auth_url)

@app.get("/oauth/callback")
def oauth_callback(request: Request, state: str | None = None, code: str | None = None):
    if not code:
        raise HTTPException(status_code=400, detail="Falta 'code' en callback")

    try:
        flow = build_flow(state=state)
        flow.fetch_token(code=code)
        creds = flow.credentials

        # guardamos en sesión
        request.session["google_creds"] = {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": creds.scopes,
            "expiry": creds.expiry.isoformat() if creds.expiry else None,
        }

        # Mejorar el parsing del state para evitar problemas de URL encoding
        next_url = "/dashboard"
        if state:
            try:
                from urllib.parse import parse_qs, unquote
                # Decodificar el state y extraer el parámetro next
                decoded_state = unquote(state)
                params = parse_qs(decoded_state)
                if "next" in params:
                    next_url = params["next"][0]
            except Exception:
                # Si hay error en el parsing, usar dashboard por defecto
                next_url = "/dashboard"
        
        return RedirectResponse(next_url)
    
    except Exception as e:
        # En caso de error, redirigir al login con mensaje de error
        return RedirectResponse("/login?error=oauth_failed")

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/")

# -----------------------------
# Helpers
# -----------------------------
def to_dt(dueDate: dict | None, dueTime: dict | None) -> datetime | None:
    if not dueDate:
        return None
    y, m, d = dueDate.get("year"), dueDate.get("month"), dueDate.get("day")
    hh = (dueTime or {}).get("hours", 23)
    mm = (dueTime or {}).get("minutes", 59)
    if not (y and m and d):
        return None
    return datetime(y, m, d, hh, mm, tzinfo=timezone.utc)

def classify_submission(sub, coursework):
    state = sub.get("state", "ASSIGNED")
    due = to_dt(coursework.get("dueDate"), coursework.get("dueTime"))
    updated = sub.get("updateTime")
    turned_in = None
    if updated:
        try:
            turned_in = datetime.fromisoformat(updated.replace("Z", "+00:00"))
        except Exception:
            pass

    if state == "RETURNED":
        return "reentrega"
    if state == "TURNED_IN":
        if due and turned_in and turned_in > due:
            return "atrasado"
        return "entregado"
    if due and datetime.now(timezone.utc) > due:
        return "faltante"
    return "faltante"

# -----------------------------
# API endpoints básicos
# -----------------------------
@app.get("/me")
def me(request: Request):
    creds = get_creds_from_session(request)
    prof = people_service(creds).people().get(
        resourceName="people/me",
        personFields="names,emailAddresses,photos"
    ).execute()
    name = (prof.get("names") or [{}])[0].get("displayName")
    email = (prof.get("emailAddresses") or [{}])[0].get("value")
    return {"name": name, "email": email}

@app.get("/courses")
def list_courses(request: Request):
    creds = get_creds_from_session(request)
    svc = classroom_service(creds)
    courses, page = [], None
    while True:
        resp = svc.courses().list(pageToken=page, pageSize=100).execute()
        courses += resp.get("courses", [])
        page = resp.get("nextPageToken")
        if not page:
            break
    return {"courses": courses}

# -----------------------------
# Dashboard route
# -----------------------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    try:
        # Verificar que el usuario esté autenticado
        creds = get_creds_from_session(request)
        return HTMLResponse("""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Semillero Digital</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .logout-btn { background: #dc3545; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px; }
        .success { background: #d4edda; color: #155724; padding: 15px; border-radius: 4px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Dashboard - Semillero Digital</h1>
            <a href="/logout" class="logout-btn">Cerrar Sesión</a>
        </div>
        <div class="success">
            ¡Autenticación exitosa! Bienvenido al dashboard.
        </div>
        <p>Tu sesión OAuth con Google está activa.</p>
        <p><a href="/me">Ver mi información</a> | <a href="/courses">Ver mis cursos</a></p>
    </div>
</body>
</html>
        """)
    except HTTPException:
        # Si no está autenticado, redirigir al login
        return RedirectResponse("/login")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return HTMLResponse(
        "<h2>Semillero Digital Dashboard</h2>"
        "<p><a href='/login'>Login con Google</a> | <a href='/dashboard'>Ver dashboard</a></p>"
        "<p>Documentación: <a href='/docs'>/docs</a></p>"
    )
