"""
MCP Server Implementation

This module implements the core MCP server that handles all MCP protocol operations.
It coordinates between resources, tools, and prompts to provide Overleaf integration.
"""

import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional

from mcp import types
from src.utils.config import Config
from src.services.document_service import DocumentService
from src.services.overleaf_service import OverleafService
from src.mcp_components.resources.manager import ResourceManager
from src.mcp_components.tools.manager import ToolManager
from src.mcp_components.prompts.manager import PromptManager

logger = logging.getLogger(__name__)

class MCPServer:
    """
    Main MCP Server implementation for Overleaf Remote MCP.
    
    This class coordinates all MCP operations and manages the integration
    between Claude AI and Overleaf through the Model Context Protocol.
    """
    
    def __init__(self, config: Config):
        """
        Initialize the MCP server.
        
        Args:
            config: Configuration instance
        """
        self.config = config
        self.initialized = False
        self.start_time = datetime.utcnow()
        
        # Core services
        self.document_service: Optional[DocumentService] = None
        self.overleaf_service: Optional[OverleafService] = None
        
        # MCP components
        self.resource_manager: Optional[ResourceManager] = None
        self.tool_manager: Optional[ToolManager] = None
        self.prompt_manager: Optional[PromptManager] = None
        
        logger.info("MCP Server instance created")
    
    def initialize(self) -> None:
        """Initialize all server components."""
        try:
            logger.info("Initializing MCP Server components...")
            
            # Initialize core services
            self.document_service = DocumentService(self.config)
            self.document_service.initialize()
            
            self.overleaf_service = OverleafService(self.config)
            self.overleaf_service.initialize()
            
            # Initialize MCP components
            self.resource_manager = ResourceManager(
                self.document_service,
                self.overleaf_service
            )
            
            self.tool_manager = ToolManager(
                self.document_service,
                self.overleaf_service
            )
            
            self.prompt_manager = PromptManager()
            
            self.initialized = True
            logger.info("MCP Server initialization completed successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize MCP Server: {e}")
            raise
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get server capabilities for MCP protocol."""
        return {
            'protocolVersion': self.config.protocol_version,
            'capabilities': {
                'resources': {
                    'subscribe': True,
                    'listChanged': True
                },
                'tools': {
                    'listChanged': True
                },
                'prompts': {
                    'listChanged': True
                },
                'logging': {}
            },
            'serverInfo': {
                'name': self.config.mcp_server_name,
                'version': self.config.mcp_server_version,
                'description': 'Remote MCP server for Overleaf integration with Claude AI'
            }
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get current server status."""
        uptime = (datetime.utcnow() - self.start_time).total_seconds()
        
        return {
            'status': 'running' if self.initialized else 'initializing',
            'uptime_seconds': uptime,
            'start_time': self.start_time.isoformat(),
            'components': {
                'document_service': self.document_service is not None,
                'overleaf_service': self.overleaf_service is not None,
                'resource_manager': self.resource_manager is not None,
                'tool_manager': self.tool_manager is not None,
                'prompt_manager': self.prompt_manager is not None
            },
            'config': {
                'overleaf_configured': self.config.is_overleaf_configured(),
                'storage_path': self.config.get_storage_path(),
                'log_level': self.config.log_level
            }
        }
    
    # MCP Protocol Handlers
    
    def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP initialize request."""
        logger.info("Handling MCP initialize request")
        
        client_info = params.get('clientInfo', {})
        logger.info(f"Client: {client_info.get('name', 'Unknown')} v{client_info.get('version', 'Unknown')}")
        
        return self.get_capabilities()
    
    def handle_list_resources(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP resources/list request."""
        logger.debug("Handling resources/list request")
        
        if not self.resource_manager:
            raise RuntimeError("Resource manager not initialized")
        
        try:
            resources = self.resource_manager.list_resources()
            return {
                'resources': [self._convert_to_dict(resource) for resource in resources]
            }
        except Exception as e:
            logger.error(f"Error listing resources: {e}")
            raise
    
    def handle_read_resource(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP resources/read request."""
        uri = params.get('uri')
        if not uri:
            raise ValueError("URI parameter is required")
        
        logger.debug(f"Handling resources/read request for URI: {uri}")
        
        if not self.resource_manager:
            raise RuntimeError("Resource manager not initialized")
        
        try:
            content = self.resource_manager.read_resource(uri)
            return {
                'contents': [
                    {
                        'uri': uri,
                        'mimeType': self.resource_manager.get_mime_type(uri),
                        'text': content
                    }
                ]
            }
        except Exception as e:
            logger.error(f"Error reading resource {uri}: {e}")
            raise
    
    def handle_subscribe_resource(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP resources/subscribe request."""
        uri = params.get('uri')
        if not uri:
            raise ValueError("URI parameter is required")
        
        logger.debug(f"Handling resources/subscribe request for URI: {uri}")
        
        # For now, just acknowledge the subscription
        # In a full implementation, this would set up change notifications
        return {'subscribed': True}
    
    def handle_unsubscribe_resource(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP resources/unsubscribe request."""
        uri = params.get('uri')
        if not uri:
            raise ValueError("URI parameter is required")
        
        logger.debug(f"Handling resources/unsubscribe request for URI: {uri}")
        
        # For now, just acknowledge the unsubscription
        return {'unsubscribed': True}
    
    def handle_list_tools(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP tools/list request."""
        logger.debug("Handling tools/list request")
        
        if not self.tool_manager:
            raise RuntimeError("Tool manager not initialized")
        
        try:
            tools = self.tool_manager.list_tools()
            return {
                'tools': [self._convert_to_dict(tool) for tool in tools]
            }
        except Exception as e:
            logger.error(f"Error listing tools: {e}")
            raise
    
    def handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP tools/call request."""
        name = params.get('name')
        arguments = params.get('arguments', {})
        
        if not name:
            raise ValueError("Tool name is required")
        
        logger.debug(f"Handling tools/call request for tool: {name}")
        
        if not self.tool_manager:
            raise RuntimeError("Tool manager not initialized")
        
        try:
            result = self.tool_manager.call_tool(name, arguments)
            return {
                'content': [self._convert_to_dict(content) for content in result]
            }
        except Exception as e:
            logger.error(f"Error calling tool {name}: {e}")
            raise
    
    def handle_list_prompts(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP prompts/list request."""
        logger.debug("Handling prompts/list request")
        
        if not self.prompt_manager:
            raise RuntimeError("Prompt manager not initialized")
        
        try:
            prompts = self.prompt_manager.list_prompts()
            return {
                'prompts': [self._convert_to_dict(prompt) for prompt in prompts]
            }
        except Exception as e:
            logger.error(f"Error listing prompts: {e}")
            raise
    
    def handle_get_prompt(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP prompts/get request."""
        name = params.get('name')
        arguments = params.get('arguments', {})
        
        if not name:
            raise ValueError("Prompt name is required")
        
        logger.debug(f"Handling prompts/get request for prompt: {name}")
        
        if not self.prompt_manager:
            raise RuntimeError("Prompt manager not initialized")
        
        try:
            result = self.prompt_manager.get_prompt(name, arguments)
            return result
        except Exception as e:
            logger.error(f"Error getting prompt {name}: {e}")
            raise
    
    def handle_set_log_level(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP logging/setLevel request."""
        level = params.get('level')
        if not level:
            raise ValueError("Log level is required")
        
        logger.info(f"Setting log level to: {level}")
        
        try:
            # Update logging level
            logging.getLogger().setLevel(getattr(logging, level.upper()))
            return {'level': level}
        except AttributeError:
            raise ValueError(f"Invalid log level: {level}")
    
    def _convert_to_dict(self, obj) -> Dict[str, Any]:
        """
        Convert MCP types to dictionaries.
        
        Args:
            obj: Object to convert
            
        Returns:
            Dictionary representation
        """
        if hasattr(obj, '__dict__'):
            # For objects with __dict__, convert to dict
            result = {}
            for key, value in obj.__dict__.items():
                if not key.startswith('_'):
                    if hasattr(value, '__dict__'):
                        result[key] = self._convert_to_dict(value)
                    elif isinstance(value, list):
                        result[key] = [self._convert_to_dict(item) if hasattr(item, '__dict__') else item for item in value]
                    else:
                        result[key] = value
            return result
        else:
            # For simple types, return as-is
            return obj
    
    def shutdown(self) -> None:
        """Shutdown the MCP server and cleanup resources."""
        logger.info("Shutting down MCP Server...")
        
        try:
            if self.document_service:
                self.document_service.shutdown()
            
            if self.overleaf_service:
                self.overleaf_service.shutdown()
            
            self.initialized = False
            logger.info("MCP Server shutdown completed")
            
        except Exception as e:
            logger.error(f"Error during MCP Server shutdown: {e}")
            raise

