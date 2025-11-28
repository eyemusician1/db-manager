"""
Application configuration settings
"""
import os


class Settings:
    """Application settings and configuration"""
    
    # Database connection settings
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_USER = os.getenv('DB_USER', 'admin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # Backup settings
    BACKUP_DIR = os.getenv('BACKUP_DIR', './backups')
    AUTO_BACKUP_ENABLED = True
    COMPRESSION_TYPE = 'gzip'  # Options: gzip, zip, None
    
    # Application settings
    THEME = 'dark'  # Options: dark, light
    LOG_LEVEL = 'INFO'
    LOG_DIR = './logs'
    
    @classmethod
    def get(cls, key, default=None):
        """Get configuration value"""
        return getattr(cls, key, default)
