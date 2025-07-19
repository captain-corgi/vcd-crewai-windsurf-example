# CrewAI Notion Chatbot

A sophisticated chatbot powered by CrewAI that can answer questions about your Notion workspace using MCP (Model Context Protocol) integration.

## Features

- 🤖 **CrewAI Integration**: Uses multiple specialized AI agents working together
- 📚 **Notion Connectivity**: Direct integration with Notion API for real-time data access
- 🔗 **MCP Support**: Compatible with CrewAI Enterprise MCP server for production deployments
- 🎯 **Intelligent Agents**: Specialized agents for research, Q&A, and conversation management
- 💬 **Multiple Interfaces**: Both CLI and Streamlit web interface
- 🧠 **Memory**: Maintains conversation context and history
- 🔄 **Fallback System**: Automatically falls back to local crews if MCP is unavailable

## Architecture

The chatbot uses a multi-agent system with the following components:

### Agents

1. **Notion Researcher**: Searches and retrieves information from Notion
2. **Q&A Specialist**: Synthesizes information into comprehensive answers
3. **Conversation Manager**: Manages conversation flow and context
4. **MCP Coordinator**: Handles CrewAI Enterprise deployments

### Tools

- **NotionSearchTool**: Search across Notion workspace
- **NotionPageRetrieverTool**: Retrieve specific page content
- **NotionDatabaseQueryTool**: Query Notion databases

### Integration

- **Local CrewAI**: Runs crews locally for development and testing
- **MCP Integration**: Connects to CrewAI Enterprise for production deployments
- **Fallback System**: Seamlessly switches between MCP and local execution

## Prerequisites

- Python 3.10 or higher (but less than 3.14)
- OpenAI API key
- Notion integration token
- (Optional) CrewAI Enterprise account for MCP features

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd vcd-crewai-windsurf-example
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:

   ```bash
   cp .env.example .env
   ```

4. **Configure your `.env` file**:

   ```env
   # Required
   OPENAI_API_KEY=your_openai_api_key_here
   NOTION_TOKEN=your_notion_integration_token_here
   
   # Optional (for MCP integration)
   MCP_CREWAI_ENTERPRISE_SERVER_URL=https://app.crewai.com
   MCP_CREWAI_ENTERPRISE_BEARER_TOKEN=your_bearer_token_here
   
   # Optional (for specific database queries)
   NOTION_DATABASE_ID=your_notion_database_id_here
   ```

## Notion Setup

### 1. Create a Notion Integration

1. Go to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click "New integration"
3. Give it a name (e.g., "CrewAI Chatbot")
4. Select your workspace
5. Copy the "Internal Integration Token"

### 2. Share Pages with Your Integration

1. Open the Notion pages you want the chatbot to access
2. Click "Share" in the top-right corner
3. Click "Invite" and select your integration
4. Grant appropriate permissions

### 3. (Optional) Get Database IDs

If you want to query specific databases:

1. Open the database in Notion
2. Copy the URL - the database ID is the long string after the last `/`
3. Add it to your `.env` file as `NOTION_DATABASE_ID`

## Usage

### CLI Interface

Run the chatbot in command-line mode:

```bash
python main.py
```

Example interaction:

```
You: What projects are currently in progress?
🤔 Thinking...
🤖 Assistant: Based on your Notion workspace, here are the current projects...
```

### Streamlit Web Interface

Launch the web interface:

```bash
streamlit run src/streamlit_app.py
```

Then open your browser to `http://localhost:8501`

The web interface provides:

- Interactive chat interface
- Environment status monitoring
- MCP connection status
- Conversation history management
- Debug information

### Example Questions

Try asking questions like:

- "What are my current tasks?"
- "Show me information about the project roadmap"
- "What meetings do I have scheduled?"
- "Find pages about the marketing campaign"
- "What's in my personal notes database?"

## MCP Integration (Optional)

### CrewAI Enterprise Setup

1. **Sign up for CrewAI Enterprise**:
   - Visit [https://app.crewai.com](https://app.crewai.com)
   - Create an account and get your bearer token

2. **Deploy your crews**:
   - Upload your crew configurations to the platform
   - Note the crew IDs for your deployments

3. **Configure MCP**:
   - Set `MCP_CREWAI_ENTERPRISE_BEARER_TOKEN` in your `.env`
   - The chatbot will automatically use MCP when available

### Local Development

When MCP is not configured or unavailable:

- The chatbot automatically falls back to local CrewAI execution
- All functionality remains available
- Performance may be slower but no external dependencies required

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key |
| `NOTION_TOKEN` | Yes | Notion integration token |
| `MCP_CREWAI_ENTERPRISE_SERVER_URL` | No | MCP server URL (default: <https://app.crewai.com>) |
| `MCP_CREWAI_ENTERPRISE_BEARER_TOKEN` | No | CrewAI Enterprise bearer token |
| `NOTION_DATABASE_ID` | No | Specific database ID to query |
| `CREWAI_TELEMETRY_OPT_OUT` | No | Set to `true` to disable telemetry |

### Crew Configuration

The chatbot uses these crew configurations:

- **Sequential Process**: Agents work in sequence for thorough analysis
- **Memory Enabled**: Maintains context across conversations
- **Embedding Model**: Uses OpenAI text-embedding-3-small for memory

## File Structure

```
vcd-crewai-windsurf-example/
├── src/
│   ├── __init__.py
│   ├── agents.py              # CrewAI agent definitions
│   ├── crews.py               # Crew configurations and main chatbot class
│   ├── mcp_client.py          # MCP client and simulator
│   ├── notion_tools.py        # Notion API integration tools
│   └── streamlit_app.py       # Streamlit web interface
├── docs/
│   └── init_prompt.md         # Project initialization prompt
├── main.py                    # CLI entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variable template
└── README.md                 # This file
```

## Troubleshooting

### Common Issues

1. **"Missing required environment variables"**
   - Ensure `.env` file is created and configured
   - Check that API keys are valid and not placeholder values

2. **"Error searching Notion"**
   - Verify your Notion integration token is correct
   - Ensure pages are shared with your integration
   - Check your internet connection

3. **"MCP Disconnected"**
   - This is normal if you haven't configured CrewAI Enterprise
   - The chatbot will use local crews automatically
   - For MCP features, ensure your bearer token is valid

4. **"Error executing local crew"**
   - Check your OpenAI API key is valid and has credits
   - Ensure all dependencies are installed correctly
   - Try restarting the application

### Debug Mode

Enable debug information in the Streamlit interface:

1. Check "Show Debug Information" at the bottom of the page
2. Review environment variables and conversation history
3. Check the console for detailed error messages

## Development

### Adding New Tools

1. Create a new tool class in `src/notion_tools.py`
2. Inherit from `BaseTool`
3. Implement the `_run` method
4. Add to the appropriate agent in `src/agents.py`

### Customizing Agents

1. Modify agent configurations in `src/agents.py`
2. Adjust roles, goals, and backstories
3. Add or remove tools as needed
4. Update crew configurations in `src/crews.py`

### Testing

Run the test script to validate functionality:

```bash
python test_chatbot.py
```

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:

- Check the troubleshooting section
- Review the CrewAI documentation
- Check Notion API documentation
- Open an issue on GitHub

## Acknowledgments

- [CrewAI](https://github.com/crewAIInc/crewAI) - Multi-agent framework
- [Notion API](https://developers.notion.com/) - Notion integration
- [Streamlit](https://streamlit.io/) - Web interface
- [OpenAI](https://openai.com/) - Language models
