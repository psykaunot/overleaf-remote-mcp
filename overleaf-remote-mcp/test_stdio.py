#!/usr/bin/env python3
"""
Simple test script to verify stdio MCP server functionality
"""

import asyncio
import json
import subprocess
import sys
import time

async def test_stdio_server():
    """Test the stdio MCP server with basic requests."""
    
    # Start the server process
    print("Starting MCP server...")
    proc = subprocess.Popen(
        [sys.executable, "src/main_stdio.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="/home/ubuntu/projects/overleaf-remote-mcp-complete/overleaf-remote-mcp"
    )
    
    try:
        # Initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        print("Sending initialize request...")
        proc.stdin.write(json.dumps(init_request) + '\n')
        proc.stdin.flush()
        
        # Read response
        response_line = proc.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"Initialize response: {response}")
        
        # Test list tools
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        print("Sending tools/list request...")
        proc.stdin.write(json.dumps(tools_request) + '\n')
        proc.stdin.flush()
        
        # Read response
        response_line = proc.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"Tools list response: {response}")
        
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Test failed: {e}")
        stderr_output = proc.stderr.read()
        if stderr_output:
            print(f"Server stderr: {stderr_output}")
    
    finally:
        # Clean up
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()

if __name__ == "__main__":
    asyncio.run(test_stdio_server())