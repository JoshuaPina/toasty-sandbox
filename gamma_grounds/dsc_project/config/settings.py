# ccds_app/config/settings.py
# Import into any module with: from ccds_app.config.settings import APP_SETTINGS

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """
    Manages all environment variables and dynamic settings.
    Loads from .env file by default.
    """
    model_config = SettingsConfigDict(
        env_file='.env', 
        env_file_encoding='utf-8'
    )

    # --- Environment Variables ---
    # RANDOM_SEED is an int, defaults to 42
    RANDOM_SEED: int = Field(default=42)
    
    # DEBUG_MODE is a boolean (Pydantic handles the 'True'/'False' conversion)
    DEBUG_MODE: bool = Field(default=False) 

    # WEATHER_API_KEY is an optional string (None if not set)
    WEATHER_API_KEY: Optional[str] = Field(default=None)


# Instantiate and export the settings object for use throughout the app
APP_SETTINGS = Settings()

