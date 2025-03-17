# Contributors guide

## Prerequisites

- Python 3.8 or higher
- Ollama installed (for local model execution)
- Basic familiarity with Python and AI models

## Contribution Guidelines

We welcome contributions in the following areas:

- Code Improvements: Optimize existing code, fix bugs, or add new features.
- Documentation: Improve the README, write tutorials, or add inline comments.
- Testing: Write unit tests, integration tests, or help with debugging.
- New Features: Implement new tools, agents, or integrations.

## Steps to Contribute

Fork the project to your GitHub account.

Create a Branch:

```bash
git checkout -b feature/your-feature-name
```

Make Your Changes.

Write your code, add documentation, or fix bugs.

Test Your Changes.

Ensure your changes work as expected and do not break existing functionality.

Push your changes to your fork and submit a pull request to the main branch of this repository. Provide a clear description of your changes and reference any related issues.

## Coding Philosophy

1. **Privacy First, Always Local**
   - All core functionality must be able to run 100% locally
   - Cloud services should only be optional alternatives, clearly defined with a warning message.
   - User data privacy is non-negotiable

2. **Agent-Based Architecture**
   - Each agent should have a clear, single responsibility
   - Agents should be modular and independently testable
   - New agents should solve specific use cases

3. **Tool-Based Extensibility**
   - Tools should be self-contained and follow the Tools base class
   - Each tool should do one thing well
   - Tools should provide clear feedback on success/failure

4. **User Experience**
   - Provide meaningful feedback for all operations
   - Support multiple languages (chinese, french, english for now)
   - Text to speech with short response.
   - Keep responses concise

5. **Code Quality**
   - Write clear, self-documenting code
   - Include type hints and docstrings
   - Follow existing patterns in the codebase
   - Add a if __name__ == "__main__" at the bottom of each class file for individual testing.
   - Ideally had automated tests.

6. **Error Handling**
   - Fail gracefully with meaningful messages
   - Include recovery mechanisms where possible
   - Log errors appropriately without exposing sensitive data

## Areas Needing Help

Here are some high-priority tasks and areas where we need contributions:

- Web Browsing: Improve the autonomous web browsing capabilities for the assistant.
- Graphical interface, a web graphical interface. (please ask first)
- Multi-Agent System: Enhance the planner agent for divide and conqueer for task (please ask first).
- New Tools: Add support for additional programming languages or APIs.
- Multi-language support for Text to speech & speech to text (english, chinese, spanish first)
- Testing: Write comprehensive tests for existing features.
- Better readme image: make a better readme image (robot whale that use tools. Ghibli or anime style, inspiration could be https://sakana.ai/assets/ai-scientist/cover.jpeg)


If you're unsure where to start, feel free to reach out by opening an issue or joining our community discussions.

## Code of Conduct

See CODE_OF_CONDUCT.md

**Thank You!**
