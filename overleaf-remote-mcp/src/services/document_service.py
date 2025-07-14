"""
Document Service

This module provides document management functionality for the Overleaf Remote MCP Server.
It handles local document storage, version control, and project management.
"""

import os
import json
import uuid
import sqlite3
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from src.utils.config import Config

logger = logging.getLogger(__name__)

class DocumentService:
    """
    Document service for managing Overleaf projects and documents locally.
    
    This service provides CRUD operations for projects and documents,
    version control, and local storage management.
    """
    
    def __init__(self, config: Config):
        """
        Initialize the document service.
        
        Args:
            config: Configuration instance
        """
        self.config = config
        self.db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'app.db')
        self.storage_path = config.get_storage_path()
        self.initialized = False
        
        logger.info("Document Service initialized")
    
    def initialize(self) -> None:
        """Initialize the document service and database."""
        try:
            # Ensure storage directory exists
            os.makedirs(self.storage_path, exist_ok=True)
            
            # Initialize database
            self._init_database()
            
            self.initialized = True
            logger.info("Document Service database initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize Document Service: {e}")
            raise
    
    def _init_database(self) -> None:
        """Initialize the database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Projects table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    type TEXT NOT NULL,
                    template_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    overleaf_id TEXT,
                    settings TEXT,
                    status TEXT DEFAULT 'active'
                )
            ''')
            
            # Documents table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (id),
                    UNIQUE(project_id, filename)
                )
            ''')
            
            # Versions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS versions (
                    id TEXT PRIMARY KEY,
                    document_id TEXT NOT NULL,
                    version_number INTEGER NOT NULL,
                    content TEXT,
                    commit_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (document_id) REFERENCES documents (id)
                )
            ''')
            
            # Templates table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS templates (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    document_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            
            # Insert default templates if they don't exist
            self._insert_default_templates(cursor)
            conn.commit()
    
    def _insert_default_templates(self, cursor) -> None:
        """Insert default LaTeX templates."""
        templates = [
            {
                'id': 'article_basic',
                'name': 'Basic Article',
                'document_type': 'article',
                'description': 'Basic LaTeX article template',
                'content': '''\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\usepackage{amsmath}
\\usepackage{amsfonts}
\\usepackage{amssymb}
\\usepackage{graphicx}

\\title{Document Title}
\\author{Author Name}
\\date{\\today}

\\begin{document}

\\maketitle

\\begin{abstract}
Your abstract goes here.
\\end{abstract}

\\section{Introduction}
Your introduction goes here.

\\section{Methodology}
Your methodology goes here.

\\section{Results}
Your results go here.

\\section{Conclusion}
Your conclusion goes here.

\\bibliographystyle{plain}
\\bibliography{references}

\\end{document}'''
            },
            {
                'id': 'report_basic',
                'name': 'Basic Report',
                'document_type': 'report',
                'description': 'Basic LaTeX report template',
                'content': '''\\documentclass{report}
\\usepackage[utf8]{inputenc}
\\usepackage{amsmath}
\\usepackage{amsfonts}
\\usepackage{amssymb}
\\usepackage{graphicx}

\\title{Report Title}
\\author{Author Name}
\\date{\\today}

\\begin{document}

\\maketitle

\\tableofcontents

\\chapter{Introduction}
Your introduction goes here.

\\chapter{Background}
Your background goes here.

\\chapter{Methodology}
Your methodology goes here.

\\chapter{Results}
Your results go here.

\\chapter{Discussion}
Your discussion goes here.

\\chapter{Conclusion}
Your conclusion goes here.

\\bibliographystyle{plain}
\\bibliography{references}

\\end{document}'''
            }
        ]
        
        for template in templates:
            cursor.execute('''
                INSERT OR IGNORE INTO templates (id, name, document_type, content, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (template['id'], template['name'], template['document_type'], 
                  template['content'], template['description']))
    
    # Project operations
    
    def create_project(self, title: str, document_type: str, template_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new project.
        
        Args:
            title: Project title
            document_type: Type of document (article, report, etc.)
            template_id: Optional template ID to use
            
        Returns:
            Project information
        """
        project_id = str(uuid.uuid4())
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO projects (id, title, type, template_id)
                VALUES (?, ?, ?, ?)
            ''', (project_id, title, document_type, template_id))
            
            conn.commit()
        
        # Create project directory
        project_dir = os.path.join(self.storage_path, project_id)
        os.makedirs(project_dir, exist_ok=True)
        os.makedirs(os.path.join(project_dir, 'documents'), exist_ok=True)
        os.makedirs(os.path.join(project_dir, 'assets'), exist_ok=True)
        os.makedirs(os.path.join(project_dir, 'compiled'), exist_ok=True)
        
        # Create main document from template
        if template_id:
            template = self.get_template(template_id)
            if template:
                self.create_document(project_id, 'main.tex', template['content'])
        else:
            # Create empty main document
            self.create_document(project_id, 'main.tex', '% Main document\n')
        
        logger.info(f"Created project: {project_id} - {title}")
        
        return {
            'id': project_id,
            'title': title,
            'type': document_type,
            'template_id': template_id,
            'created_at': datetime.utcnow().isoformat()
        }
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, type, template_id, created_at, updated_at, overleaf_id, status
                FROM projects
                WHERE status = 'active'
                ORDER BY updated_at DESC
            ''')
            
            projects = []
            for row in cursor.fetchall():
                projects.append({
                    'id': row[0],
                    'title': row[1],
                    'type': row[2],
                    'template_id': row[3],
                    'created_at': row[4],
                    'updated_at': row[5],
                    'overleaf_id': row[6],
                    'status': row[7]
                })
            
            return projects
    
    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get project by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, type, template_id, created_at, updated_at, overleaf_id, settings, status
                FROM projects
                WHERE id = ?
            ''', (project_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'title': row[1],
                    'type': row[2],
                    'template_id': row[3],
                    'created_at': row[4],
                    'updated_at': row[5],
                    'overleaf_id': row[6],
                    'settings': json.loads(row[7]) if row[7] else {},
                    'status': row[8]
                }
            
            return None
    
    # Document operations
    
    def create_document(self, project_id: str, filename: str, content: str = '') -> Dict[str, Any]:
        """
        Create a new document in a project.
        
        Args:
            project_id: Project ID
            filename: Document filename
            content: Initial content
            
        Returns:
            Document information
        """
        document_id = str(uuid.uuid4())
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO documents (id, project_id, filename, content)
                VALUES (?, ?, ?, ?)
            ''', (document_id, project_id, filename, content))
            
            conn.commit()
        
        # Save to file system
        project_dir = os.path.join(self.storage_path, project_id, 'documents')
        file_path = os.path.join(project_dir, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Created document: {filename} in project {project_id}")
        
        return {
            'id': document_id,
            'project_id': project_id,
            'filename': filename,
            'content': content,
            'created_at': datetime.utcnow().isoformat()
        }
    
    def list_documents(self, project_id: str) -> List[Dict[str, Any]]:
        """List all documents in a project."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, filename, created_at, updated_at
                FROM documents
                WHERE project_id = ?
                ORDER BY filename
            ''', (project_id,))
            
            documents = []
            for row in cursor.fetchall():
                documents.append({
                    'id': row[0],
                    'filename': row[1],
                    'created_at': row[2],
                    'updated_at': row[3]
                })
            
            return documents
    
    def get_document(self, project_id: str, filename: str) -> Optional[Dict[str, Any]]:
        """Get document content."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, content, created_at, updated_at
                FROM documents
                WHERE project_id = ? AND filename = ?
            ''', (project_id, filename))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'project_id': project_id,
                    'filename': filename,
                    'content': row[1],
                    'created_at': row[2],
                    'updated_at': row[3]
                }
            
            return None
    
    def update_document(self, project_id: str, filename: str, content: str, commit_message: str = '') -> bool:
        """Update document content."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get current document
                cursor.execute('''
                    SELECT id, content FROM documents
                    WHERE project_id = ? AND filename = ?
                ''', (project_id, filename))
                
                row = cursor.fetchone()
                if not row:
                    return False
                
                document_id, old_content = row
                
                # Create version entry
                cursor.execute('''
                    SELECT COALESCE(MAX(version_number), 0) + 1
                    FROM versions
                    WHERE document_id = ?
                ''', (document_id,))
                
                version_number = cursor.fetchone()[0]
                
                cursor.execute('''
                    INSERT INTO versions (id, document_id, version_number, content, commit_message)
                    VALUES (?, ?, ?, ?, ?)
                ''', (str(uuid.uuid4()), document_id, version_number, old_content, commit_message))
                
                # Update document
                cursor.execute('''
                    UPDATE documents
                    SET content = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (content, document_id))
                
                # Update project timestamp
                cursor.execute('''
                    UPDATE projects
                    SET updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (project_id,))
                
                conn.commit()
            
            # Save to file system
            project_dir = os.path.join(self.storage_path, project_id, 'documents')
            file_path = os.path.join(project_dir, filename)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Updated document: {filename} in project {project_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating document {filename}: {e}")
            return False
    
    # Template operations
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """List all available templates."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, document_type, description, created_at
                FROM templates
                ORDER BY name
            ''')
            
            templates = []
            for row in cursor.fetchall():
                templates.append({
                    'id': row[0],
                    'name': row[1],
                    'document_type': row[2],
                    'description': row[3],
                    'created_at': row[4]
                })
            
            return templates
    
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get template by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, document_type, content, description, created_at
                FROM templates
                WHERE id = ?
            ''', (template_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'name': row[1],
                    'document_type': row[2],
                    'content': row[3],
                    'description': row[4],
                    'created_at': row[5]
                }
            
            return None
    
    def shutdown(self) -> None:
        """Shutdown the document service."""
        logger.info("Document Service shutdown completed")

