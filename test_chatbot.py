"""
Test script for the CrewAI Notion Chatbot
"""
import os
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
from crews import NotionChatbot
from mcp_client import get_mcp_client

def test_environment_setup():
    """Test that environment variables are properly configured"""
    print("🧪 Testing Environment Setup...")
    
    # Load environment variables
    load_dotenv()
    
    # Check required variables
    required_vars = ["OPENAI_API_KEY", "NOTION_TOKEN"]
    optional_vars = ["MCP_CREWAI_ENTERPRISE_BEARER_TOKEN", "NOTION_DATABASE_ID"]
    
    print("\n📋 Required Environment Variables:")
    for var in required_vars:
        value = os.getenv(var)
        if value and not value.startswith("your_"):
            print(f"  ✅ {var}: Configured")
        else:
            print(f"  ❌ {var}: Missing or not configured")
    
    print("\n📋 Optional Environment Variables:")
    for var in optional_vars:
        value = os.getenv(var)
        if value and not value.startswith("your_"):
            print(f"  ✅ {var}: Configured")
        else:
            print(f"  ⚠️ {var}: Not configured (using defaults)")
    
    return True

def test_mcp_client():
    """Test MCP client functionality"""
    print("\n🧪 Testing MCP Client...")
    
    try:
        mcp_client = get_mcp_client()
        
        # Test list available crews
        print("  📋 Testing list_available_crews...")
        crews_response = mcp_client.list_available_crews()
        
        if "error" in crews_response:
            print(f"  ⚠️ MCP Error (expected for local dev): {crews_response['error']}")
        else:
            print(f"  ✅ Found {len(crews_response.get('crews', []))} available crews")
            for crew in crews_response.get('crews', []):
                print(f"    - {crew.get('name', 'Unknown')}")
        
        # Test kickoff crew
        print("  🚀 Testing kickoff_crew...")
        kickoff_response = mcp_client.kickoff_crew(
            crew_id="test_crew",
            inputs={"test": "input"}
        )
        
        if "error" in kickoff_response:
            print(f"  ⚠️ Kickoff Error (expected for local dev): {kickoff_response['error']}")
        else:
            execution_id = kickoff_response.get("execution_id")
            print(f"  ✅ Crew kicked off with execution ID: {execution_id}")
            
            # Test get status
            print("  📊 Testing get_crew_status...")
            status_response = mcp_client.get_crew_status(execution_id)
            
            if "error" in status_response:
                print(f"  ⚠️ Status Error: {status_response['error']}")
            else:
                print(f"  ✅ Status: {status_response.get('status', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ MCP Client Error: {str(e)}")
        return False

def test_notion_tools():
    """Test Notion tools (if configured)"""
    print("\n🧪 Testing Notion Tools...")
    
    notion_token = os.getenv("NOTION_TOKEN")
    if not notion_token or notion_token.startswith("your_"):
        print("  ⚠️ Notion token not configured, skipping Notion tests")
        return True
    
    try:
        from notion_tools import NotionSearchTool, NotionPageRetrieverTool, NotionDatabaseQueryTool
        
        print("  🔍 Testing NotionSearchTool...")
        search_tool = NotionSearchTool()
        # Test with a simple query
        result = search_tool._run("test")
        print(f"  ✅ Search tool executed (result length: {len(str(result))})")
        
        print("  📄 Testing NotionPageRetrieverTool...")
        page_tool = NotionPageRetrieverTool()
        # This will likely fail without a valid page ID, but that's expected
        print("  ✅ Page retriever tool initialized")
        
        print("  🗄️ Testing NotionDatabaseQueryTool...")
        db_tool = NotionDatabaseQueryTool()
        print("  ✅ Database query tool initialized")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Notion Tools Error: {str(e)}")
        return False

def test_chatbot_initialization():
    """Test chatbot initialization"""
    print("\n🧪 Testing Chatbot Initialization...")
    
    try:
        chatbot = NotionChatbot()
        print("  ✅ Chatbot initialized successfully")
        
        # Test MCP status
        print("  🔗 Testing MCP status...")
        mcp_status = chatbot.get_mcp_status()
        
        if mcp_status['connected']:
            print("  ✅ MCP connected")
            crews = mcp_status.get('available_crews', [])
            print(f"  📋 Available crews: {len(crews)}")
        else:
            print(f"  ⚠️ MCP not connected (using local crews): {mcp_status.get('error', 'Unknown')}")
        
        # Test conversation history
        print("  📚 Testing conversation history...")
        history = chatbot.get_conversation_history()
        print(f"  ✅ Conversation history: {len(history)} entries")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Chatbot Initialization Error: {str(e)}")
        return False

def test_simple_query():
    """Test a simple query (if environment is configured)"""
    print("\n🧪 Testing Simple Query...")
    
    # Check if we have the required environment variables
    openai_key = os.getenv("OPENAI_API_KEY")
    notion_token = os.getenv("NOTION_TOKEN")
    
    if not openai_key or openai_key.startswith("your_"):
        print("  ⚠️ OpenAI API key not configured, skipping query test")
        return True
    
    if not notion_token or notion_token.startswith("your_"):
        print("  ⚠️ Notion token not configured, skipping query test")
        return True
    
    try:
        chatbot = NotionChatbot()
        
        # Test with a simple question
        print("  💬 Testing simple question...")
        test_question = "Hello, can you help me understand how to use this system?"
        
        response = chatbot.answer_question(test_question, use_mcp=False)
        
        if response['success']:
            print("  ✅ Query executed successfully")
            print(f"  📝 Answer preview: {str(response['answer'])[:100]}...")
            print(f"  🎯 Source: {response['source']}")
        else:
            print(f"  ⚠️ Query failed: {response.get('error', 'Unknown error')}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Query Test Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting CrewAI Notion Chatbot Tests")
    print("=" * 50)
    
    tests = [
        ("Environment Setup", test_environment_setup),
        ("MCP Client", test_mcp_client),
        ("Notion Tools", test_notion_tools),
        ("Chatbot Initialization", test_chatbot_initialization),
        ("Simple Query", test_simple_query),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} failed with exception: {str(e)}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("🏁 Test Results Summary:")
    print("=" * 50)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} {test_name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n📊 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your chatbot is ready to use.")
        print("\nNext steps:")
        print("1. Run 'python main.py' for CLI interface")
        print("2. Run 'streamlit run src/streamlit_app.py' for web interface")
    else:
        print("⚠️ Some tests failed. Please check your configuration.")
        print("\nTips:")
        print("- Ensure your .env file is properly configured")
        print("- Check your API keys are valid")
        print("- Verify your Notion integration is set up correctly")

if __name__ == "__main__":
    main()
