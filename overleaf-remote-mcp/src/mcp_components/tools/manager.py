"""
Tool Manager

This module implements MCP tools for Overleaf operations.
It provides tools for creating, editing, and managing documents and projects.
"""

import logging
import json
from typing import List, Dict, Any, Optional

from mcp import types
from src.services.document_service import DocumentService
from src.services.overleaf_service import OverleafService

logger = logging.getLogger(__name__)

class ToolManager:
    """
    Tool manager for MCP protocol.
    
    This class manages all tools exposed through the MCP protocol,
    providing functionality for document and project operations.
    """
    
    def __init__(self, document_service: DocumentService, overleaf_service: OverleafService):
        """
        Initialize the tool manager.
        
        Args:
            document_service: Document service instance
            overleaf_service: Overleaf service instance
        """
        self.document_service = document_service
        self.overleaf_service = overleaf_service
        
        logger.info("Tool Manager initialized")
    
    def list_tools_metadata(self) -> Dict[str, Any]:
        """
        Get tool metadata for MCP discovery.
        
        Returns:
            Tool metadata dictionary
        """
        return {
            "listChanged": True
        }
    
    def list_tools(self) -> List[types.Tool]:
        """
        List all available tools.
        
        Returns:
            List of MCP tools
        """
        tools = [
            # Project management tools
            types.Tool(
                name="create_project",
                description="Create a new LaTeX project",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Project title"
                        },
                        "document_type": {
                            "type": "string",
                            "enum": ["article", "report", "book", "thesis"],
                            "description": "Type of document to create"
                        },
                        "template_id": {
                            "type": "string",
                            "description": "Optional template ID to use"
                        }
                    },
                    "required": ["title", "document_type"]
                }
            ),
            
            types.Tool(
                name="list_projects",
                description="List all projects",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            
            types.Tool(
                name="get_project",
                description="Get project details",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "Project ID"
                        }
                    },
                    "required": ["project_id"]
                }
            ),
            
            # Document management tools
            types.Tool(
                name="create_document",
                description="Create a new document in a project",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "Project ID"
                        },
                        "filename": {
                            "type": "string",
                            "description": "Document filename (e.g., 'chapter1.tex')"
                        },
                        "content": {
                            "type": "string",
                            "description": "Initial document content"
                        }
                    },
                    "required": ["project_id", "filename"]
                }
            ),
            
            types.Tool(
                name="update_document",
                description="Update document content",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "Project ID"
                        },
                        "filename": {
                            "type": "string",
                            "description": "Document filename"
                        },
                        "content": {
                            "type": "string",
                            "description": "New document content"
                        },
                        "commit_message": {
                            "type": "string",
                            "description": "Optional commit message for version control"
                        }
                    },
                    "required": ["project_id", "filename", "content"]
                }
            ),
            
            types.Tool(
                name="get_document",
                description="Get document content",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "Project ID"
                        },
                        "filename": {
                            "type": "string",
                            "description": "Document filename"
                        }
                    },
                    "required": ["project_id", "filename"]
                }
            ),
            
            types.Tool(
                name="list_documents",
                description="List all documents in a project",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "Project ID"
                        }
                    },
                    "required": ["project_id"]
                }
            ),
            
            # Content generation tools
            types.Tool(
                name="generate_section",
                description="Generate LaTeX content for a specific section",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "section_type": {
                            "type": "string",
                            "enum": ["abstract", "introduction", "methodology", "results", "discussion", "conclusion", "bibliography"],
                            "description": "Type of section to generate"
                        },
                        "topic": {
                            "type": "string",
                            "description": "Topic or subject matter"
                        },
                        "context": {
                            "type": "string",
                            "description": "Additional context or requirements"
                        },
                        "length": {
                            "type": "string",
                            "enum": ["short", "medium", "long"],
                            "description": "Desired length of the section"
                        }
                    },
                    "required": ["section_type", "topic"]
                }
            ),
            
            types.Tool(
                name="improve_content",
                description="Improve existing LaTeX content",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "Existing LaTeX content to improve"
                        },
                        "improvement_type": {
                            "type": "string",
                            "enum": ["clarity", "academic_style", "grammar", "structure", "citations"],
                            "description": "Type of improvement to apply"
                        },
                        "instructions": {
                            "type": "string",
                            "description": "Specific instructions for improvement"
                        }
                    },
                    "required": ["content", "improvement_type"]
                }
            ),
            
            # Template tools
            types.Tool(
                name="list_templates",
                description="List available LaTeX templates",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            
            types.Tool(
                name="get_template",
                description="Get template content",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "template_id": {
                            "type": "string",
                            "description": "Template ID"
                        }
                    },
                    "required": ["template_id"]
                }
            ),
            
            # Overleaf integration tools
            types.Tool(
                name="sync_to_overleaf",
                description="Synchronize project to Overleaf",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "Local project ID to sync"
                        }
                    },
                    "required": ["project_id"]
                }
            ),
            
            types.Tool(
                name="compile_project",
                description="Compile LaTeX project to PDF",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "Project ID to compile"
                        }
                    },
                    "required": ["project_id"]
                }
            )
        ]
        
        logger.info(f"Listed {len(tools)} tools")
        return tools
    
    def call_tool(self, name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """
        Call a specific tool with given arguments.
        
        Args:
            name: Tool name
            arguments: Tool arguments
            
        Returns:
            List of content results
        """
        try:
            logger.info(f"Calling tool: {name}")
            
            if name == "create_project":
                return self._create_project(arguments)
            elif name == "list_projects":
                return self._list_projects(arguments)
            elif name == "get_project":
                return self._get_project(arguments)
            elif name == "create_document":
                return self._create_document(arguments)
            elif name == "update_document":
                return self._update_document(arguments)
            elif name == "get_document":
                return self._get_document(arguments)
            elif name == "list_documents":
                return self._list_documents(arguments)
            elif name == "generate_section":
                return self._generate_section(arguments)
            elif name == "improve_content":
                return self._improve_content(arguments)
            elif name == "list_templates":
                return self._list_templates(arguments)
            elif name == "get_template":
                return self._get_template(arguments)
            elif name == "sync_to_overleaf":
                return self._sync_to_overleaf(arguments)
            elif name == "compile_project":
                return self._compile_project(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")
                
        except Exception as e:
            logger.error(f"Error calling tool {name}: {e}")
            return [types.TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )]
    
    # Tool implementations
    
    def _create_project(self, args: Dict[str, Any]) -> List[types.TextContent]:
        """Create a new project."""
        title = args["title"]
        document_type = args["document_type"]
        template_id = args.get("template_id")
        
        project = self.document_service.create_project(title, document_type, template_id)
        
        return [types.TextContent(
            type="text",
            text=f"Created project '{title}' with ID: {project['id']}\n\n" +
                 json.dumps(project, indent=2)
        )]
    
    def _list_projects(self, args: Dict[str, Any]) -> List[types.TextContent]:
        """List all projects."""
        projects = self.document_service.list_projects()
        
        if not projects:
            return [types.TextContent(
                type="text",
                text="No projects found."
            )]
        
        project_list = "\n".join([
            f"- {p['title']} (ID: {p['id']}, Type: {p['type']})"
            for p in projects
        ])
        
        return [types.TextContent(
            type="text",
            text=f"Found {len(projects)} projects:\n\n{project_list}\n\n" +
                 json.dumps(projects, indent=2)
        )]
    
    def _get_project(self, args: Dict[str, Any]) -> List[types.TextContent]:
        """Get project details."""
        project_id = args["project_id"]
        project = self.document_service.get_project(project_id)
        
        if not project:
            return [types.TextContent(
                type="text",
                text=f"Project not found: {project_id}"
            )]
        
        documents = self.document_service.list_documents(project_id)
        
        return [types.TextContent(
            type="text",
            text=f"Project: {project['title']}\n\n" +
                 f"Documents ({len(documents)}):\n" +
                 "\n".join([f"- {d['filename']}" for d in documents]) +
                 f"\n\nProject Details:\n{json.dumps(project, indent=2)}"
        )]
    
    def _create_document(self, args: Dict[str, Any]) -> List[types.TextContent]:
        """Create a new document."""
        project_id = args["project_id"]
        filename = args["filename"]
        content = args.get("content", "")
        
        document = self.document_service.create_document(project_id, filename, content)
        
        return [types.TextContent(
            type="text",
            text=f"Created document '{filename}' in project {project_id}\n\n" +
                 json.dumps(document, indent=2)
        )]
    
    def _update_document(self, args: Dict[str, Any]) -> List[types.TextContent]:
        """Update document content."""
        project_id = args["project_id"]
        filename = args["filename"]
        content = args["content"]
        commit_message = args.get("commit_message", "Updated via MCP")
        
        success = self.document_service.update_document(
            project_id, filename, content, commit_message
        )
        
        if success:
            return [types.TextContent(
                type="text",
                text=f"Successfully updated document '{filename}' in project {project_id}"
            )]
        else:
            return [types.TextContent(
                type="text",
                text=f"Failed to update document '{filename}' in project {project_id}"
            )]
    
    def _get_document(self, args: Dict[str, Any]) -> List[types.TextContent]:
        """Get document content."""
        project_id = args["project_id"]
        filename = args["filename"]
        
        document = self.document_service.get_document(project_id, filename)
        
        if not document:
            return [types.TextContent(
                type="text",
                text=f"Document not found: {filename} in project {project_id}"
            )]
        
        return [types.TextContent(
            type="text",
            text=f"Document: {filename}\n\n{document['content']}"
        )]
    
    def _list_documents(self, args: Dict[str, Any]) -> List[types.TextContent]:
        """List documents in a project."""
        project_id = args["project_id"]
        documents = self.document_service.list_documents(project_id)
        
        if not documents:
            return [types.TextContent(
                type="text",
                text=f"No documents found in project {project_id}"
            )]
        
        doc_list = "\n".join([
            f"- {d['filename']} (Created: {d['created_at']})"
            for d in documents
        ])
        
        return [types.TextContent(
            type="text",
            text=f"Documents in project {project_id}:\n\n{doc_list}"
        )]
    
    def _generate_section(self, args: Dict[str, Any]) -> List[types.TextContent]:
        """Generate LaTeX content for a section."""
        section_type = args["section_type"]
        topic = args["topic"]
        context = args.get("context", "")
        length = args.get("length", "medium")
        
        # This is a mock implementation
        # In a real implementation, this would use AI to generate content
        templates = {
            "abstract": f"""\\begin{{abstract}}
This paper presents a comprehensive study on {topic}. {context} The research methodology involves systematic analysis and evaluation. Key findings demonstrate significant implications for the field. The results contribute to our understanding of {topic} and provide valuable insights for future research.
\\end{{abstract}}""",
            
            "introduction": f"""\\section{{Introduction}}

{topic} has become increasingly important in recent years. {context} This research addresses the need for better understanding of the underlying principles and mechanisms.

The main objectives of this study are:
\\begin{{itemize}}
    \\item To investigate the fundamental aspects of {topic}
    \\item To analyze current approaches and methodologies
    \\item To propose improvements and novel solutions
\\end{{itemize}}

This paper is organized as follows: Section 2 presents the background and related work, Section 3 describes the methodology, Section 4 presents the results, and Section 5 concludes the paper.""",
            
            "methodology": f"""\\section{{Methodology}}

This section describes the research methodology employed in this study of {topic}. {context}

\\subsection{{Research Design}}
The research follows a systematic approach combining theoretical analysis with empirical evaluation.

\\subsection{{Data Collection}}
Data was collected through multiple sources to ensure comprehensive coverage of the research domain.

\\subsection{{Analysis Framework}}
The analysis framework incorporates both quantitative and qualitative methods to provide robust insights.""",
            
            "results": f"""\\section{{Results}}

This section presents the findings of our investigation into {topic}. {context}

\\subsection{{Primary Findings}}
The analysis revealed several key insights:

\\begin{{itemize}}
    \\item Significant improvement in performance metrics
    \\item Enhanced understanding of underlying mechanisms
    \\item Novel patterns and relationships identified
\\end{{itemize}}

\\subsection{{Statistical Analysis}}
Statistical analysis confirms the significance of the observed results (p < 0.05).

\\subsection{{Discussion of Results}}
These findings have important implications for the field and suggest new directions for future research.""",
            
            "conclusion": f"""\\section{{Conclusion}}

This study has provided valuable insights into {topic}. {context} The research has successfully addressed the initial objectives and contributed to the advancement of knowledge in this field.

\\subsection{{Key Contributions}}
The main contributions of this work include:
\\begin{{itemize}}
    \\item Novel theoretical framework for understanding {topic}
    \\item Empirical validation of proposed approaches
    \\item Practical implications for real-world applications
\\end{{itemize}}

\\subsection{{Future Work}}
Future research directions include extending the current framework and exploring additional applications in related domains."""
        }
        
        content = templates.get(section_type, f"% {section_type.title()} section for {topic}\n% {context}")
        
        return [types.TextContent(
            type="text",
            text=f"Generated {section_type} section for '{topic}':\n\n{content}"
        )]
    
    def _improve_content(self, args: Dict[str, Any]) -> List[types.TextContent]:
        """Improve existing content."""
        content = args["content"]
        improvement_type = args["improvement_type"]
        instructions = args.get("instructions", "")
        
        # Mock improvement - in reality, this would use AI
        improved_content = f"% Improved for {improvement_type}\n% {instructions}\n\n{content}"
        
        return [types.TextContent(
            type="text",
            text=f"Improved content ({improvement_type}):\n\n{improved_content}"
        )]
    
    def _list_templates(self, args: Dict[str, Any]) -> List[types.TextContent]:
        """List available templates."""
        templates = self.document_service.list_templates()
        
        if not templates:
            return [types.TextContent(
                type="text",
                text="No templates available."
            )]
        
        template_list = "\n".join([
            f"- {t['name']} (ID: {t['id']}, Type: {t['document_type']})"
            for t in templates
        ])
        
        return [types.TextContent(
            type="text",
            text=f"Available templates:\n\n{template_list}"
        )]
    
    def _get_template(self, args: Dict[str, Any]) -> List[types.TextContent]:
        """Get template content."""
        template_id = args["template_id"]
        template = self.document_service.get_template(template_id)
        
        if not template:
            return [types.TextContent(
                type="text",
                text=f"Template not found: {template_id}"
            )]
        
        return [types.TextContent(
            type="text",
            text=f"Template: {template['name']}\n\n{template['content']}"
        )]
    
    def _sync_to_overleaf(self, args: Dict[str, Any]) -> List[types.TextContent]:
        """Sync project to Overleaf."""
        project_id = args["project_id"]
        
        project = self.document_service.get_project(project_id)
        if not project:
            return [types.TextContent(
                type="text",
                text=f"Project not found: {project_id}"
            )]
        
        documents = self.document_service.list_documents(project_id)
        doc_contents = []
        for doc in documents:
            doc_data = self.document_service.get_document(project_id, doc['filename'])
            if doc_data:
                doc_contents.append(doc_data)
        
        overleaf_id = self.overleaf_service.sync_project_to_overleaf(project, doc_contents)
        
        if overleaf_id:
            return [types.TextContent(
                type="text",
                text=f"Successfully synced project to Overleaf. Overleaf ID: {overleaf_id}"
            )]
        else:
            return [types.TextContent(
                type="text",
                text="Failed to sync project to Overleaf. Check Overleaf service configuration."
            )]
    
    def _compile_project(self, args: Dict[str, Any]) -> List[types.TextContent]:
        """Compile project to PDF."""
        project_id = args["project_id"]
        
        project = self.document_service.get_project(project_id)
        if not project:
            return [types.TextContent(
                type="text",
                text=f"Project not found: {project_id}"
            )]
        
        overleaf_id = project.get('overleaf_id')
        if not overleaf_id:
            return [types.TextContent(
                type="text",
                text="Project not synced to Overleaf. Use sync_to_overleaf tool first."
            )]
        
        result = self.overleaf_service.compile_project(overleaf_id)
        
        if result['success']:
            return [types.TextContent(
                type="text",
                text=f"Compilation successful!\nPDF URL: {result.get('pdf_url', 'N/A')}\nLog: {result.get('log', 'N/A')}"
            )]
        else:
            return [types.TextContent(
                type="text",
                text=f"Compilation failed: {result.get('error', 'Unknown error')}"
            )]

