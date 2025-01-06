from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain_community.tools import WriteFileTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from typing import Any, Dict, Optional
import os
import time
from pathlib import Path

def create_search_tool() -> Tool:
    """Create a search tool using GoogleSerperAPIWrapper."""
    search = GoogleSerperAPIWrapper()
    
    return Tool(
        name="Search",
        description="Search the internet for information about companies, markets, and industries",
        func=lambda q: search.run(q),
        handle_tool_error=True
)

class ReportGenerator:
    def __init__(self):
        self.search_tool = create_search_tool()
        
        self.write_file_tool = Tool(
            name="Write File",
            description="Write content to a file. Input should be a dictionary with 'file_path' and 'text' keys.",
            func=self.write_file_tool_wrapper,
            handle_tool_error=True
        )

    def write_file_tool_wrapper(self, file_input: Any) -> Any:
        try:
            if isinstance(file_input, str):
                file_input = {"file_path": "report.md", "text": file_input}
            return WriteFileTool().run(file_input)
        except Exception as e:
            return {
                "error": f"File write failed: {str(e)}",
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }

    def enhanced_search(self, query: str) -> dict:
        """Enhanced search using search tool"""
        try:
            formatted_query = f"{query} analysis OR {query} insights 2024"
            search_results = self.search_tool.run(formatted_query)
            return {
                "query": formatted_query,
                "results": search_results,
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            return {
                "error": f"Search failed: {str(e)}",
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }

    def create_market_analysis_crew(self, inputs: Dict[str, Any]) -> Crew:
        analyst = Agent(
            role='Market Research Analyst',
            goal=f'Analyze {inputs["company_name"]} market position and trends',
            backstory="""Expert in market research and analysis. Skilled at identifying trends 
            and opportunities in various markets.""",
            tools=[self.search_tool],
            verbose=True,
            allow_delegation=False
        )

        writer = Agent(
            role='Business Report Writer',
            goal='Create comprehensive market analysis reports',
            backstory="""Professional business writer specializing in creating clear, 
            actionable market analysis reports.""",
            tools=[self.write_file_tool],
            verbose=True,
            allow_delegation=False
        )

        tasks = [
            Task(
                description=f"""Analyze market trends and position for {inputs["company_name"]}
                Focus on: {', '.join(inputs.get('focus_areas', []))}
                Industry: {inputs.get('industry', 'Not specified')}
                Time Period: {inputs.get('time_period', '2024')}""",
                expected_output="""A comprehensive market analysis containing:
                - Market size and growth trends
                - Industry analysis
                - Key market drivers
                - Competitive landscape
                - Market opportunities and challenges""",
                agent=analyst
            ),
            Task(
                description="Create a detailed market analysis report with findings",
                expected_output="""A well-structured markdown report containing:
                - Executive summary
                - Market overview
                - Detailed analysis
                - Key findings
                - Strategic recommendations""",
                agent=writer
            )
        ]

        return Crew(
            agents=[analyst, writer],
            tasks=tasks,
            verbose=True,
            process=Process.sequential
        )

    def generate_report(self, report_type: str, inputs: Dict[str, Any]) -> Any:
        crew = self.create_market_analysis_crew(inputs)
        return crew.kickoff()

def create_reports(result: Any, inputs: Dict[str, Any], report_type: str) -> tuple[str, str]:
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    base_name = f"{inputs['company_name']}_{report_type}_{timestamp}"
    
    validation_file = f"{base_name}_validation.txt"
    report_file = f"{base_name}_report.md"

    # Create reports directory if it doesn't exist
    reports_dir = Path('reports')
    reports_dir.mkdir(exist_ok=True)

    # Create validation report
    with open(reports_dir / validation_file, 'w') as f:
        f.write(f"Validation Report for {inputs['company_name']}\n")
        f.write(f"Report Type: {report_type}\n")
        f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(str(result))

    # Create main report
    with open(reports_dir / report_file, 'w') as f:
        f.write(f"# {report_type.replace('_', ' ').title()} Report\n\n")
        f.write(f"## Overview\n")
        f.write(f"Company: {inputs['company_name']}\n")
        f.write(str(result))

    return str(reports_dir / validation_file), str(reports_dir / report_file)

def get_report_generator() -> ReportGenerator:
    return ReportGenerator()