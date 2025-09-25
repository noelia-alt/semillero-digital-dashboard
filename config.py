from pydantic_settings import BaseSettings  #  Pydantic v2 usa este paquete

class Settings(BaseSettings):
    google_client_id: str
    google_client_secret: str
    secret_key: str

    class Config:
        # archivo de variables de entorno
        env_file = ".env"
        # (opcional) codificación del archivo
        env_file_encoding = "utf-8"

# crea una instancia global que usarás en main.py
settings = Settings()
