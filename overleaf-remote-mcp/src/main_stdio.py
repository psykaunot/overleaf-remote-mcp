#!/usr/bin/env python3
"""
Overleaf Remote MCP Server - Stdio Transport for Claude Desktop

This module provides stdio transport for the Overleaf Remote MCP Server,
compatible with Claude Desktop's MCP configuration.
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, Optional, Union

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource, Tool, Prompt, TextContent, ImageContent, EmbeddedResource,
    CallToolResult, GetPromptResult, ListResourcesResult, ListToolsResult, 
    ListPromptsResult, ReadResourceResult
)

from src.utils.config import Config
from src.utils.logger import setup_logging
from src.services.mcp_server import MCPServer

# Configuration and Logging Setup
config = Config()
setup_logging(config.LOG_LEVEL, config.LOG_FILE)
logger = logging.getLogger(__name__)

# Create MCP Server instance
server = Server("overleaf-remote-mcp")

# Initialize our MCP server components
mcp_server = MCPServer(config)

@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    """Handle resources/list requests."""
    try:
        logger.debug("Handling list_resources request")
        # Call the sync method and return the resources
        result = mcp_server.resource_manager.list_resources()
        return result
    except Exception as e:
        logger.error(f"Error in list_resources: {e}")
        raise

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Handle resources/read requests."""
    try:
        logger.debug(f"Handling read_resource request for URI: {uri}")
        # Call the sync method
        result = mcp_server.resource_manager.read_resource(uri)
        return result
    except Exception as e:
        logger.error(f"Error in read_resource: {e}")
        raise

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """Handle tools/list requests."""
    try:
        logger.debug("Handling list_tools request")
        # Call the sync method
        result = mcp_server.tool_manager.list_tools()
        return result
    except Exception as e:
        logger.error(f"Error in list_tools: {e}")
        raise

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent | ImageContent | EmbeddedResource]:
    """Handle tools/call requests."""
    try:
        logger.debug(f"Handling call_tool request for tool: {name}")
        # Call the sync method
        result = mcp_server.tool_manager.call_tool(name, arguments)
        
        # Convert result to proper MCP types
        content_list = []
        for item in result:
            if isinstance(item, dict):
                if item.get('type') == 'text':
                    content_list.append(TextContent(type="text", text=item.get('text', '')))
                else:
                    content_list.append(TextContent(type="text", text=str(item)))
            else:
                content_list.append(TextContent(type="text", text=str(item)))
        
        return content_list
    except Exception as e:
        logger.error(f"Error in call_tool: {e}")
        raise

@server.list_prompts()
async def handle_list_prompts() -> list[Prompt]:
    """Handle prompts/list requests."""
    try:
        logger.debug("Handling list_prompts request")
        # Call the sync method
        result = mcp_server.prompt_manager.list_prompts()
        return result
    except Exception as e:
        logger.error(f"Error in list_prompts: {e}")
        raise

@server.get_prompt()
async def handle_get_prompt(name: str, arguments: Optional[dict] = None) -> GetPromptResult:
    """Handle prompts/get requests."""
    try:
        logger.debug(f"Handling get_prompt request for prompt: {name}")
        # Call the sync method
        result = mcp_server.prompt_manager.get_prompt(name, arguments or {})
        
        # Convert result to GetPromptResult if needed
        if isinstance(result, dict):
            messages = result.get('messages', [])
            description = result.get('description', '')
            
            # Convert messages to proper TextContent format
            prompt_messages = []
            for msg in messages:
                if isinstance(msg, dict):
                    content = TextContent(type="text", text=msg.get('content', ''))
                    prompt_messages.append({
                        "role": msg.get('role', 'user'),
                        "content": content
                    })
            
            return GetPromptResult(
                description=description,
                messages=prompt_messages
            )
        
        return result
    except Exception as e:
        logger.error(f"Error in get_prompt: {e}")
        raise

async def main():
    """Main function to run the MCP server with stdio transport."""
    try:
        logger.info("Initializing Overleaf Remote MCP Server (stdio transport)...")
        
        # Initialize MCP server components
        mcp_server.initialize()
        logger.info("MCP server components initialized successfully")
        
        # Run the server with stdio transport
        logger.info("Starting MCP server with stdio transport...")
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream, 
                write_stream, 
                server.create_initialization_options()
            )
            
    except Exception as e:
        logger.error(f"Error running MCP server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())