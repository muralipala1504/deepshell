
# DeepShell 🐚

A powerful command-line productivity tool powered by DeepSeek LLM, inspired by Shell GPT but optimized for DeepSeek's capabilities.

## Features

- 🤖 **AI-Powered Assistance**: Leverage DeepSeek's advanced language models
- 🐚 **Shell Command Generation**: Generate and execute shell commands with AI
- 💬 **Interactive Chat**: Persistent conversation sessions
- 🔄 **REPL Mode**: Interactive Read-Eval-Print Loop
- 🎭 **Persona System**: Specialized AI behaviors for different tasks
- ⚡ **Streaming Responses**: Real-time response generation
- 💾 **Smart Caching**: Reduce API costs with intelligent caching
- 🔧 **Function Calling**: Extensible tool integration
- 🎨 **Rich Formatting**: Beautiful markdown and syntax highlighting

## Installation

### From PyPI (Recommended)

```bash
pip install deepshell
```

### From Source

```bash
git clone https://github.com/deepshell/deepshell.git
cd deepshell
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/deepshell/deepshell.git
cd deepshell
pip install -e ".[dev]"
```

## Quick Start

1. **Get your DeepSeek API key** from [DeepSeek Platform](https://platform.deepseek.com/)

2. **Set your API key**:
   ```bash
   export DEEPSEEK_API_KEY="sk-your-api-key-here"
   ```

3. **Start using DeepShell**:
   ```bash
   # Basic usage
   deepshell "How do I list all files in a directory?"
   
   # Generate shell commands
   deepshell --shell "find large files over 100MB"
   
   # Start a chat session
   deepshell --chat mysession "Help me with Python scripting"
   
   # Interactive REPL mode
   deepshell --repl coding
   ```

## Usage Examples

### Shell Command Generation

```bash
# Generate shell commands
deepshell --shell "compress all .log files"
# Output: tar -czf logs.tar.gz *.log

# Interactive execution
deepshell --shell --interactive "backup my home directory"
# Generates command and prompts for execution
```

### Chat Sessions

```bash
# Start a persistent chat
deepshell --chat work "Help me debug this Python script"

# Continue the conversation
deepshell --chat work "Now optimize it for performance"

# List all chat sessions
deepshell --list-chats

# Show chat history
deepshell --show-chat work
```

### REPL Mode

```bash
# Start interactive REPL
deepshell --repl coding

# In REPL:
🤖 help me write a Python function to parse JSON
🤖 """
def complex_multiline_query():
    # This is multiline input
    pass
"""
🤖 exit
```

### Personas (Specialized AI Behaviors)

```bash
# Use shell expert persona
deepshell --persona shell "optimize this command: find . -name '*.py'"

# Use coding persona
deepshell --persona coder "write a REST API in FastAPI"

# Use reasoning persona for complex problems
deepshell --persona reasoning "explain the time complexity of quicksort"

# List available personas
deepshell --list-personas

# Create custom persona
deepshell --create-persona myexpert
```

### Code Generation

```bash
# Generate code without explanations
deepshell --code "Python function to calculate fibonacci"

# Generate with explanations
deepshell --persona coder "Python function to calculate fibonacci"
```

## Configuration

DeepShell uses a configuration file at `~/.config/deepshell/.deepshellrc`:

```ini
# API Configuration
DEEPSEEK_API_KEY=sk-your-key-here
API_BASE_URL=https://api.deepseek.com
DEFAULT_MODEL=deepseek-chat

# Display Options
PRETTIFY_MARKDOWN=true
DEFAULT_COLOR=cyan
CODE_THEME=monokai
DISABLE_STREAMING=false

# Cache Settings
ENABLE_CACHE=true
CACHE_LENGTH=100
CHAT_CACHE_LENGTH=100

# Advanced Options
REQUEST_TIMEOUT=60
MAX_RETRIES=3
USE_FUNCTIONS=true
```

### Environment Variables

All configuration options can be overridden with environment variables:

```bash
export DEEPSEEK_API_KEY="sk-your-key"
export DEFAULT_MODEL="deepseek-reasoner"
export DISABLE_STREAMING="false"
export PRETTIFY_MARKDOWN="true"
```

## Available Models

- **deepseek-chat**: General conversation and assistance (default)
- **deepseek-reasoner**: Advanced reasoning with chain-of-thought
- **deepseek-coder**: Specialized for code generation and programming

```bash
# Use reasoning model
deepshell --model deepseek-reasoner "solve this logic puzzle step by step"

# Use coding model
deepshell --model deepseek-coder "write a binary search algorithm"
```

## Built-in Personas

- **default**: General-purpose assistant
- **shell**: Shell command generation (no explanations)
- **describe-shell**: Shell command explanation
- **code**: Code generation (no explanations)
- **reasoning**: Step-by-step problem solving
- **coder**: Programming assistance with explanations

## Advanced Features

### Function Calling

DeepShell supports function calling for extended capabilities:

```bash
# Enable function calling
deepshell --functions "help me manage my files"
```

### Shell Integration

Install shell integration for hotkey access:

```bash
deepshell --install-integration
```

After installation, press `Ctrl+G` in your shell to trigger DeepShell suggestions.

### Caching

DeepShell automatically caches responses to reduce API costs:

```bash
# Disable caching for a request
deepshell --no-cache "give me a random joke"

# Clear cache
deepshell --clear-cache
```

### Streaming vs Non-streaming

```bash
# Disable streaming for faster batch processing
deepshell --no-stream "analyze this large dataset"

# Enable streaming for interactive feel (default)
deepshell --stream "write a long article about AI"
```

## Command Reference

### Basic Commands

```bash
deepshell [OPTIONS] [PROMPT]
```

### Options

| Option | Description |
|--------|-------------|
| `--model, -m` | DeepSeek model to use |
| `--temperature, -t` | Randomness (0.0-2.0) |
| `--top-p` | Nucleus sampling (0.0-1.0) |
| `--max-tokens` | Maximum response tokens |
| `--shell, -s` | Generate shell commands |
| `--describe-shell, -d` | Describe shell commands |
| `--code, -c` | Generate code only |
| `--interactive` | Interactive shell execution |
| `--chat` | Chat session ID |
| `--repl` | Start REPL mode |
| `--persona, -p` | AI persona to use |
| `--functions` | Enable function calling |
| `--stream/--no-stream` | Enable/disable streaming |
| `--cache/--no-cache` | Enable/disable caching |
| `--md/--no-md` | Enable/disable markdown |
| `--editor` | Use $EDITOR for input |

### Management Commands

| Command | Description |
|---------|-------------|
| `--list-chats, -lc` | List chat sessions |
| `--show-chat` | Show chat history |
| `--list-personas, -lp` | List personas |
| `--create-persona` | Create new persona |
| `--show-persona` | Show persona details |
| `--install-integration` | Install shell integration |
| `--version, -v` | Show version |

## Input Methods

DeepShell supports multiple input methods:

```bash
# Command line argument
deepshell "your prompt here"

# Stdin piping
echo "analyze this" | deepshell

# File redirection
deepshell "explain this code" < script.py

# Editor mode
deepshell --editor

# Here documents
deepshell <<< "your prompt"
```

## Error Handling

DeepShell provides helpful error messages and suggestions:

- **API Key Issues**: Clear instructions for setting up authentication
- **Rate Limits**: Automatic retry with exponential backoff
- **Network Issues**: Connection troubleshooting tips
- **Model Errors**: Model availability and parameter validation

## Performance Tips

1. **Use Caching**: Keep caching enabled for repeated queries
2. **Choose Right Model**: Use `deepseek-chat` for general tasks, `deepseek-reasoner` for complex problems
3. **Optimize Prompts**: Be specific and clear in your requests
4. **Batch Operations**: Use chat sessions for related queries
5. **Stream Responses**: Enable streaming for better perceived performance

## Troubleshooting

### Common Issues

**API Key Not Found**
```bash
export DEEPSEEK_API_KEY="sk-your-key-here"
# or add to ~/.config/deepshell/.deepshellrc
```

**Connection Issues**
```bash
# Check your internet connection
# Verify API endpoint accessibility
deepshell --version  # Test basic functionality
```

**Cache Issues**
```bash
# Clear cache if responses seem stale
rm -rf ~/.cache/deepshell/
```

**Permission Issues**
```bash
# Fix configuration directory permissions
chmod 755 ~/.config/deepshell/
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/deepshell/deepshell.git
cd deepshell
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
pytest --cov=deepshell  # With coverage
```

### Code Formatting

```bash
black deepshell/
isort deepshell/
flake8 deepshell/
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

## Support

- 📖 **Documentation**: [https://deepshell.readthedocs.io](https://deepshell.readthedocs.io)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/deepshell/deepshell/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/deepshell/deepshell/discussions)
- 📧 **Email**: team@deepshell.ai

## Acknowledgments

- Inspired by [Shell GPT](https://github.com/TheR1D/shell_gpt)
- Powered by [DeepSeek LLM](https://www.deepseek.com/)
- Built with [LiteLLM](https://github.com/BerriAI/litellm)
- CLI framework: [Typer](https://typer.tiangolo.com/)
- Rich formatting: [Rich](https://rich.readthedocs.io/)

---

**DeepShell** - Bringing the power of DeepSeek LLM to your command line! 🚀
