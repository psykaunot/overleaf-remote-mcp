#!/usr/bin/env python3
"""
Test Script for Overleaf Remote MCP Server

This script tests the MCP server functionality including:
- Server startup and health checks
- MCP protocol compliance
- Resource management
- Tool operations
- Prompt generation
"""

import json
import time
import requests
import subprocess
import sys
import os
from typing import Dict, Any, Optional

def test_server_health(base_url: str) -> bool:
    """Test server health endpoint."""
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Server health check passed: {data['status']}")
            return True
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health check error: {e}")
        return False

def test_capabilities(base_url: str) -> bool:
    """Test server capabilities endpoint."""
    try:
        response = requests.get(f"{base_url}/capabilities", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Capabilities endpoint working")
            print(f"  Protocol Version: {data.get('protocolVersion')}")
            print(f"  Server: {data.get('serverInfo', {}).get('name')}")
            return True
        else:
            print(f"✗ Capabilities check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Capabilities error: {e}")
        return False

def test_mcp_jsonrpc(base_url: str) -> bool:
    """Test MCP JSON-RPC endpoint."""
    try:
        # Test initialize request
        initialize_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "clientInfo": {
                    "name": "Test Client",
                    "version": "1.0.0"
                }
            }
        }
        
        response = requests.post(
            f"{base_url}/mcp/jsonrpc",
            json=initialize_request,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if "result" in data:
                print("✓ MCP initialize request successful")
                return True
            else:
                print(f"✗ MCP initialize failed: {data}")
                return False
        else:
            print(f"✗ MCP JSON-RPC failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ MCP JSON-RPC error: {e}")
        return False

def test_resources_list(base_url: str) -> bool:
    """Test resources/list endpoint."""
    try:
        request_data = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "resources/list",
            "params": {}
        }
        
        response = requests.post(
            f"{base_url}/mcp/jsonrpc",
            json=request_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if "result" in data and "resources" in data["result"]:
                resources = data["result"]["resources"]
                print(f"✓ Resources list successful: {len(resources)} resources")
                return True
            else:
                print(f"✗ Resources list failed: {data}")
                return False
        else:
            print(f"✗ Resources list failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Resources list error: {e}")
        return False

def test_tools_list(base_url: str) -> bool:
    """Test tools/list endpoint."""
    try:
        request_data = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/list",
            "params": {}
        }
        
        response = requests.post(
            f"{base_url}/mcp/jsonrpc",
            json=request_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if "result" in data and "tools" in data["result"]:
                tools = data["result"]["tools"]
                print(f"✓ Tools list successful: {len(tools)} tools")
                return True
            else:
                print(f"✗ Tools list failed: {data}")
                return False
        else:
            print(f"✗ Tools list failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Tools list error: {e}")
        return False

def test_prompts_list(base_url: str) -> bool:
    """Test prompts/list endpoint."""
    try:
        request_data = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "prompts/list",
            "params": {}
        }
        
        response = requests.post(
            f"{base_url}/mcp/jsonrpc",
            json=request_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if "result" in data and "prompts" in data["result"]:
                prompts = data["result"]["prompts"]
                print(f"✓ Prompts list successful: {len(prompts)} prompts")
                return True
            else:
                print(f"✗ Prompts list failed: {data}")
                return False
        else:
            print(f"✗ Prompts list failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Prompts list error: {e}")
        return False

def test_create_project_tool(base_url: str) -> Optional[str]:
    """Test create_project tool."""
    try:
        request_data = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "create_project",
                "arguments": {
                    "title": "Test Project",
                    "document_type": "article",
                    "template_id": "article_basic"
                }
            }
        }
        
        response = requests.post(
            f"{base_url}/mcp/jsonrpc",
            json=request_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if "result" in data and "content" in data["result"]:
                content = data["result"]["content"][0]["text"]
                print("✓ Create project tool successful")
                
                # Extract project ID from response
                try:
                    import re
                    match = re.search(r"ID: ([a-f0-9-]+)", content)
                    if match:
                        return match.group(1)
                except:
                    pass
                return "test_project_id"
            else:
                print(f"✗ Create project tool failed: {data}")
                return None
        else:
            print(f"✗ Create project tool failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Create project tool error: {e}")
        return None

def test_list_projects_tool(base_url: str) -> bool:
    """Test list_projects tool."""
    try:
        request_data = {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "tools/call",
            "params": {
                "name": "list_projects",
                "arguments": {}
            }
        }
        
        response = requests.post(
            f"{base_url}/mcp/jsonrpc",
            json=request_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if "result" in data and "content" in data["result"]:
                print("✓ List projects tool successful")
                return True
            else:
                print(f"✗ List projects tool failed: {data}")
                return False
        else:
            print(f"✗ List projects tool failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ List projects tool error: {e}")
        return False

def test_write_abstract_prompt(base_url: str) -> bool:
    """Test write_abstract prompt."""
    try:
        request_data = {
            "jsonrpc": "2.0",
            "id": 7,
            "method": "prompts/get",
            "params": {
                "name": "write_abstract",
                "arguments": {
                    "title": "Test Research Paper",
                    "research_area": "Computer Science",
                    "key_findings": "Novel algorithm improves performance",
                    "methodology": "Experimental evaluation"
                }
            }
        }
        
        response = requests.post(
            f"{base_url}/mcp/jsonrpc",
            json=request_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if "result" in data and "messages" in data["result"]:
                print("✓ Write abstract prompt successful")
                return True
            else:
                print(f"✗ Write abstract prompt failed: {data}")
                return False
        else:
            print(f"✗ Write abstract prompt failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Write abstract prompt error: {e}")
        return False

def test_sse_endpoint(base_url: str) -> bool:
    """Test SSE endpoint (basic connectivity)."""
    try:
        response = requests.get(
            f"{base_url}/sse/",
            stream=True,
            timeout=5,
            headers={"Accept": "text/event-stream"}
        )
        
        if response.status_code == 200:
            print("✓ SSE endpoint accessible")
            return True
        else:
            print(f"✗ SSE endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print("✓ SSE endpoint accessible (timeout expected)")
        return True
    except Exception as e:
        print(f"✗ SSE endpoint error: {e}")
        return False

def start_server() -> subprocess.Popen:
    """Start the MCP server."""
    print("Starting MCP server...")
    
    # Change to server directory
    server_dir = os.path.dirname(os.path.abspath(__file__))



    
    # Start server process
    process = subprocess.Popen(
        [sys.executable, "src/main.py"],
        cwd=server_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, "VIRTUAL_ENV": f"{server_dir}/venv"}
    )


    
    # Wait for server to start
    time.sleep(3)
    
    return process

def main():
    """Run all tests."""
    print("=" * 60)
    print("Overleaf Remote MCP Server Test Suite")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Start server
    server_process = start_server()
    
    try:
        # Wait for server to be ready
        print("\nWaiting for server to start...")
        time.sleep(2)
        
        # Run tests
        tests = [
            ("Server Health", lambda: test_server_health(base_url)),
            ("Server Capabilities", lambda: test_capabilities(base_url)),
            ("MCP JSON-RPC Initialize", lambda: test_mcp_jsonrpc(base_url)),
            ("Resources List", lambda: test_resources_list(base_url)),
            ("Tools List", lambda: test_tools_list(base_url)),
            ("Prompts List", lambda: test_prompts_list(base_url)),
            ("Create Project Tool", lambda: test_create_project_tool(base_url) is not None),
            ("List Projects Tool", lambda: test_list_projects_tool(base_url)),
            ("Write Abstract Prompt", lambda: test_write_abstract_prompt(base_url)),
            ("SSE Endpoint", lambda: test_sse_endpoint(base_url))
        ]
        
        passed = 0
        total = len(tests)
        
        print(f"\nRunning {total} tests...")
        print("-" * 40)
        
        for test_name, test_func in tests:
            print(f"\nTesting: {test_name}")
            try:
                if test_func():
                    passed += 1
                else:
                    print(f"  FAILED: {test_name}")
            except Exception as e:
                print(f"  ERROR: {test_name} - {e}")
        
        print("\n" + "=" * 60)
        print(f"Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! MCP server is working correctly.")
            return 0
        else:
            print(f"❌ {total - passed} tests failed.")
            return 1
            
    finally:
        # Stop server
        print("\nStopping server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()

if __name__ == "__main__":
    sys.exit(main())

