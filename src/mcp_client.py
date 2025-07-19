"""
MCP (Model Context Protocol) client for CrewAI Enterprise integration
"""
import os
import json
import requests
from typing import Dict, Any, Optional
from pydantic import BaseModel


class MCPClient:
    """Client for interacting with CrewAI Enterprise MCP Server"""
    
    def __init__(self):
        self.server_url = os.getenv("MCP_CREWAI_ENTERPRISE_SERVER_URL", "https://app.crewai.com")
        self.bearer_token = os.getenv("MCP_CREWAI_ENTERPRISE_BEARER_TOKEN")
        
        if not self.bearer_token:
            raise ValueError("MCP_CREWAI_ENTERPRISE_BEARER_TOKEN environment variable is required")
        
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json"
        }
    
    def kickoff_crew(self, crew_id: str, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Kickoff a CrewAI crew deployment
        
        Args:
            crew_id: The ID of the crew to kickoff
            inputs: Optional inputs for the crew
            
        Returns:
            Response from the MCP server
        """
        try:
            payload = {
                "crew_id": crew_id,
                "inputs": inputs or {}
            }
            
            response = requests.post(
                f"{self.server_url}/mcp/kickoff_crew",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"Failed to kickoff crew: {response.status_code}",
                    "details": response.text
                }
        except Exception as e:
            return {
                "error": f"Error kicking off crew: {str(e)}"
            }
    
    def get_crew_status(self, execution_id: str) -> Dict[str, Any]:
        """
        Get the status of a crew execution
        
        Args:
            execution_id: The ID of the crew execution
            
        Returns:
            Status information from the MCP server
        """
        try:
            response = requests.get(
                f"{self.server_url}/mcp/get_crew_status/{execution_id}",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"Failed to get crew status: {response.status_code}",
                    "details": response.text
                }
        except Exception as e:
            return {
                "error": f"Error getting crew status: {str(e)}"
            }
    
    def list_available_crews(self) -> Dict[str, Any]:
        """
        List available crews in the enterprise deployment
        
        Returns:
            List of available crews
        """
        try:
            response = requests.get(
                f"{self.server_url}/mcp/crews",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"Failed to list crews: {response.status_code}",
                    "details": response.text
                }
        except Exception as e:
            return {
                "error": f"Error listing crews: {str(e)}"
            }


class LocalMCPSimulator:
    """
    Simulator for MCP functionality when not using CrewAI Enterprise
    This allows local development and testing
    """
    
    def __init__(self):
        self.executions = {}
        self.crew_counter = 0
    
    def kickoff_crew(self, crew_id: str, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """Simulate crew kickoff"""
        self.crew_counter += 1
        execution_id = f"exec_{self.crew_counter}"
        
        self.executions[execution_id] = {
            "crew_id": crew_id,
            "inputs": inputs or {},
            "status": "running",
            "started_at": "2024-01-01T00:00:00Z",
            "result": None
        }
        
        return {
            "execution_id": execution_id,
            "status": "started",
            "message": f"Crew {crew_id} has been kicked off"
        }
    
    def get_crew_status(self, execution_id: str) -> Dict[str, Any]:
        """Simulate crew status check"""
        if execution_id not in self.executions:
            return {
                "error": f"Execution {execution_id} not found"
            }
        
        execution = self.executions[execution_id]
        
        # Simulate completion after first status check
        if execution["status"] == "running":
            execution["status"] = "completed"
            execution["result"] = "Task completed successfully (simulated)"
            execution["completed_at"] = "2024-01-01T00:01:00Z"
        
        return execution
    
    def list_available_crews(self) -> Dict[str, Any]:
        """Simulate crew listing"""
        return {
            "crews": [
                {
                    "id": "notion_qa_crew",
                    "name": "Notion Q&A Crew",
                    "description": "A crew specialized in answering questions about Notion content"
                },
                {
                    "id": "research_crew",
                    "name": "Research Crew",
                    "description": "A crew that can research and analyze information"
                }
            ]
        }


def get_mcp_client() -> MCPClient | LocalMCPSimulator:
    """
    Get the appropriate MCP client based on environment configuration
    """
    bearer_token = os.getenv("MCP_CREWAI_ENTERPRISE_BEARER_TOKEN")
    
    if bearer_token and bearer_token != "your_bearer_token_here":
        return MCPClient()
    else:
        print("Using local MCP simulator for development")
        return LocalMCPSimulator()
