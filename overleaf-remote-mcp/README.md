# Overleaf Remote MCP Server

A Model Context Protocol (MCP) server that connects Overleaf to Claude AI via Remote MCP, enabling Claude to write and manage LaTeX documents directly in Overleaf projects.

## 🎯 Overview

This server provides a bridge between Claude AI and Overleaf, allowing you to:

- **Create and manage LaTeX projects** directly from Claude conversations
- **Generate academic content** using AI-powered prompts for abstracts, introductions, methodology, etc.
- **Edit and improve documents** with intelligent content suggestions
- **Synchronize with Overleaf** for collaborative editing and PDF compilation
- **Access document templates** for articles, reports, theses, and more

## ✨ Key Features

### 🔧 **13 Powerful Tools**
- `create_project` - Create new LaTeX projects with templates
- `list_projects` - View all your projects
- `create_document` - Add new documents to projects
- `update_document` - Edit document content with version control
- `generate_section` - AI-powered content generation for specific sections
- `improve_content` - Enhance existing text for clarity and academic style
- `sync_to_overleaf` - Synchronize projects with Overleaf
- `compile_project` - Compile LaTeX to PDF
- And more...

### 📝 **11 Smart Prompts**
- `write_abstract` - Generate comprehensive abstracts
- `write_introduction` - Create engaging introductions
- `write_methodology` - Develop detailed methodology sections
- `write_results` - Present findings effectively
- `improve_writing` - Enhance academic writing style
- `create_outline` - Structure your papers
- `format_citations` - Handle citations and bibliography
- `latex_help` - Get LaTeX formatting assistance
- And more...

### 📚 **Resource Management**
- Access project metadata and documents
- View version history
- Check compilation status
- Browse available templates

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Claude Pro account (no API key required)
- Optional: Overleaf account for synchronization

### Installation

1. **Clone and setup the server:**
```bash
cd overleaf-remote-mcp
source venv/bin/activate
pip install -r requirements.txt
```

2. **Configure environment (optional):**
```bash
cp .env.example .env
# Edit .env with your preferences
```

3. **Start the server:**
```bash
python src/main.py
```

The server will start on `http://localhost:5000` by default.

### Connecting to Claude AI

1. **In Claude.ai, go to Settings → Integrations**
2. **Add a new Remote MCP integration:**
   - **Name:** Overleaf MCP Server
   - **URL:** `http://your-server-url:5000/sse/`
   - **Description:** LaTeX document management and generation

3. **Start using the integration in your conversations!**

## 📖 Usage Examples

### Creating a New Research Paper

```
Claude, please create a new research paper project titled "Machine Learning in Healthcare" using the article template.
```

### Generating Content

```
Claude, write an abstract for my paper on "Deep Learning for Medical Image Analysis" in the field of Computer Science, focusing on novel CNN architectures and improved diagnostic accuracy.
```

### Improving Existing Content

```
Claude, please improve the clarity and academic style of this methodology section: [paste your LaTeX content]
```

### Managing Projects

```
Claude, list all my projects and show me the documents in the "Machine Learning in Healthcare" project.
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following options:

```bash
# Server Configuration
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=5000
MCP_DEBUG=false
MCP_SECRET_KEY=your-secret-key

# Logging
MCP_LOG_LEVEL=INFO
MCP_LOG_FILE=logs/mcp_server.log

# Storage
MCP_STORAGE_PATH=data/projects
MCP_DATABASE_PATH=src/database/app.db

# Overleaf Integration (Optional)
OVERLEAF_EMAIL=your-email@example.com
OVERLEAF_PASSWORD=your-password
OVERLEAF_API_URL=https://www.overleaf.com

# Security
MCP_ALLOWED_ORIGINS=*
MCP_MAX_REQUEST_SIZE=10485760
MCP_RATE_LIMIT=100
```

### Server Endpoints

- **Health Check:** `GET /health`
- **Capabilities:** `GET /capabilities`
- **MCP JSON-RPC:** `POST /mcp/jsonrpc`
- **Server-Sent Events:** `GET /sse/`
- **Status:** `GET /mcp/status`

## 🏗️ Architecture

The server is built with a modular architecture:

```
src/
├── main.py                 # Main server entry point
├── services/              # Core services
│   ├── mcp_server.py      # MCP protocol handler
│   ├── document_service.py # Document management
│   └── overleaf_service.py # Overleaf integration
├── mcp_components/        # MCP protocol components
│   ├── resources/         # Resource management
│   ├── tools/            # Tool implementations
│   └── prompts/          # Prompt templates
├── routes/               # HTTP routes
│   ├── mcp.py           # MCP JSON-RPC endpoints
│   └── sse.py           # Server-Sent Events
└── utils/               # Utilities
    ├── config.py        # Configuration management
    └── logger.py        # Logging setup
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_mcp_server.py
```

This tests:
- Server health and capabilities
- MCP protocol compliance
- Resource management
- Tool operations
- Prompt generation
- SSE endpoints

## 🚀 Deployment

### Local Development

```bash
python src/main.py
```

### Production Deployment

1. **Using Docker:**
```bash
docker build -t overleaf-mcp-server .
docker run -p 5000:5000 overleaf-mcp-server
```

2. **Using Docker Compose:**
```bash
docker-compose up -d
```

3. **Manual Deployment:**
```bash
# Install dependencies
pip install -r requirements.txt

# Set production environment
export MCP_DEBUG=false
export MCP_LOG_LEVEL=WARNING

# Start server
python src/main.py
```

### Public Access

For Claude.ai to connect to your server, it must be publicly accessible. Options include:

1. **Cloud deployment** (AWS, Google Cloud, Azure)
2. **VPS hosting** (DigitalOcean, Linode, etc.)
3. **Tunneling services** (ngrok, cloudflare tunnel)

## 🔒 Security

- **CORS enabled** for Claude.ai integration
- **Rate limiting** to prevent abuse
- **Input validation** for all requests
- **Secure configuration** options
- **Optional authentication** for production use

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation:** See the `docs/` directory for detailed guides
- **Issues:** Report bugs and feature requests on GitHub
- **Discussions:** Join the community discussions

## 🙏 Acknowledgments

- **Anthropic** for the Model Context Protocol specification
- **Overleaf** for the collaborative LaTeX platform
- **Flask** and **Python** communities for excellent tools

---

**Ready to revolutionize your academic writing with AI? Start using the Overleaf Remote MCP Server today!** 🚀

