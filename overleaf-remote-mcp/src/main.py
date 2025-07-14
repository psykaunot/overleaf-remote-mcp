#!/usr/bin/env python3
"""
Overleaf Remote MCP Server Main Entry Point

This module initializes and runs the Flask application for the Overleaf Remote MCP Server.
It sets up logging, configuration, and registers the necessary blueprints for MCP and SSE routes.
"""

import os
import logging
from datetime import datetime

from flask import Flask, request, jsonify, Response, send_from_directory
from flask_cors import CORS

from src.utils.config import Config
from src.utils.logger import setup_logging
from src.services.mcp_server import MCPServer
from src.routes.mcp import mcp_bp
from src.routes.sse import sse_bp

# --- Configuration and Logging Setup ---
config = Config()
setup_logging(config.LOG_LEVEL, config.LOG_FILE)
logger = logging.getLogger(__name__)

# --- Flask App Initialization ---
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config.from_object(config) # Load config from Config object

# Enable CORS for all origins, allowing Claude.ai to connect
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "Accept", "Origin"],
        "expose_headers": ["Content-Range", "X-Content-Range"]
    }
})

# --- MCP Server Initialization ---
mcp_server = MCPServer(config)

# Register blueprints
app.register_blueprint(mcp_bp, url_prefix='/rpc')
app.register_blueprint(sse_bp, url_prefix='/sse')

# Make sure mcp_server is available to blueprints
app.mcp_server = mcp_server

# --- Authentication Middleware ---
@app.before_request
def handle_auth():
    """Handle authentication for Claude.ai connections."""
    # Skip auth for health checks and static files
    if request.path in ['/health', '/favicon.ico'] or request.path.startswith('/static'):
        return
    
    # For MCP connections, allow all requests (Claude.ai handles auth differently)
    if request.path.startswith('/rpc') or request.path.startswith('/sse') or request.path.startswith('/.well-known'):
        return
    
    # Add any auth headers needed by Claude.ai
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept, Origin'
    
    if request.method == 'OPTIONS':
        return response

# --- Routes ---
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    logger.info("Health check requested.")
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "server_version": "1.0.0"
    })

# OAuth endpoints removed for authless configuration

@app.route('/.well-known/model-context-protocol', methods=['GET'])
def mcp_discovery():
    """MCP discovery endpoint - authless version."""
    logger.info("MCP discovery requested.")
    
    scheme = 'https' if request.headers.get('X-Forwarded-Proto') == 'https' or request.is_secure else 'http'
    host = request.headers.get('X-Forwarded-Host', request.headers.get('Host', request.host))
    base_url = f"{scheme}://{host}"
    
    return jsonify({
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "resources": {"subscribe": True, "listChanged": True},
            "tools": {"listChanged": True},
            "prompts": {"listChanged": True}
        },
        "serverInfo": {
            "name": "overleaf-remote-mcp",
            "version": "1.0.0",
            "description": "Overleaf Remote MCP Server"
        },
        "instructions": f"Connect to {base_url}/sse/ for SSE transport"
    }), 200, {'Content-Type': 'application/json'}

@app.route('/', defaults={'path': ''}) # Catch-all for root and subpaths
@app.route('/<path:path>')
def serve(path):
    """Serve static files for the frontend (if any)."""
    # This assumes your frontend build output (e.g., index.html) is in a 'static' folder
    # relative to your main.py. Adjust static_folder in Flask(__name__, static_folder=...) if needed.
    static_folder_path = app.static_folder
    if not os.path.exists(static_folder_path):
        logger.warning(f"Static folder not found at: {static_folder_path}")
        return "Frontend static files not found.", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        return send_from_directory(static_folder_path, 'index.html')

# --- Main Execution ---
if __name__ == '__main__':
    logger.info("Initializing Overleaf Remote MCP Server...")
    # Initialize the MCP server components
    mcp_server.initialize()
    logger.info("Server initialization completed successfully")

    logger.info(f"Starting Overleaf Remote MCP Server on {config.SERVER_HOST}:{config.SERVER_PORT}")
    logger.info(f"Debug mode: {app.debug}")
    logger.info(f"Log level: {config.LOG_LEVEL}")
    app.run(host=config.SERVER_HOST, port=config.SERVER_PORT, debug=config.DEBUG)
