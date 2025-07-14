"""
Resource Manager

This module implements MCP resource management for the Overleaf Remote MCP Server.
It provides access to projects, documents, templates, and other resources.
"""

import logging
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

from mcp import types
from src.services.document_service import DocumentService
from src.services.overleaf_service import OverleafService

logger = logging.getLogger(__name__)

class ResourceManager:
    """
    Resource manager for MCP protocol.
    
    This class manages all resources exposed through the MCP protocol,
    including projects, documents, templates, and compilation results.
    """
    
    OVERLEAF_SCHEME = "overleaf-remote"
    
    def __init__(self, document_service: DocumentService, overleaf_service: OverleafService):
        """
        Initialize the resource manager.
        
        Args:
            document_service: Document service instance
            overleaf_service: Overleaf service instance
        """
        self.document_service = document_service
        self.overleaf_service = overleaf_service
        
        logger.info("Resource Manager initialized")
    
    def list_resources_metadata(self) -> Dict[str, Any]:
        """
        Get resource metadata for MCP discovery.
        
        Returns:
            Resource metadata dictionary
        """
        return {
            "subscribe": True,
            "listChanged": True
        }
    
    def list_resources(self) -> List[types.Resource]:
        """
        List all available resources.
        
        Returns:
            List of MCP resources
        """
        try:
            resources = []
            
            # Get all projects from document service
            projects = self.document_service.list_projects()
            
            for project in projects:
                # Add project metadata resource
                project_uri = f"{self.OVERLEAF_SCHEME}:///projects/{project['id']}/metadata"
                resources.append(types.Resource(
                    uri=project_uri,
                    name=f"Project: {project['title']}",
                    description=f"Metadata for project '{project['title']}'",
                    mimeType="application/json"
                ))
                
                # Add document resources for each file in the project
                documents = self.document_service.list_documents(project['id'])
                for doc in documents:
                    doc_uri = f"{self.OVERLEAF_SCHEME}:///projects/{project['id']}/documents/{doc['filename']}"
                    
                    # Determine MIME type based on file extension
                    mime_type = self._get_mime_type(doc['filename'])
                    
                    resources.append(types.Resource(
                        uri=doc_uri,
                        name=f"Document: {doc['filename']}",
                        description=f"LaTeX document '{doc['filename']}' in project '{project['title']}'",
                        mimeType=mime_type
                    ))
                
                # Add version history resource
                history_uri = f"{self.OVERLEAF_SCHEME}:///projects/{project['id']}/history"
                resources.append(types.Resource(
                    uri=history_uri,
                    name=f"Version History: {project['title']}",
                    description=f"Version history for project '{project['title']}'",
                    mimeType="application/json"
                ))
                
                # Add compilation status resource
                compilation_uri = f"{self.OVERLEAF_SCHEME}:///projects/{project['id']}/compilation"
                resources.append(types.Resource(
                    uri=compilation_uri,
                    name=f"Compilation Status: {project['title']}",
                    description=f"Compilation status and results for project '{project['title']}'",
                    mimeType="application/json"
                ))
            
            # Add template resources
            templates = self.document_service.list_templates()
            for template in templates:
                template_uri = f"{self.OVERLEAF_SCHEME}:///templates/{template['id']}"
                resources.append(types.Resource(
                    uri=template_uri,
                    name=f"Template: {template['name']}",
                    description=f"LaTeX template for {template['document_type']}",
                    mimeType="text/x-latex"
                ))
            
            logger.info(f"Listed {len(resources)} resources")
            return resources
            
        except Exception as e:
            logger.error(f"Error listing resources: {e}")
            raise
    
    def read_resource(self, uri: str) -> str:
        """
        Read the content of a specific resource.
        
        Args:
            uri: Resource URI
            
        Returns:
            Resource content as string
        """
        try:
            uri_str = str(uri)
            parsed_uri = urlparse(uri_str)
            
            if parsed_uri.scheme != self.OVERLEAF_SCHEME:
                raise ValueError(f"Unsupported URI scheme: {parsed_uri.scheme}")
            
            path_parts = parsed_uri.path.strip('/').split('/')
            
            if len(path_parts) < 2:
                raise ValueError(f"Invalid URI format: {uri_str}")
            
            resource_type = path_parts[0]
            
            if resource_type == "projects":
                return self._read_project_resource(path_parts[1:], parsed_uri.query)
            elif resource_type == "templates":
                return self._read_template_resource(path_parts[1:])
            else:
                raise ValueError(f"Unknown resource type: {resource_type}")
                
        except Exception as e:
            logger.error(f"Failed to read resource {uri}: {e}")
            raise
    
    def _read_project_resource(self, path_parts: List[str], query: str) -> str:
        """Read project-related resource."""
        if len(path_parts) < 2:
            raise ValueError("Invalid project resource path")
        
        project_id = path_parts[0]
        resource_type = path_parts[1]
        
        project = self.document_service.get_project(project_id)
        if not project:
            raise ValueError(f"Project not found: {project_id}")
        
        if resource_type == "metadata":
            return self._get_project_metadata(project)
        elif resource_type == "documents":
            if len(path_parts) < 3:
                raise ValueError("Document filename required")
            filename = path_parts[2]
            return self._get_document_content(project_id, filename)
        elif resource_type == "history":
            return self._get_project_history(project_id)
        elif resource_type == "compilation":
            return self._get_compilation_status(project_id)
        else:
            raise ValueError(f"Unknown project resource type: {resource_type}")
    
    def _read_template_resource(self, path_parts: List[str]) -> str:
        """Read template resource."""
        if len(path_parts) < 1:
            raise ValueError("Template ID required")
        
        template_id = path_parts[0]
        template = self.document_service.get_template(template_id)
        
        if not template:
            raise ValueError(f"Template not found: {template_id}")
        
        return template['content']
    
    def _get_project_metadata(self, project: Dict[str, Any]) -> str:
        """Get project metadata as JSON."""
        import json
        
        # Get document count
        documents = self.document_service.list_documents(project['id'])
        
        metadata = {
            'id': project['id'],
            'title': project['title'],
            'type': project['type'],
            'template_id': project.get('template_id'),
            'created_at': project['created_at'],
            'updated_at': project['updated_at'],
            'overleaf_id': project.get('overleaf_id'),
            'status': project.get('status', 'active'),
            'settings': project.get('settings', {}),
            'document_count': len(documents),
            'documents': [doc['filename'] for doc in documents]
        }
        
        return json.dumps(metadata, indent=2)
    
    def _get_document_content(self, project_id: str, filename: str) -> str:
        """Get document content."""
        document = self.document_service.get_document(project_id, filename)
        if not document:
            raise ValueError(f"Document not found: {filename}")
        
        return document['content'] or ''
    
    def _get_project_history(self, project_id: str) -> str:
        """Get project version history as JSON."""
        import json
        
        # This would typically query the versions table
        # For now, return a mock history
        history = {
            'project_id': project_id,
            'versions': [
                {
                    'version': 1,
                    'timestamp': '2024-01-15T10:30:00Z',
                    'message': 'Initial project creation',
                    'author': 'user'
                },
                {
                    'version': 2,
                    'timestamp': '2024-01-16T14:20:00Z',
                    'message': 'Added introduction section',
                    'author': 'user'
                }
            ]
        }
        
        return json.dumps(history, indent=2)
    
    def _get_compilation_status(self, project_id: str) -> str:
        """Get compilation status as JSON."""
        import json
        
        # Get status from Overleaf service if available
        if self.overleaf_service.is_available():
            project = self.document_service.get_project(project_id)
            if project and project.get('overleaf_id'):
                status = self.overleaf_service.get_compilation_status(project['overleaf_id'])
            else:
                status = {
                    'status': 'not_synced',
                    'message': 'Project not synced to Overleaf'
                }
        else:
            status = {
                'status': 'offline',
                'message': 'Overleaf service not available'
            }
        
        return json.dumps(status, indent=2)
    
    def _get_mime_type(self, filename: str) -> str:
        """Get MIME type based on file extension."""
        extension = filename.lower().split('.')[-1] if '.' in filename else ''
        
        mime_types = {
            'tex': 'text/x-latex',
            'bib': 'text/x-bibtex',
            'cls': 'text/x-latex',
            'sty': 'text/x-latex',
            'txt': 'text/plain',
            'md': 'text/markdown',
            'json': 'application/json',
            'pdf': 'application/pdf',
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'gif': 'image/gif',
            'svg': 'image/svg+xml'
        }
        
        return mime_types.get(extension, 'text/plain')
    
    def get_mime_type(self, uri: str) -> str:
        """Get MIME type for a resource URI."""
        try:
            parsed_uri = urlparse(str(uri))
            path_parts = parsed_uri.path.strip('/').split('/')
            
            if len(path_parts) >= 3 and path_parts[0] == "projects" and path_parts[2] == "documents":
                if len(path_parts) >= 4:
                    filename = path_parts[3]
                    return self._get_mime_type(filename)
            elif len(path_parts) >= 2 and path_parts[0] == "templates":
                return "text/x-latex"
            
            return "application/json"
            
        except Exception:
            return "text/plain"

