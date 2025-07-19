"""
CrewAI agents for the Notion-connected chatbot
"""
import os
from crewai import Agent
from langchain_openai import ChatOpenAI
from .notion_tools import NotionSearchTool, NotionPageRetrieverTool, NotionDatabaseQueryTool


def get_llm():
    """Get the configured LLM"""
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )


def create_notion_researcher_agent():
    """Create an agent specialized in researching Notion content"""
    
    notion_tools = [
        NotionSearchTool(),
        NotionPageRetrieverTool(),
        NotionDatabaseQueryTool()
    ]
    
    return Agent(
        role="Notion Content Researcher",
        goal="Research and retrieve relevant information from Notion workspace to answer user questions",
        backstory="""You are an expert at navigating and extracting information from Notion workspaces. 
        You can search through pages, databases, and content to find the most relevant information 
        for answering user questions. You understand how to interpret Notion's structure and 
        present information in a clear, organized manner.""",
        tools=notion_tools,
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )


def create_qa_specialist_agent():
    """Create an agent specialized in answering questions based on retrieved information"""
    
    return Agent(
        role="Question Answering Specialist",
        goal="Provide comprehensive and accurate answers to user questions based on the information retrieved from Notion",
        backstory="""You are an expert at synthesizing information and providing clear, 
        comprehensive answers to user questions. You can take information from various sources 
        and present it in a coherent, well-structured response. You always cite your sources 
        and provide context for your answers.""",
        tools=[],
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=2
    )


def create_conversation_manager_agent():
    """Create an agent that manages the conversation flow"""
    
    return Agent(
        role="Conversation Manager",
        goal="Manage the conversation flow and ensure user queries are properly understood and addressed",
        backstory="""You are an expert at understanding user intent and managing conversational flow. 
        You can determine what type of information the user is looking for and coordinate with 
        other agents to provide the best possible response. You maintain context throughout 
        the conversation and can handle follow-up questions effectively.""",
        tools=[],
        llm=get_llm(),
        verbose=True,
        allow_delegation=True,
        max_iter=2
    )


def create_mcp_coordinator_agent():
    """Create an agent that coordinates with MCP services"""
    
    return Agent(
        role="MCP Coordinator",
        goal="Coordinate with MCP services and CrewAI Enterprise deployments when available",
        backstory="""You are an expert at working with Model Context Protocol (MCP) services 
        and CrewAI Enterprise deployments. You can kickoff crews, monitor their status, 
        and integrate their results into the conversation. You understand how to work with 
        both local and remote crew deployments.""",
        tools=[],
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=2
    )
