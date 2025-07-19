"""
CrewAI crew configurations for the Notion-connected chatbot
"""
from crewai import Crew, Task, Process
from .agents import (
    create_notion_researcher_agent,
    create_qa_specialist_agent,
    create_conversation_manager_agent,
    create_mcp_coordinator_agent
)
from .mcp_client import get_mcp_client


def create_notion_qa_crew():
    """Create a crew specialized in answering questions about Notion content"""
    
    # Create agents
    researcher = create_notion_researcher_agent()
    qa_specialist = create_qa_specialist_agent()
    conversation_manager = create_conversation_manager_agent()
    
    return Crew(
        agents=[conversation_manager, researcher, qa_specialist],
        process=Process.sequential,
        verbose=True,
        memory=True,
        embedder={
            "provider": "openai",
            "config": {"model": "text-embedding-3-small"}
        }
    )


def create_research_task(user_question: str):
    """Create a research task for finding relevant Notion content"""
    return Task(
        description=f"""
        Research and find relevant information in the Notion workspace to answer this question: {user_question}
        
        Steps to follow:
        1. Search for relevant pages and databases in Notion using the search tool
        2. Retrieve detailed content from the most relevant pages
        3. Query relevant databases for specific information
        4. Organize and summarize the findings
        
        Focus on finding the most relevant and up-to-date information to answer the user's question.
        """,
        expected_output="A comprehensive summary of relevant information found in Notion, organized by source and relevance",
        agent=create_notion_researcher_agent()
    )


def create_answer_task(user_question: str):
    """Create a task for answering the user's question based on research"""
    return Task(
        description=f"""
        Based on the research findings from Notion, provide a comprehensive answer to this question: {user_question}
        
        Requirements:
        1. Use the information gathered from Notion to answer the question
        2. Provide a clear, well-structured response
        3. Include relevant details and context
        4. Cite sources (page titles, URLs) where appropriate
        5. If the information is incomplete, mention what additional information might be needed
        
        Make sure your answer is accurate, helpful, and directly addresses the user's question.
        """,
        expected_output="A comprehensive, well-structured answer to the user's question with proper citations",
        agent=create_qa_specialist_agent()
    )


def create_conversation_management_task(user_question: str):
    """Create a task for managing the conversation flow"""
    return Task(
        description=f"""
        Manage the conversation flow and ensure the user's question is properly understood and addressed: {user_question}
        
        Responsibilities:
        1. Understand the user's intent and question context
        2. Coordinate with other agents to gather and synthesize information
        3. Ensure the response is complete and addresses all aspects of the question
        4. Maintain conversation context for follow-up questions
        
        Make sure the overall response is coherent and meets the user's needs.
        """,
        expected_output="A well-managed conversation response that addresses the user's question comprehensively",
        agent=create_conversation_manager_agent()
    )


class NotionChatbot:
    """Main chatbot class that coordinates CrewAI and MCP integration"""
    
    def __init__(self):
        self.crew = create_notion_qa_crew()
        self.mcp_client = get_mcp_client()
        self.conversation_history = []
    
    def answer_question(self, user_question: str, use_mcp: bool = False):
        """Answer a user question using CrewAI crew and optionally MCP"""
        
        # Add to conversation history
        self.conversation_history.append({
            "type": "user_question",
            "content": user_question,
            "timestamp": "now"
        })
        
        if use_mcp:
            # Try to use MCP crew deployment if available
            return self._answer_with_mcp(user_question)
        else:
            # Use local crew
            return self._answer_with_local_crew(user_question)
    
    def _answer_with_local_crew(self, user_question: str):
        """Answer question using local CrewAI crew"""
        try:
            # Create tasks for this question
            tasks = [
                create_conversation_management_task(user_question),
                create_research_task(user_question),
                create_answer_task(user_question)
            ]
            
            # Update crew with tasks
            self.crew.tasks = tasks
            
            # Execute the crew
            result = self.crew.kickoff()
            
            # Add result to conversation history
            self.conversation_history.append({
                "type": "assistant_response",
                "content": str(result),
                "timestamp": "now"
            })
            
            return {
                "success": True,
                "answer": str(result),
                "source": "local_crew",
                "execution_id": None
            }
            
        except Exception as e:
            error_msg = f"Error executing local crew: {str(e)}"
            return {
                "success": False,
                "error": error_msg,
                "source": "local_crew"
            }
    
    def _answer_with_mcp(self, user_question: str):
        """Answer question using MCP crew deployment"""
        try:
            # Check available crews
            crews_response = self.mcp_client.list_available_crews()
            
            if "error" in crews_response:
                # Fall back to local crew
                return self._answer_with_local_crew(user_question)
            
            # Use the first available crew (or find notion_qa_crew)
            available_crews = crews_response.get("crews", [])
            crew_id = "notion_qa_crew"  # Default crew ID
            
            for crew in available_crews:
                if crew.get("id") == "notion_qa_crew":
                    crew_id = crew.get("id")
                    break
            
            # Kickoff the crew
            kickoff_response = self.mcp_client.kickoff_crew(
                crew_id=crew_id,
                inputs={"user_question": user_question}
            )
            
            if "error" in kickoff_response:
                # Fall back to local crew
                return self._answer_with_local_crew(user_question)
            
            execution_id = kickoff_response.get("execution_id")
            
            # Get crew status (in a real implementation, you might poll this)
            status_response = self.mcp_client.get_crew_status(execution_id)
            
            if "error" in status_response:
                return {
                    "success": False,
                    "error": status_response["error"],
                    "source": "mcp_crew"
                }
            
            # Add result to conversation history
            result = status_response.get("result", "No result available")
            self.conversation_history.append({
                "type": "assistant_response",
                "content": result,
                "timestamp": "now"
            })
            
            return {
                "success": True,
                "answer": result,
                "source": "mcp_crew",
                "execution_id": execution_id,
                "status": status_response.get("status", "unknown")
            }
            
        except Exception as e:
            error_msg = f"Error executing MCP crew: {str(e)}"
            # Fall back to local crew
            return self._answer_with_local_crew(user_question)
    
    def get_conversation_history(self):
        """Get the conversation history"""
        return self.conversation_history
    
    def clear_conversation_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
    
    def get_mcp_status(self):
        """Get MCP connection status"""
        try:
            crews_response = self.mcp_client.list_available_crews()
            if "error" in crews_response:
                return {
                    "connected": False,
                    "error": crews_response["error"]
                }
            else:
                return {
                    "connected": True,
                    "available_crews": crews_response.get("crews", [])
                }
        except Exception as e:
            return {
                "connected": False,
                "error": str(e)
            }
