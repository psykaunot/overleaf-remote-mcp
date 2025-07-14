# Overleaf Remote MCP Server - Complete Guide

## Table of Contents

1. [Introduction](#introduction)
2. [What is Remote MCP?](#what-is-remote-mcp)
3. [Installation Guide](#installation-guide)
4. [Configuration](#configuration)
5. [Connecting to Claude AI](#connecting-to-claude-ai)
6. [Usage Examples](#usage-examples)
7. [Available Tools](#available-tools)
8. [Available Prompts](#available-prompts)
9. [Deployment Options](#deployment-options)
10. [Troubleshooting](#troubleshooting)
11. [Advanced Configuration](#advanced-configuration)

## Introduction

The Overleaf Remote MCP Server is a revolutionary tool that bridges Claude AI and Overleaf, enabling seamless LaTeX document creation and management directly from your Claude conversations. This server implements the Model Context Protocol (MCP) to provide Claude with powerful tools for academic writing, document management, and LaTeX compilation.

### Key Benefits

- **No API Key Required**: Works with Claude Pro accounts without needing API access
- **Direct Integration**: Claude can create, edit, and manage LaTeX documents
- **AI-Powered Content**: Generate academic content using specialized prompts
- **Version Control**: Track changes and maintain document history
- **Overleaf Sync**: Optional synchronization with Overleaf for collaboration
- **Template System**: Pre-built templates for articles, reports, and theses

## What is Remote MCP?

Remote MCP (Model Context Protocol) is a new feature from Anthropic that allows Claude.ai to connect to external servers and access additional capabilities. Unlike traditional MCP that requires Claude Desktop, Remote MCP works directly in the web interface with Claude Pro accounts.

### How It Works

1. **Server Setup**: You run the MCP server on your machine or cloud
2. **Public Access**: The server is made accessible via a public URL
3. **Claude Connection**: Claude.ai connects to your server via Server-Sent Events (SSE)
4. **Tool Access**: Claude gains access to all the tools and prompts you've configured

## Installation Guide

### Prerequisites

- **Python 3.11 or higher**
- **Claude Pro account** (required for Remote MCP)
- **Git** for cloning the repository
- **Optional**: Overleaf account for synchronization features

### Step 1: Download and Setup

```bash
# Navigate to the project directory
cd overleaf-remote-mcp

# Activate the virtual environment
source venv/bin/activate

# Install dependencies (already done during setup)
pip install -r requirements.txt
```

### Step 2: Basic Configuration

Create a `.env` file for configuration:

```bash
cp .env.example .env
```

Edit the `.env` file with your preferences:

```bash
# Basic server configuration
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=5000
MCP_DEBUG=false

# Logging
MCP_LOG_LEVEL=INFO

# Storage paths
MCP_STORAGE_PATH=data/projects
```

### Step 3: Test Local Installation

```bash
# Start the server
python src/main.py

# In another terminal, run tests
python test_mcp_server.py
```

You should see all tests pass, confirming the installation is working correctly.

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_SERVER_HOST` | `0.0.0.0` | Server host address |
| `MCP_SERVER_PORT` | `5000` | Server port |
| `MCP_DEBUG` | `false` | Enable debug mode |
| `MCP_LOG_LEVEL` | `INFO` | Logging level |
| `MCP_STORAGE_PATH` | `data/projects` | Project storage directory |
| `OVERLEAF_EMAIL` | - | Overleaf account email (optional) |
| `OVERLEAF_PASSWORD` | - | Overleaf account password (optional) |

### Server Endpoints

The server exposes several endpoints:

- **`/health`** - Health check endpoint
- **`/capabilities`** - Server capabilities
- **`/sse/`** - Server-Sent Events endpoint (for Claude connection)
- **`/mcp/jsonrpc`** - JSON-RPC endpoint for MCP protocol
- **`/mcp/status`** - Server status information

## Connecting to Claude AI

### Step 1: Make Your Server Publicly Accessible

For Claude.ai to connect to your server, it must be accessible from the internet. Here are several options:

#### Option A: Cloud Deployment (Recommended)

Deploy to a cloud service like:
- **AWS EC2**
- **Google Cloud Compute Engine**
- **DigitalOcean Droplet**
- **Azure Virtual Machine**

#### Option B: Tunneling (For Testing)

Use a tunneling service for quick testing:

```bash
# Using ngrok
ngrok http 5000

# Using cloudflare tunnel
cloudflared tunnel --url http://localhost:5000
```

#### Option C: VPS Hosting

Use a VPS provider and configure your server with a domain name.

### Step 2: Configure Claude AI

1. **Open Claude.ai** in your web browser
2. **Go to Settings** (click your profile icon)
3. **Navigate to Integrations** or **Custom Integrations**
4. **Add New Integration** with these details:
   - **Name**: `Overleaf MCP Server`
   - **URL**: `https://your-server-url.com/sse/`
   - **Description**: `LaTeX document management and academic writing assistant`

### Step 3: Test the Connection

Start a new conversation with Claude and try:

```
Hello! Can you list the available tools for document management?
```

Claude should respond with information about the Overleaf MCP tools.

## Usage Examples

### Creating Your First Project

```
Claude, please create a new research paper project titled "AI in Healthcare" using the article template.
```

**Expected Response:**
Claude will use the `create_project` tool to create a new LaTeX project with the specified title and template.

### Generating Academic Content

```
Claude, write an abstract for a paper on "Machine Learning for Medical Diagnosis" in the field of Computer Science. The key findings are improved accuracy and faster diagnosis times. The methodology involves deep learning and clinical data analysis.
```

**Expected Response:**
Claude will use the `write_abstract` prompt to generate a comprehensive abstract in LaTeX format.

### Managing Documents

```
Claude, show me all my projects and then list the documents in the "AI in Healthcare" project.
```

**Expected Response:**
Claude will use the `list_projects` and `list_documents` tools to show your project overview.

### Improving Existing Content

```
Claude, please improve the academic style and clarity of this text:

\section{Results}
We found that the algorithm works better than before. The accuracy increased by 15%. This is good for medical applications.
```

**Expected Response:**
Claude will use the `improve_content` tool to enhance the text with better academic language and structure.

### Working with LaTeX

```
Claude, help me create a table in LaTeX that shows comparison results between three different algorithms with columns for Algorithm Name, Accuracy, and Processing Time.
```

**Expected Response:**
Claude will use the `latex_help` prompt to provide proper LaTeX table syntax and formatting.

## Available Tools

### Project Management Tools

1. **`create_project`**
   - Creates new LaTeX projects
   - Parameters: title, document_type, template_id
   - Returns: Project information with unique ID

2. **`list_projects`**
   - Lists all existing projects
   - No parameters required
   - Returns: Array of project summaries

3. **`get_project`**
   - Gets detailed project information
   - Parameters: project_id
   - Returns: Complete project details and document list

### Document Management Tools

4. **`create_document`**
   - Creates new documents in projects
   - Parameters: project_id, filename, content
   - Returns: Document information

5. **`update_document`**
   - Updates document content with version control
   - Parameters: project_id, filename, content, commit_message
   - Returns: Success confirmation

6. **`get_document`**
   - Retrieves document content
   - Parameters: project_id, filename
   - Returns: Document content

7. **`list_documents`**
   - Lists all documents in a project
   - Parameters: project_id
   - Returns: Array of document information

### Content Generation Tools

8. **`generate_section`**
   - Generates LaTeX content for specific sections
   - Parameters: section_type, topic, context, length
   - Returns: Generated LaTeX content

9. **`improve_content`**
   - Improves existing LaTeX content
   - Parameters: content, improvement_type, instructions
   - Returns: Enhanced content

### Template Tools

10. **`list_templates`**
    - Lists available LaTeX templates
    - No parameters required
    - Returns: Array of template information

11. **`get_template`**
    - Gets template content
    - Parameters: template_id
    - Returns: Template LaTeX code

### Integration Tools

12. **`sync_to_overleaf`**
    - Synchronizes project to Overleaf
    - Parameters: project_id
    - Returns: Overleaf project URL

13. **`compile_project`**
    - Compiles LaTeX project to PDF
    - Parameters: project_id
    - Returns: Compilation results and PDF URL

## Available Prompts

### Academic Writing Prompts

1. **`write_abstract`**
   - Generates comprehensive abstracts
   - Arguments: title, research_area, key_findings, methodology

2. **`write_introduction`**
   - Creates engaging introductions
   - Arguments: topic, research_question, background, objectives

3. **`write_methodology`**
   - Develops detailed methodology sections
   - Arguments: research_type, data_collection, analysis_methods, participants

4. **`write_results`**
   - Presents findings effectively
   - Arguments: findings, data_analysis, statistical_significance, figures_tables

5. **`write_discussion`**
   - Creates insightful discussion sections
   - Arguments: results_summary, implications, limitations, future_work

6. **`write_conclusion`**
   - Writes strong conclusions
   - Arguments: main_contributions, research_question, broader_impact

### Writing Enhancement Prompts

7. **`improve_writing`**
   - Enhances academic writing style
   - Arguments: text, improvement_focus, target_audience

8. **`create_outline`**
   - Structures papers effectively
   - Arguments: topic, paper_type, length, requirements

### Technical Assistance Prompts

9. **`format_citations`**
   - Handles citations and bibliography
   - Arguments: citation_style, sources, context

10. **`latex_help`**
    - Provides LaTeX formatting assistance
    - Arguments: task, document_class, packages

### Research Support Prompts

11. **`research_proposal`**
    - Generates research proposals
    - Arguments: research_area, problem_statement, objectives, methodology, timeline

## Deployment Options

### Option 1: Local Development

**Best for**: Testing and development

```bash
# Start the server locally
python src/main.py

# Use ngrok for public access
ngrok http 5000
```

**Pros**: Quick setup, easy debugging
**Cons**: Not suitable for production, temporary URLs

### Option 2: Cloud VPS Deployment

**Best for**: Production use, permanent setup

#### DigitalOcean Droplet Example

1. **Create a droplet** with Ubuntu 22.04
2. **Install dependencies**:
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv git nginx
```

3. **Clone and setup**:
```bash
git clone <your-repo-url>
cd overleaf-remote-mcp
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Configure systemd service**:
```bash
sudo nano /etc/systemd/system/mcp-server.service
```

```ini
[Unit]
Description=Overleaf MCP Server
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/overleaf-remote-mcp
Environment=PATH=/home/ubuntu/overleaf-remote-mcp/venv/bin
ExecStart=/home/ubuntu/overleaf-remote-mcp/venv/bin/python src/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

5. **Start the service**:
```bash
sudo systemctl enable mcp-server
sudo systemctl start mcp-server
```

6. **Configure Nginx**:
```bash
sudo nano /etc/nginx/sites-available/mcp-server
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # SSE specific headers
        proxy_buffering off;
        proxy_cache off;
        proxy_set_header Connection '';
        proxy_http_version 1.1;
        chunked_transfer_encoding off;
    }
}
```

7. **Enable the site**:
```bash
sudo ln -s /etc/nginx/sites-available/mcp-server /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option 3: Docker Deployment

**Best for**: Containerized environments

```bash
# Build the image
docker build -t overleaf-mcp-server .

# Run the container
docker run -d \
  --name mcp-server \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -e MCP_SERVER_HOST=0.0.0.0 \
  overleaf-mcp-server
```

Or use Docker Compose:

```bash
docker-compose up -d
```

### Option 4: Heroku Deployment

**Best for**: Quick cloud deployment

1. **Install Heroku CLI**
2. **Create Heroku app**:
```bash
heroku create your-mcp-server
```

3. **Configure environment**:
```bash
heroku config:set MCP_SERVER_HOST=0.0.0.0
heroku config:set MCP_SERVER_PORT=$PORT
```

4. **Deploy**:
```bash
git push heroku main
```

## Troubleshooting

### Common Issues

#### 1. Server Won't Start

**Symptoms**: Error messages when running `python src/main.py`

**Solutions**:
- Check Python version: `python --version` (should be 3.11+)
- Verify virtual environment: `which python`
- Install missing dependencies: `pip install -r requirements.txt`
- Check port availability: `netstat -tulpn | grep 5000`

#### 2. Claude Can't Connect

**Symptoms**: Claude reports connection errors

**Solutions**:
- Verify server is publicly accessible: `curl http://your-url/health`
- Check firewall settings
- Ensure CORS is enabled (it is by default)
- Verify the SSE endpoint: `curl -H "Accept: text/event-stream" http://your-url/sse/`

#### 3. Tools Not Working

**Symptoms**: Claude can connect but tools fail

**Solutions**:
- Check server logs: `tail -f logs/mcp_server_*.log`
- Verify database permissions: `ls -la src/database/`
- Test tools manually: `python test_mcp_server.py`
- Check storage directory: `ls -la data/projects/`

#### 4. Overleaf Sync Issues

**Symptoms**: Sync to Overleaf fails

**Solutions**:
- Verify Overleaf credentials in `.env`
- Check Overleaf service status
- Review authentication logs
- Note: Overleaf integration is currently in mock mode for development

### Debug Mode

Enable debug mode for detailed logging:

```bash
export MCP_DEBUG=true
export MCP_LOG_LEVEL=DEBUG
python src/main.py
```

### Log Analysis

Check logs for issues:

```bash
# View recent logs
tail -f logs/mcp_server_*.log

# Search for errors
grep -i error logs/mcp_server_*.log

# Check specific component logs
grep "ResourceManager" logs/mcp_server_*.log
```

## Advanced Configuration

### Custom Templates

Add your own LaTeX templates:

1. **Access the database**:
```bash
sqlite3 src/database/app.db
```

2. **Insert new template**:
```sql
INSERT INTO templates (id, name, document_type, content, description)
VALUES ('custom_thesis', 'Custom Thesis', 'thesis', 
        '\documentclass{report}...', 'Custom thesis template');
```

### Security Configuration

For production deployment:

```bash
# Generate secure secret key
export MCP_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Restrict origins
export MCP_ALLOWED_ORIGINS="https://claude.ai,https://your-domain.com"

# Enable rate limiting
export MCP_RATE_LIMIT=50

# Set production log level
export MCP_LOG_LEVEL=WARNING
```

### Performance Tuning

For high-traffic deployments:

```bash
# Increase worker processes
export FLASK_WORKERS=4

# Configure database connection pooling
export MCP_DB_POOL_SIZE=10

# Enable caching
export MCP_ENABLE_CACHE=true
```

### Monitoring

Set up monitoring with:

1. **Health checks**: Monitor `/health` endpoint
2. **Log aggregation**: Use ELK stack or similar
3. **Metrics collection**: Implement Prometheus metrics
4. **Alerting**: Set up alerts for service failures

---

## Conclusion

The Overleaf Remote MCP Server provides a powerful bridge between Claude AI and LaTeX document management. With proper setup and configuration, you can revolutionize your academic writing workflow by leveraging AI assistance directly in your document creation process.

For additional support, refer to the project documentation or open an issue on the GitHub repository.

