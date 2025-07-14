import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv() # Load environment variables from .env file

        # Server Configuration
        self.SERVER_HOST = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
        self.SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", 5000))
        self.DEBUG = os.getenv("MCP_DEBUG", "False").lower() == "true"
        self.SECRET_KEY = os.getenv("MCP_SECRET_KEY", "super-secret-key")

        # Logging
        self.LOG_LEVEL = os.getenv("MCP_LOG_LEVEL", "INFO").upper()
        self.LOG_FILE = os.getenv("MCP_LOG_FILE", "logs/mcp_server.log")

        # Storage
        self.STORAGE_PATH = os.getenv("MCP_STORAGE_PATH", "data/projects")
        self.DATABASE_PATH = os.getenv("MCP_DATABASE_PATH", "src/database/app.db")

        # Overleaf Integration (Optional)
        self.OVERLEAF_EMAIL = os.getenv("OVERLEAF_EMAIL")
        self.OVERLEAF_PASSWORD = os.getenv("OVERLEAF_PASSWORD")
        self.OVERLEAF_API_URL = os.getenv("OVERLEAF_API_URL", "https://www.overleaf.com" )

        # Security
        self.ALLOWED_ORIGINS = os.getenv("MCP_ALLOWED_ORIGINS", "*")
        self.MAX_REQUEST_SIZE = int(os.getenv("MCP_MAX_REQUEST_SIZE", 10485760))
        self.RATE_LIMIT = int(os.getenv("MCP_RATE_LIMIT", 100))

        # MCP Protocol
        self.protocol_version = "1.1.0"
        self.mcp_server_name = "overleaf-remote-mcp"
        self.mcp_server_version = "1.0.0"
        self.log_level = self.LOG_LEVEL

    def get_storage_path(self):
        """Get the storage path for project files."""
        return self.STORAGE_PATH

    def is_overleaf_configured(self):
        """Check if Overleaf credentials are configured."""
        return bool(self.OVERLEAF_EMAIL and self.OVERLEAF_PASSWORD)

