# config.py
from pydantic_settings import BaseSettings  # Pydantic v2 usa este paquete

class Settings(BaseSettings):
    """
    Configuración global cargada desde .env
    """
    google_client_id: str
    google_client_secret: str
    secret_key: str
    redirect_uri: str  # URI de redirección autorizada en Google Cloud

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# instancia global que se importa en main.py
settings = Settings()
