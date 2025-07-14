import json
import time
import logging
from datetime import datetime
from flask import Blueprint, Response, stream_with_context, request, jsonify

logger = logging.getLogger(__name__)
sse_bp = Blueprint("sse", __name__)

@sse_bp.route("/", methods=['GET'], strict_slashes=False)
def sse_connect():
    """MCP-compliant SSE endpoint."""
    
    def event_stream():
        try:
            # Send MCP initialization
            init_message = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
                "params": {}
            }
            yield f"data: {json.dumps(init_message)}\n\n"
            
            # Keep connection alive
            while True:
                heartbeat = {
                    "jsonrpc": "2.0", 
                    "method": "notifications/heartbeat",
                    "params": {"timestamp": datetime.now().isoformat()}
                }
                yield f"data: {json.dumps(heartbeat)}\n\n"
                time.sleep(30)
                
        except GeneratorExit:
            logger.info("SSE connection closed")
        except Exception as e:
            logger.error(f"SSE error: {e}")

    response = Response(
        stream_with_context(event_stream()),
        mimetype="text/event-stream",
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization, Accept',
            'X-Accel-Buffering': 'no'  # Disable nginx buffering
        }
    )
    return response

# Add POST handler for MCP JSON-RPC messages
@sse_bp.route("/", methods=['POST'], strict_slashes=False)
def sse_post():
    """Handle MCP JSON-RPC messages via POST to SSE endpoint."""
    from flask import current_app
    
    try:
        # Get JSON-RPC request
        data = request.get_json()
        if not data:
            return jsonify({
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32600,
                    "message": "Invalid Request"
                }
            }), 400
        
        # Get MCP server instance
        mcp_server = current_app.mcp_server
        if not mcp_server:
            return jsonify({
                "jsonrpc": "2.0",
                "id": data.get("id"),
                "error": {
                    "code": -32603,
                    "message": "Internal Error: MCP server not initialized"
                }
            }), 500
        
        # Route MCP method to appropriate handler
        method = data.get("method")
        params = data.get("params", {})
        request_id = data.get("id")
        
        logger.debug(f"Handling MCP method: {method}")
        
        # Handle different MCP methods
        if method == "initialize":
            result = mcp_server.handle_initialize(params)
        elif method == "resources/list":
            result = mcp_server.handle_list_resources(params)
        elif method == "resources/read":
            result = mcp_server.handle_read_resource(params)
        elif method == "resources/subscribe":
            result = mcp_server.handle_subscribe_resource(params)
        elif method == "resources/unsubscribe":
            result = mcp_server.handle_unsubscribe_resource(params)
        elif method == "tools/list":
            result = mcp_server.handle_list_tools(params)
        elif method == "tools/call":
            result = mcp_server.handle_call_tool(params)
        elif method == "prompts/list":
            result = mcp_server.handle_list_prompts(params)
        elif method == "prompts/get":
            result = mcp_server.handle_get_prompt(params)
        elif method == "logging/setLevel":
            result = mcp_server.handle_set_log_level(params)
        else:
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }), 404
        
        # Return successful response
        response = jsonify({
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        })
        
        # Add CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Accept'
        
        return response
        
    except Exception as e:
        logger.error(f"Error handling MCP request: {e}")
        return jsonify({
            "jsonrpc": "2.0",
            "id": data.get("id") if 'data' in locals() else None,
            "error": {
                "code": -32603,
                "message": f"Internal Error: {str(e)}"
            }
        }), 500

# Add OPTIONS handler for CORS preflight
@sse_bp.route("/", methods=['OPTIONS'], strict_slashes=False)
def sse_options():
    """Handle CORS preflight for SSE endpoint."""
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Accept'
    return response
