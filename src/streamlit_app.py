"""
Streamlit interface for the CrewAI Notion Chatbot
"""
import streamlit as st
import os
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent))

from crews import NotionChatbot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="CrewAI Notion Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 10px;
        border-left: 4px solid #2E86AB;
        background-color: #f8f9fa;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #1976d2;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left-color: #7b1fa2;
    }
    .status-box {
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .status-success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .status-error {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    .status-warning {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = NotionChatbot()
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'mcp_status' not in st.session_state:
    st.session_state.mcp_status = None

# Header
st.markdown('<div class="main-header">🤖 CrewAI Notion Chatbot</div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("🔧 Configuration")
    
    # Environment status
    st.subheader("Environment Status")
    
    # Check required environment variables
    required_vars = {
        "OPENAI_API_KEY": "OpenAI API Key",
        "NOTION_TOKEN": "Notion Integration Token",
        "MCP_CREWAI_ENTERPRISE_BEARER_TOKEN": "MCP Bearer Token"
    }
    
    env_status = {}
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value and value != f"your_{var.lower()}_here":
            env_status[var] = "✅ Configured"
        else:
            env_status[var] = "❌ Missing"
    
    for var, status in env_status.items():
        st.write(f"**{required_vars[var]}**: {status}")
    
    # MCP Status
    st.subheader("MCP Connection Status")
    if st.button("Check MCP Status"):
        st.session_state.mcp_status = st.session_state.chatbot.get_mcp_status()
    
    if st.session_state.mcp_status:
        if st.session_state.mcp_status['connected']:
            st.success("✅ MCP Connected")
            crews = st.session_state.mcp_status.get('available_crews', [])
            if crews:
                st.write("**Available Crews:**")
                for crew in crews:
                    st.write(f"- {crew.get('name', 'Unknown')}")
        else:
            st.error(f"❌ MCP Disconnected: {st.session_state.mcp_status.get('error', 'Unknown error')}")
    
    # Settings
    st.subheader("Settings")
    use_mcp = st.checkbox("Use MCP (if available)", value=False)
    
    # Clear conversation
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.chatbot.clear_conversation_history()
        st.rerun()

# Main chat interface
st.header("💬 Chat Interface")

# Display conversation history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message assistant-message"><strong>Assistant:</strong> {message["content"]}</div>', unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask a question about your Notion workspace..."):
    # Add user message to conversation
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {prompt}</div>', unsafe_allow_html=True)
    
    # Get response from chatbot
    with st.spinner("🤔 Thinking..."):
        try:
            response = st.session_state.chatbot.answer_question(prompt, use_mcp=use_mcp)
            
            if response['success']:
                answer = response['answer']
                source = response['source']
                
                # Add assistant response to conversation
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
                # Display assistant response
                st.markdown(f'<div class="chat-message assistant-message"><strong>Assistant:</strong> {answer}</div>', unsafe_allow_html=True)
                
                # Show source information
                if source == "mcp_crew":
                    st.markdown(f'<div class="status-box status-success">✅ Response from MCP Crew (ID: {response.get("execution_id", "unknown")})</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="status-box status-warning">⚠️ Response from Local Crew (MCP unavailable)</div>', unsafe_allow_html=True)
                
            else:
                error_msg = response.get('error', 'Unknown error')
                st.error(f"❌ Error: {error_msg}")
                
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
    
    # Rerun to update the display
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>CrewAI Notion Chatbot - Powered by CrewAI, MCP, and Notion API</p>
    <p>Make sure to configure your environment variables in the .env file</p>
</div>
""", unsafe_allow_html=True)

# Instructions expandable section
with st.expander("📋 Setup Instructions"):
    st.markdown("""
    ### Environment Setup
    
    1. **Copy the example environment file:**
       ```bash
       cp .env.example .env
       ```
    
    2. **Configure your API keys in the .env file:**
       - `OPENAI_API_KEY`: Your OpenAI API key
       - `NOTION_TOKEN`: Your Notion integration token
       - `NOTION_DATABASE_ID`: (Optional) Specific database ID to query
       - `MCP_CREWAI_ENTERPRISE_BEARER_TOKEN`: Your CrewAI Enterprise token
    
    ### Notion Integration Setup
    
    1. **Create a Notion Integration:**
       - Go to https://www.notion.so/my-integrations
       - Click "New integration"
       - Give it a name and select your workspace
       - Copy the "Internal Integration Token"
    
    2. **Share pages with your integration:**
       - Open the Notion pages you want to query
       - Click "Share" → "Invite" → Select your integration
    
    ### MCP Setup (Optional)
    
    1. **CrewAI Enterprise Account:**
       - Sign up at https://app.crewai.com
       - Deploy your crews to the platform
       - Get your bearer token from the dashboard
    
    2. **Local Development:**
       - The app will use local CrewAI crews if MCP is not configured
       - This allows you to test without CrewAI Enterprise
    """)

# Debug information (only show if in development)
if st.checkbox("Show Debug Information"):
    st.subheader("Debug Information")
    st.write("**Environment Variables:**")
    for var in required_vars.keys():
        value = os.getenv(var, "Not set")
        # Don't show the actual values for security
        if value and value != "Not set":
            st.write(f"- {var}: {'*' * 10} (configured)")
        else:
            st.write(f"- {var}: Not configured")
    
    st.write("**Conversation History:**")
    history = st.session_state.chatbot.get_conversation_history()
    st.json(history)
