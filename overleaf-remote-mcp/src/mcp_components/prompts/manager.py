"""
Prompt Manager

This module implements MCP prompts for content generation and document assistance.
It provides pre-defined prompts for various academic writing tasks.
"""

import logging
from typing import List, Dict, Any

from mcp import types

logger = logging.getLogger(__name__)

class PromptManager:
    """
    Prompt manager for MCP protocol.
    
    This class manages all prompts exposed through the MCP protocol,
    providing templates for academic writing and document generation.
    """
    
    def __init__(self):
        """Initialize the prompt manager."""
        logger.info("Prompt Manager initialized")
    
    def list_prompts_metadata(self) -> Dict[str, Any]:
        """
        Get prompt metadata for MCP discovery.
        
        Returns:
            Prompt metadata dictionary
        """
        return {
            "listChanged": True
        }
    
    def list_prompts(self) -> List[types.Prompt]:
        """
        List all available prompts.
        
        Returns:
            List of MCP prompts
        """
        prompts = [
            types.Prompt(
                name="write_abstract",
                description="Generate an abstract for an academic paper",
                arguments=[
                    types.PromptArgument(
                        name="title",
                        description="Paper title",
                        required=True
                    ),
                    types.PromptArgument(
                        name="research_area",
                        description="Research area or field",
                        required=True
                    ),
                    types.PromptArgument(
                        name="key_findings",
                        description="Key findings or contributions",
                        required=False
                    ),
                    types.PromptArgument(
                        name="methodology",
                        description="Research methodology used",
                        required=False
                    )
                ]
            ),
            
            types.Prompt(
                name="write_introduction",
                description="Generate an introduction section for an academic paper",
                arguments=[
                    types.PromptArgument(
                        name="topic",
                        description="Main topic or subject",
                        required=True
                    ),
                    types.PromptArgument(
                        name="research_question",
                        description="Research question or problem statement",
                        required=True
                    ),
                    types.PromptArgument(
                        name="background",
                        description="Background information",
                        required=False
                    ),
                    types.PromptArgument(
                        name="objectives",
                        description="Research objectives",
                        required=False
                    )
                ]
            ),
            
            types.Prompt(
                name="write_methodology",
                description="Generate a methodology section",
                arguments=[
                    types.PromptArgument(
                        name="research_type",
                        description="Type of research (experimental, theoretical, etc.)",
                        required=True
                    ),
                    types.PromptArgument(
                        name="data_collection",
                        description="Data collection methods",
                        required=False
                    ),
                    types.PromptArgument(
                        name="analysis_methods",
                        description="Analysis methods and tools",
                        required=False
                    ),
                    types.PromptArgument(
                        name="participants",
                        description="Participants or subjects",
                        required=False
                    )
                ]
            ),
            
            types.Prompt(
                name="write_results",
                description="Generate a results section",
                arguments=[
                    types.PromptArgument(
                        name="findings",
                        description="Main findings or results",
                        required=True
                    ),
                    types.PromptArgument(
                        name="data_analysis",
                        description="Data analysis results",
                        required=False
                    ),
                    types.PromptArgument(
                        name="statistical_significance",
                        description="Statistical significance information",
                        required=False
                    ),
                    types.PromptArgument(
                        name="figures_tables",
                        description="Description of figures and tables",
                        required=False
                    )
                ]
            ),
            
            types.Prompt(
                name="write_discussion",
                description="Generate a discussion section",
                arguments=[
                    types.PromptArgument(
                        name="results_summary",
                        description="Summary of key results",
                        required=True
                    ),
                    types.PromptArgument(
                        name="implications",
                        description="Implications of the findings",
                        required=False
                    ),
                    types.PromptArgument(
                        name="limitations",
                        description="Study limitations",
                        required=False
                    ),
                    types.PromptArgument(
                        name="future_work",
                        description="Suggestions for future work",
                        required=False
                    )
                ]
            ),
            
            types.Prompt(
                name="write_conclusion",
                description="Generate a conclusion section",
                arguments=[
                    types.PromptArgument(
                        name="main_contributions",
                        description="Main contributions of the work",
                        required=True
                    ),
                    types.PromptArgument(
                        name="research_question",
                        description="How the research question was answered",
                        required=False
                    ),
                    types.PromptArgument(
                        name="broader_impact",
                        description="Broader impact of the work",
                        required=False
                    )
                ]
            ),
            
            types.Prompt(
                name="improve_writing",
                description="Improve existing academic writing",
                arguments=[
                    types.PromptArgument(
                        name="text",
                        description="Text to improve",
                        required=True
                    ),
                    types.PromptArgument(
                        name="improvement_focus",
                        description="Focus area (clarity, flow, academic style, etc.)",
                        required=False
                    ),
                    types.PromptArgument(
                        name="target_audience",
                        description="Target audience",
                        required=False
                    )
                ]
            ),
            
            types.Prompt(
                name="create_outline",
                description="Create an outline for an academic paper",
                arguments=[
                    types.PromptArgument(
                        name="topic",
                        description="Paper topic",
                        required=True
                    ),
                    types.PromptArgument(
                        name="paper_type",
                        description="Type of paper (research, review, thesis, etc.)",
                        required=True
                    ),
                    types.PromptArgument(
                        name="length",
                        description="Expected length or page count",
                        required=False
                    ),
                    types.PromptArgument(
                        name="requirements",
                        description="Specific requirements or guidelines",
                        required=False
                    )
                ]
            ),
            
            types.Prompt(
                name="format_citations",
                description="Help format citations and bibliography",
                arguments=[
                    types.PromptArgument(
                        name="citation_style",
                        description="Citation style (APA, MLA, IEEE, etc.)",
                        required=True
                    ),
                    types.PromptArgument(
                        name="sources",
                        description="List of sources to cite",
                        required=True
                    ),
                    types.PromptArgument(
                        name="context",
                        description="Context where citations will be used",
                        required=False
                    )
                ]
            ),
            
            types.Prompt(
                name="latex_help",
                description="Get help with LaTeX formatting and commands",
                arguments=[
                    types.PromptArgument(
                        name="task",
                        description="LaTeX task or problem",
                        required=True
                    ),
                    types.PromptArgument(
                        name="document_class",
                        description="Document class being used",
                        required=False
                    ),
                    types.PromptArgument(
                        name="packages",
                        description="Packages already loaded",
                        required=False
                    )
                ]
            ),
            
            types.Prompt(
                name="research_proposal",
                description="Generate a research proposal",
                arguments=[
                    types.PromptArgument(
                        name="research_area",
                        description="Research area or field",
                        required=True
                    ),
                    types.PromptArgument(
                        name="problem_statement",
                        description="Problem statement or research gap",
                        required=True
                    ),
                    types.PromptArgument(
                        name="objectives",
                        description="Research objectives",
                        required=False
                    ),
                    types.PromptArgument(
                        name="methodology",
                        description="Proposed methodology",
                        required=False
                    ),
                    types.PromptArgument(
                        name="timeline",
                        description="Project timeline",
                        required=False
                    )
                ]
            )
        ]
        
        logger.info(f"Listed {len(prompts)} prompts")
        return prompts
    
    def get_prompt(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get a specific prompt with arguments filled in.
        
        Args:
            name: Prompt name
            arguments: Prompt arguments
            
        Returns:
            Prompt result with messages
        """
        try:
            logger.info(f"Getting prompt: {name}")
            
            if name == "write_abstract":
                return self._write_abstract_prompt(arguments)
            elif name == "write_introduction":
                return self._write_introduction_prompt(arguments)
            elif name == "write_methodology":
                return self._write_methodology_prompt(arguments)
            elif name == "write_results":
                return self._write_results_prompt(arguments)
            elif name == "write_discussion":
                return self._write_discussion_prompt(arguments)
            elif name == "write_conclusion":
                return self._write_conclusion_prompt(arguments)
            elif name == "improve_writing":
                return self._improve_writing_prompt(arguments)
            elif name == "create_outline":
                return self._create_outline_prompt(arguments)
            elif name == "format_citations":
                return self._format_citations_prompt(arguments)
            elif name == "latex_help":
                return self._latex_help_prompt(arguments)
            elif name == "research_proposal":
                return self._research_proposal_prompt(arguments)
            else:
                raise ValueError(f"Unknown prompt: {name}")
                
        except Exception as e:
            logger.error(f"Error getting prompt {name}: {e}")
            return {
                "messages": [
                    {
                        "role": "user",
                        "content": {
                            "type": "text",
                            "text": f"Error: {str(e)}"
                        }
                    }
                ]
            }
    
    # Prompt implementations
    
    def _write_abstract_prompt(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generate abstract writing prompt."""
        title = args.get("title", "")
        research_area = args.get("research_area", "")
        key_findings = args.get("key_findings", "")
        methodology = args.get("methodology", "")
        
        prompt = f"""Please write a comprehensive abstract for an academic paper with the following details:

Title: {title}
Research Area: {research_area}
Key Findings: {key_findings}
Methodology: {methodology}

The abstract should:
1. Clearly state the research problem and objectives
2. Briefly describe the methodology
3. Summarize the key findings
4. Highlight the significance and implications
5. Be approximately 150-250 words
6. Be written in LaTeX format with \\begin{{abstract}} and \\end{{abstract}} tags

Please ensure the abstract is concise, informative, and follows academic writing standards."""
        
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt
                    }
                }
            ]
        }
    
    def _write_introduction_prompt(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generate introduction writing prompt."""
        topic = args.get("topic", "")
        research_question = args.get("research_question", "")
        background = args.get("background", "")
        objectives = args.get("objectives", "")
        
        prompt = f"""Please write an introduction section for an academic paper with the following details:

Topic: {topic}
Research Question: {research_question}
Background: {background}
Objectives: {objectives}

The introduction should:
1. Provide context and background for the research
2. Clearly state the research problem or gap
3. Present the research question and objectives
4. Outline the paper structure
5. Be well-structured with logical flow
6. Include relevant citations (use placeholder citations like \\cite{{author2023}})
7. Be written in LaTeX format with \\section{{Introduction}}

Please ensure the introduction motivates the research and engages the reader."""
        
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt
                    }
                }
            ]
        }
    
    def _write_methodology_prompt(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generate methodology writing prompt."""
        research_type = args.get("research_type", "")
        data_collection = args.get("data_collection", "")
        analysis_methods = args.get("analysis_methods", "")
        participants = args.get("participants", "")
        
        prompt = f"""Please write a methodology section for an academic paper with the following details:

Research Type: {research_type}
Data Collection: {data_collection}
Analysis Methods: {analysis_methods}
Participants: {participants}

The methodology section should:
1. Describe the research design and approach
2. Detail data collection procedures
3. Explain analysis methods and tools
4. Describe participants or subjects (if applicable)
5. Address validity and reliability
6. Be written in LaTeX format with \\section{{Methodology}}
7. Include subsections as appropriate

Please ensure the methodology is detailed enough for replication."""
        
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt
                    }
                }
            ]
        }
    
    def _write_results_prompt(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generate results writing prompt."""
        findings = args.get("findings", "")
        data_analysis = args.get("data_analysis", "")
        statistical_significance = args.get("statistical_significance", "")
        figures_tables = args.get("figures_tables", "")
        
        prompt = f"""Please write a results section for an academic paper with the following details:

Main Findings: {findings}
Data Analysis: {data_analysis}
Statistical Significance: {statistical_significance}
Figures/Tables: {figures_tables}

The results section should:
1. Present findings objectively without interpretation
2. Include statistical analysis results
3. Reference figures and tables appropriately
4. Be organized logically
5. Use appropriate statistical reporting
6. Be written in LaTeX format with \\section{{Results}}
7. Include subsections if needed

Please ensure results are presented clearly and objectively."""
        
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt
                    }
                }
            ]
        }
    
    def _write_discussion_prompt(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generate discussion writing prompt."""
        results_summary = args.get("results_summary", "")
        implications = args.get("implications", "")
        limitations = args.get("limitations", "")
        future_work = args.get("future_work", "")
        
        prompt = f"""Please write a discussion section for an academic paper with the following details:

Results Summary: {results_summary}
Implications: {implications}
Limitations: {limitations}
Future Work: {future_work}

The discussion section should:
1. Interpret and explain the results
2. Compare findings with existing literature
3. Discuss implications and significance
4. Address limitations honestly
5. Suggest future research directions
6. Be written in LaTeX format with \\section{{Discussion}}
7. Include appropriate citations

Please ensure the discussion provides meaningful interpretation of results."""
        
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt
                    }
                }
            ]
        }
    
    def _write_conclusion_prompt(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generate conclusion writing prompt."""
        main_contributions = args.get("main_contributions", "")
        research_question = args.get("research_question", "")
        broader_impact = args.get("broader_impact", "")
        
        prompt = f"""Please write a conclusion section for an academic paper with the following details:

Main Contributions: {main_contributions}
Research Question Answered: {research_question}
Broader Impact: {broader_impact}

The conclusion should:
1. Summarize the main contributions
2. Restate how the research question was answered
3. Highlight the broader impact and significance
4. Avoid introducing new information
5. End with a strong closing statement
6. Be written in LaTeX format with \\section{{Conclusion}}
7. Be concise but comprehensive

Please ensure the conclusion effectively wraps up the paper."""
        
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt
                    }
                }
            ]
        }
    
    def _improve_writing_prompt(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generate writing improvement prompt."""
        text = args.get("text", "")
        improvement_focus = args.get("improvement_focus", "general improvement")
        target_audience = args.get("target_audience", "academic")
        
        prompt = f"""Please improve the following academic text with focus on {improvement_focus} for a {target_audience} audience:

Original Text:
{text}

Please:
1. Improve clarity and readability
2. Enhance academic style and tone
3. Fix any grammatical issues
4. Improve sentence structure and flow
5. Maintain the original meaning
6. Keep the LaTeX formatting intact
7. Focus specifically on: {improvement_focus}

Provide the improved version along with a brief explanation of the changes made."""
        
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt
                    }
                }
            ]
        }
    
    def _create_outline_prompt(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generate outline creation prompt."""
        topic = args.get("topic", "")
        paper_type = args.get("paper_type", "")
        length = args.get("length", "")
        requirements = args.get("requirements", "")
        
        prompt = f"""Please create a detailed outline for a {paper_type} on the topic: {topic}

Additional Details:
Length: {length}
Requirements: {requirements}

The outline should:
1. Include all major sections and subsections
2. Provide brief descriptions for each section
3. Suggest appropriate content for each part
4. Follow academic paper structure
5. Be suitable for the specified paper type
6. Consider the target length
7. Include LaTeX section commands

Please provide a comprehensive outline that can guide the writing process."""
        
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt
                    }
                }
            ]
        }
    
    def _format_citations_prompt(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generate citation formatting prompt."""
        citation_style = args.get("citation_style", "")
        sources = args.get("sources", "")
        context = args.get("context", "")
        
        prompt = f"""Please help format citations in {citation_style} style for the following sources:

Sources:
{sources}

Context: {context}

Please provide:
1. Properly formatted in-text citations
2. Complete bibliography entries
3. LaTeX commands for the citations
4. Explanation of the citation format
5. Examples of how to use them in text

Ensure all citations follow {citation_style} guidelines exactly."""
        
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt
                    }
                }
            ]
        }
    
    def _latex_help_prompt(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generate LaTeX help prompt."""
        task = args.get("task", "")
        document_class = args.get("document_class", "")
        packages = args.get("packages", "")
        
        prompt = f"""Please help with the following LaTeX task: {task}

Document Class: {document_class}
Loaded Packages: {packages}

Please provide:
1. Complete LaTeX code solution
2. Explanation of the commands used
3. Any additional packages needed
4. Best practices and tips
5. Alternative approaches if applicable

Ensure the solution is compatible with the specified document class and packages."""
        
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt
                    }
                }
            ]
        }
    
    def _research_proposal_prompt(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generate research proposal prompt."""
        research_area = args.get("research_area", "")
        problem_statement = args.get("problem_statement", "")
        objectives = args.get("objectives", "")
        methodology = args.get("methodology", "")
        timeline = args.get("timeline", "")
        
        prompt = f"""Please write a research proposal with the following details:

Research Area: {research_area}
Problem Statement: {problem_statement}
Objectives: {objectives}
Methodology: {methodology}
Timeline: {timeline}

The proposal should include:
1. Title and abstract
2. Problem statement and significance
3. Literature review outline
4. Research objectives and questions
5. Methodology and approach
6. Timeline and milestones
7. Expected outcomes
8. References section
9. LaTeX formatting throughout

Please ensure the proposal is compelling and well-structured."""
        
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt
                    }
                }
            ]
        }

