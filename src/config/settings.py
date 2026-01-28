"""
Application Settings

Centralized configuration management using Pydantic Settings.
Loads from environment variables with sensible defaults.
"""

import os
from pathlib import Path
from typing import Optional
from functools import lru_cache


class Settings:
    """
    Application settings with environment variable support.
    
    Usage:
        settings = Settings()
        api_key = settings.GOOGLE_API_KEY
    """
    
    def __init__(self):
        # API Keys
        self.GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
        
        # Paths
        self.BASE_DIR: Path = Path(__file__).parent.parent.parent
        self.MODEL_PATH: str = os.getenv("MODEL_PATH", str(self.BASE_DIR / "data" / "models"))
        self.DATA_PATH: str = os.getenv("DATA_PATH", str(self.BASE_DIR / "data"))
        self.LOG_PATH: str = os.getenv("LOG_PATH", str(self.BASE_DIR / "logs"))
        
        # Model files
        self.RISK_MODEL_PATH: str = os.path.join(self.MODEL_PATH, "risk_model.pkl")
        self.GOAL_MODEL_PATH: str = os.path.join(self.MODEL_PATH, "goal_model.pkl")
        self.RISK_SCALER_PATH: str = os.path.join(self.MODEL_PATH, "risk_scaler.pkl")
        
        # Data files
        self.PRODUCT_CATALOG_PATH: str = os.path.join(self.DATA_PATH, "products.csv")
        self.PROSPECT_DATA_PATH: str = os.path.join(self.DATA_PATH, "prospects.csv")
        
        # LLM Configuration
        self.LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-pro")
        self.LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.3"))
        self.LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "2048"))
        self.LLM_TIMEOUT: int = int(os.getenv("LLM_TIMEOUT", "30"))
        
        # Processing
        self.MAX_CONCURRENT: int = int(os.getenv("MAX_CONCURRENT", "5"))
        self.BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "10"))
        
        # Cache
        self.LLM_CACHE_TTL: int = int(os.getenv("LLM_CACHE_TTL", "300"))
        self.ML_CACHE_TTL: int = int(os.getenv("ML_CACHE_TTL", "3600"))
        
        # Logging
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FORMAT: str = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}"
        
        # Streamlit
        self.STREAMLIT_PORT: int = int(os.getenv("STREAMLIT_PORT", "8501"))
        
    def validate(self) -> bool:
        """
        Validate critical settings.
        
        Returns:
            True if all critical settings are valid
        """
        issues = []
        
        if not self.GOOGLE_API_KEY:
            issues.append("GOOGLE_API_KEY is not set")
        
        if not Path(self.MODEL_PATH).exists():
            issues.append(f"MODEL_PATH does not exist: {self.MODEL_PATH}")
        
        if issues:
            for issue in issues:
                print(f"Warning: {issue}")
            return False
        
        return True
    
    def to_dict(self) -> dict:
        """Convert settings to dictionary (excluding sensitive data)"""
        return {
            "LLM_MODEL": self.LLM_MODEL,
            "LLM_TEMPERATURE": self.LLM_TEMPERATURE,
            "LLM_TIMEOUT": self.LLM_TIMEOUT,
            "MAX_CONCURRENT": self.MAX_CONCURRENT,
            "LOG_LEVEL": self.LOG_LEVEL,
            "MODEL_PATH": self.MODEL_PATH,
            "DATA_PATH": self.DATA_PATH,
        }


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings singleton instance
    """
    return Settings()


# Convenience function
def load_settings() -> Settings:
    """Load and return settings"""
    return get_settings()
