"""
Main entry point for the CrewAI Notion Chatbot
"""
import os
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
from crews import NotionChatbot

def main():
    """Main function to run the chatbot"""
    # Load environment variables
    load_dotenv()
    
    # Check if required environment variables are set
    required_vars = ["OPENAI_API_KEY", "NOTION_TOKEN"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var) or os.getenv(var).startswith("your_"):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease configure these in your .env file (see .env.example)")
        return
    
    # Initialize chatbot
    print("🤖 Initializing CrewAI Notion Chatbot...")
    chatbot = NotionChatbot()
    
    # Check MCP status
    mcp_status = chatbot.get_mcp_status()
    if mcp_status['connected']:
        print("✅ MCP Connected")
        crews = mcp_status.get('available_crews', [])
        if crews:
            print("Available crews:")
            for crew in crews:
                print(f"  - {crew.get('name', 'Unknown')}")
    else:
        print(f"⚠️ MCP not available: {mcp_status.get('error', 'Unknown error')}")
        print("Using local CrewAI crews instead")
    
    print("\n" + "="*50)
    print("CrewAI Notion Chatbot is ready!")
    print("Type 'quit' or 'exit' to stop the chatbot")
    print("="*50 + "\n")
    
    # Chat loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("🤔 Thinking...")
            
            # Get response from chatbot
            response = chatbot.answer_question(user_input, use_mcp=mcp_status['connected'])
            
            if response['success']:
                print(f"\n🤖 Assistant: {response['answer']}")
                
                # Show source information
                source = response['source']
                if source == "mcp_crew":
                    print(f"✅ (Response from MCP Crew - ID: {response.get('execution_id', 'unknown')})")
                else:
                    print("⚠️ (Response from Local Crew - MCP unavailable)")
            else:
                print(f"❌ Error: {response.get('error', 'Unknown error')}")
            
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
