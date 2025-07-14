"""
MCP Routes

This module implements the JSON-RPC endpoints for the Model Context Protocol.
It handles MCP requests and routes them to the appropriate handlers.
"""

import json
import logging
from flask import Blueprint, request, jsonify, current_app
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

mcp_bp = Blueprint('mcp', __name__)

@mcp_bp.route('/jsonrpc', methods=['POST'])
def handle_jsonrpc():
    """Handle JSON-RPC requests for MCP protocol."""
    try:
        # Parse JSON-RPC request
        data = request.get_json()
        if not data:
            return create_error_response(None, -32700, "Parse error")
        
        # Validate JSON-RPC format
        if not isinstance(data, dict) or data.get('jsonrpc') != '2.0':
            return create_error_response(data.get('id'), -32600, "Invalid Request")
        
        method = data.get('method')
        params = data.get('params', {})
        request_id = data.get('id')
        
        if not method:
            return create_error_response(request_id, -32600, "Invalid Request")
        
        logger.debug(f"Handling MCP request: {method}")
        
        # Get MCP server instance
        mcp_server = current_app.mcp_server
        if not mcp_server:
            return create_error_response(request_id, -32603, "MCP server not initialized")
        
        # Route to appropriate handler
        try:
            if method == 'initialize':
                result = await_if_needed(mcp_server.handle_initialize(params))
            elif method == 'resources/list':
                result = await_if_needed(mcp_server.handle_list_resources(params))
            elif method == 'resources/read':
                result = await_if_needed(mcp_server.handle_read_resource(params))
            elif method == 'resources/subscribe':
                result = await_if_needed(mcp_server.handle_subscribe_resource(params))
            elif method == 'resources/unsubscribe':
                result = await_if_needed(mcp_server.handle_unsubscribe_resource(params))
            elif method == 'tools/list':
                result = await_if_needed(mcp_server.handle_list_tools(params))
            elif method == 'tools/call':
                result = await_if_needed(mcp_server.handle_call_tool(params))
            elif method == 'prompts/list':
                result = await_if_needed(mcp_server.handle_list_prompts(params))
            elif method == 'prompts/get':
                result = await_if_needed(mcp_server.handle_get_prompt(params))
            elif method == 'logging/setLevel':
                result = await_if_needed(mcp_server.handle_set_log_level(params))
            elif method == 'ping':
                result = {'status': 'pong', 'timestamp': str(datetime.utcnow())}
            else:
                return create_error_response(request_id, -32601, f"Method not found: {method}")
            
            return create_success_response(request_id, result)
            
        except Exception as e:
            logger.error(f"Error handling MCP request {method}: {e}")
            return create_error_response(request_id, -32603, f"Internal error: {str(e)}")
    
    except Exception as e:
        logger.error(f"Error processing JSON-RPC request: {e}")
        return create_error_response(None, -32700, "Parse error")

@mcp_bp.route('/capabilities', methods=['GET'])
def get_capabilities():
    """Get server capabilities."""
    try:
        mcp_server = current_app.mcp_server
        if not mcp_server:
            return jsonify({'error': 'MCP server not initialized'}), 500
        
        capabilities = mcp_server.get_capabilities()
        return jsonify(capabilities)
    
    except Exception as e:
        logger.error(f"Error getting capabilities: {e}")
        return jsonify({'error': str(e)}), 500

@mcp_bp.route('/status', methods=['GET'])
def get_status():
    """Get server status."""
    try:
        mcp_server = current_app.mcp_server
        if not mcp_server:
            return jsonify({'status': 'error', 'message': 'MCP server not initialized'}), 500
        
        status = mcp_server.get_status()
        return jsonify(status)
    
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({'error': str(e)}), 500

def create_success_response(request_id: Optional[Any], result: Any) -> Dict[str, Any]:
    """Create a JSON-RPC success response."""
    response = {
        'jsonrpc': '2.0',
        'id': request_id,
        'result': result
    }
    return jsonify(response)

def create_error_response(request_id: Optional[Any], code: int, message: str, data: Optional[Any] = None) -> Dict[str, Any]:
    """Create a JSON-RPC error response."""
    error = {
        'code': code,
        'message': message
    }
    if data is not None:
        error['data'] = data
    
    response = {
        'jsonrpc': '2.0',
        'id': request_id,
        'error': error
    }
    return jsonify(response)

def await_if_needed(result):
    """Handle both sync and async results."""
    return result  # Your methods are actually sync, not async

# Import datetime for ping response
from datetime import datetime

