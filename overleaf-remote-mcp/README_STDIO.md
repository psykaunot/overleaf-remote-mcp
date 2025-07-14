# Overleaf Remote MCP Server - Claude Desktop Integration

This is the stdio transport version of the Overleaf Remote MCP Server, designed to work with Claude Desktop.

## Features

The server provides 13 tools, 14 resources, and 11 prompts for comprehensive Overleaf and LaTeX document management:

### Tools Available:
- **Project Management**: create_project, list_projects, get_project
- **Document Management**: create_document, update_document, get_document, list_documents
- **Content Generation**: generate_section, improve_content
- **Templates**: list_templates, get_template
- **Overleaf Integration**: sync_to_overleaf, compile_project

### Resources Available:
- Project metadata and documents
- Version history
- Compilation status
- Template library

### Prompts Available:
- Academic writing templates
- LaTeX structure helpers
- Content improvement suggestions

## Installation

1. **Install dependencies**:
   ```bash
   cd /home/ubuntu/projects/overleaf-remote-mcp-complete/overleaf-remote-mcp
   pip install -r requirements_stdio.txt
   ```

2. **Test the server**:
   ```bash
   python3 src/main_stdio.py
   ```

## Claude Desktop Configuration

1. **Find your Claude Desktop config file**:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. **Add the server configuration**:
   ```json
   {
     "mcpServers": {
       "overleaf-remote-mcp": {
         "command": "python3",
         "args": [
           "/home/ubuntu/projects/overleaf-remote-mcp-complete/overleaf-remote-mcp/src/main_stdio.py"
         ],
         "env": {
           "MCP_LOG_LEVEL": "INFO"
         }
       }
     }
   }
   ```

3. **Restart Claude Desktop** to load the new server.

## Usage

Once configured, you'll see the Overleaf MCP tools available in Claude Desktop. You can:

1. **Create LaTeX projects**:
   ```
   Create a new research paper project called "My Research" of type "article"
   ```

2. **Generate content**:
   ```
   Generate an introduction section for a paper about "Machine Learning Applications"
   ```

3. **Manage documents**:
   ```
   List all my projects and show me the documents in the first one
   ```

4. **Use templates**:
   ```
   Show me available LaTeX templates
   ```

## Configuration Options

The server can be configured using environment variables:

- `MCP_LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)
- `MCP_STORAGE_PATH`: Path for storing project files (default: "data/projects")
- `OVERLEAF_EMAIL`: Optional Overleaf email for online sync
- `OVERLEAF_PASSWORD`: Optional Overleaf password for online sync

## File Structure

```
src/
├── main_stdio.py           # Main stdio transport server
├── services/
│   ├── mcp_server.py       # Core MCP server implementation
│   ├── document_service.py # Local document management
│   └── overleaf_service.py # Overleaf integration
├── mcp_components/
│   ├── tools/manager.py    # Tool implementations
│   ├── resources/manager.py # Resource management
│   └── prompts/manager.py  # Prompt templates
└── utils/
    ├── config.py           # Configuration management
    └── logger.py           # Logging setup
```

## Troubleshooting

1. **Server not starting**:
   - Check Python path in configuration
   - Verify all dependencies are installed
   - Check log files in `logs/mcp_server.log`

2. **Tools not appearing in Claude Desktop**:
   - Restart Claude Desktop after configuration changes
   - Check the configuration file syntax
   - Verify the absolute path to main_stdio.py

3. **Permission issues**:
   - Ensure the script is executable: `chmod +x src/main_stdio.py`
   - Check file permissions on the project directory

## Development

To modify or extend the server:

1. **Add new tools**: Edit `src/mcp_components/tools/manager.py`
2. **Add new resources**: Edit `src/mcp_components/resources/manager.py`
3. **Add new prompts**: Edit `src/mcp_components/prompts/manager.py`

The server automatically loads changes when restarted.

## Offline Mode

The server works in offline mode by default. To enable Overleaf integration:

1. Set environment variables:
   ```bash
   export OVERLEAF_EMAIL="your-email@example.com"
   export OVERLEAF_PASSWORD="your-password"
   ```

2. Restart the server.

## Logging

Logs are written to `logs/mcp_server.log` by default. You can view them with:

```bash
tail -f logs/mcp_server.log
```