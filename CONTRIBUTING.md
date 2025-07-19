# Contributing to CrewAI Notion Chatbot

Thank you for your interest in contributing to the CrewAI Notion Chatbot! This document provides guidelines and information for contributors.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Git Flow Guidelines](#git-flow-guidelines)
5. [Coding Standards](#coding-standards)
6. [Testing](#testing)
7. [Documentation](#documentation)
8. [Pull Request Process](#pull-request-process)
9. [Issue Reporting](#issue-reporting)
10. [Community](#community)

## Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow:

- **Be respectful**: Treat everyone with respect and kindness
- **Be inclusive**: Welcome newcomers and help them contribute
- **Be collaborative**: Work together constructively
- **Be patient**: Help others learn and grow
- **Be professional**: Maintain a professional demeanor in all interactions

## Getting Started

### Prerequisites

- Python 3.10-3.13
- Git with Git Flow installed
- OpenAI API key
- Notion integration token
- Basic understanding of CrewAI framework

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/vcd-crewai-windsurf-example.git
   cd vcd-crewai-windsurf-example
   ```

2. **Set up Development Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Validate Setup**
   ```bash
   python test_chatbot.py
   ```

## Development Workflow

### Git Flow Process

This project uses Git Flow for branch management:

```bash
# Initialize git flow (first time only)
git flow init -d

# Start a new feature
git flow feature start feature-name

# Work on your feature
git add .
git commit -m "feat: add new feature description"

# Finish feature (merges to develop)
git flow feature finish feature-name

# Start a release
git flow release start v1.0.0

# Finish release (merges to master and develop)
git flow release finish v1.0.0
```

### Branch Structure

- **master/main**: Production-ready code
- **develop**: Integration branch for features
- **feature/**: Feature development branches
- **release/**: Release preparation branches
- **hotfix/**: Critical bug fixes

## Git Flow Guidelines

### Commit Message Convention

Follow conventional commits format:

```
<type>(<scope>): <description>

<body>

<footer>
```

#### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

#### Examples
```bash
feat(agents): add new conversation manager agent
fix(mcp): resolve connection timeout issue
docs(readme): update installation instructions
test(notion): add integration tests for notion tools
```

### Feature Development

1. **Start Feature Branch**
   ```bash
   git flow feature start your-feature-name
   ```

2. **Develop Your Feature**
   - Write code following coding standards
   - Add tests for new functionality
   - Update documentation as needed
   - Test thoroughly

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat(scope): descriptive commit message"
   ```

4. **Finish Feature**
   ```bash
   git flow feature finish your-feature-name
   ```

### Release Process

1. **Start Release Branch**
   ```bash
   git flow release start v1.0.0
   ```

2. **Prepare Release**
   - Update version numbers
   - Update CHANGELOG.md
   - Final testing
   - Documentation updates

3. **Finish Release**
   ```bash
   git flow release finish v1.0.0
   ```

## Coding Standards

### Python Code Style

- Follow PEP 8 style guide
- Use type hints for all functions
- Maximum line length: 88 characters (Black formatter)
- Use meaningful variable and function names

### Code Quality Tools

```bash
# Format code
black src/
isort src/

# Lint code
flake8 src/
pylint src/

# Type checking
mypy src/
```

### Example Code Structure

```python
from typing import Optional, Dict, Any
from crewai import Agent
from crewai_tools import BaseTool


class ExampleTool(BaseTool):
    """Example tool following project conventions."""
    
    name: str = "Example Tool"
    description: str = "Detailed description of what this tool does"
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the tool with optional configuration."""
        super().__init__()
        self.config = config or {}
    
    def _run(self, query: str) -> str:
        """Execute the tool with the given query.
        
        Args:
            query: The input query string
            
        Returns:
            The processed result as a string
            
        Raises:
            ValueError: If query is invalid
        """
        if not query.strip():
            raise ValueError("Query cannot be empty")
        
        # Implementation here
        return f"Processed: {query}"
```

## Testing

### Test Structure

```
tests/
├── unit/
│   ├── test_agents.py
│   ├── test_tools.py
│   └── test_crews.py
├── integration/
│   ├── test_mcp_integration.py
│   └── test_notion_integration.py
└── fixtures/
    └── test_data.py
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_agents.py

# Run with coverage
pytest --cov=src tests/

# Run integration tests (requires API keys)
pytest tests/integration/ --integration
```

### Writing Tests

```python
import pytest
from unittest.mock import Mock, patch
from src.agents import get_notion_researcher


class TestNotionResearcher:
    """Test cases for Notion Researcher agent."""
    
    def test_agent_initialization(self):
        """Test that agent initializes correctly."""
        agent = get_notion_researcher()
        assert agent.role == "Notion Researcher"
        assert agent.goal
        assert agent.backstory
    
    @patch('src.notion_tools.NotionSearchTool')
    def test_agent_with_mocked_tools(self, mock_tool):
        """Test agent behavior with mocked tools."""
        mock_tool.return_value._run.return_value = "mocked result"
        agent = get_notion_researcher()
        # Test agent behavior
```

## Documentation

### Documentation Requirements

All contributions should include appropriate documentation:

- **Code Documentation**: Docstrings for all classes and functions
- **API Documentation**: Update API docs for new endpoints
- **User Documentation**: Update user guide for new features
- **Architecture Documentation**: Update technical docs for system changes

### Documentation Style

```python
def example_function(param1: str, param2: Optional[int] = None) -> str:
    """Brief description of the function.
    
    Longer description if needed, explaining the purpose,
    behavior, and any important details.
    
    Args:
        param1: Description of first parameter
        param2: Description of optional second parameter
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is invalid
        TypeError: When param2 is wrong type
        
    Example:
        >>> result = example_function("test", 42)
        >>> print(result)
        'processed: test-42'
    """
```

## Pull Request Process

### Before Submitting

1. **Test Your Changes**
   ```bash
   python test_chatbot.py
   pytest
   ```

2. **Code Quality Checks**
   ```bash
   black --check src/
   flake8 src/
   mypy src/
   ```

3. **Update Documentation**
   - Update relevant documentation
   - Add docstrings for new code
   - Update user guide if needed

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Documentation
- [ ] Code is documented
- [ ] User documentation updated
- [ ] API documentation updated

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Tests added for new functionality
- [ ] All tests pass
```

### Review Process

1. **Automated Checks**: All CI checks must pass
2. **Code Review**: At least one maintainer review required
3. **Testing**: Comprehensive testing verification
4. **Documentation**: Documentation completeness check

## Issue Reporting

### Bug Reports

Use the bug report template:

```markdown
**Bug Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected Behavior**
What you expected to happen

**Environment**
- OS: [e.g. Windows 11]
- Python version: [e.g. 3.11]
- Project version: [e.g. 1.0.0]

**Additional Context**
Any other context about the problem
```

### Feature Requests

Use the feature request template:

```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Describe the use case for this feature

**Proposed Solution**
Describe your proposed solution

**Alternatives Considered**
Alternative solutions you've considered

**Additional Context**
Any other context or screenshots
```

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General discussions and questions
- **Code Reviews**: Technical discussions on pull requests

### Getting Help

- Check existing documentation
- Search existing issues
- Create a new issue with detailed information
- Join community discussions

### Recognition

Contributors are recognized through:
- GitHub contributor statistics
- Changelog acknowledgments
- Community highlights

## Development Best Practices

### Code Organization

- Keep functions small and focused
- Use clear, descriptive names
- Separate concerns appropriately
- Follow SOLID principles

### Error Handling

```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def safe_operation(data: str) -> Optional[str]:
    """Perform operation with proper error handling."""
    try:
        result = process_data(data)
        logger.info(f"Operation successful: {result}")
        return result
    except ValueError as e:
        logger.error(f"Invalid data provided: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
```

### Performance Considerations

- Profile code for performance bottlenecks
- Use appropriate data structures
- Implement caching where beneficial
- Consider async operations for I/O

### Security Guidelines

- Never commit API keys or secrets
- Validate all user inputs
- Use environment variables for configuration
- Follow secure coding practices

## Release Notes

When contributing to releases, update the changelog:

```markdown
## [1.0.0] - 2025-01-19

### Added
- New conversation manager agent
- MCP integration for enterprise deployment
- Comprehensive documentation suite

### Changed
- Improved error handling in Notion tools
- Enhanced user interface design

### Fixed
- Connection timeout issues
- Memory leak in agent processing

### Security
- Enhanced API key management
- Improved data privacy controls
```

Thank you for contributing to the CrewAI Notion Chatbot! Your contributions help make this project better for everyone.
