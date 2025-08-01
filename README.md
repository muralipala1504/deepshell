DeepShell 🐚

Your AI Second Opinion for the Command Line

Ever wish you could get a second (or third) opinion before running a risky command or deploying a new script?
DeepShell brings the wisdom of multiple top AI models—OpenAI, Gemini, and DeepSeek—right to your terminal.

Don’t just ask one AI—get a consensus.
DeepShell is your trusted, multi-provider assistant for Linux, coding, and automation.

Features

	🤖 AI-Powered Assistance: Leverage advanced language models from OpenAI, Gemini, and DeepSeek
    🐚 Shell Command Generation: Generate and execute shell commands with AI
    💬 Interactive Chat: Persistent conversation sessions
    🔄 REPL Mode: Interactive Read-Eval-Print Loop
    🎭 Persona System: Specialized AI behaviors for different tasks
    ⚡ Streaming Responses: Real-time response generation
    💾 Smart Caching: Reduce API costs with intelligent caching
    🔧 Function Calling: Extensible tool integration
    🎨 Rich Formatting: Beautiful markdown and syntax highlighting
    🌐 Multi-Provider: Seamlessly switch between OpenAI, Gemini, and DeepSeek
    🩺 Consensus Mode (coming soon!): See where LLMs agree or differ—just like getting a second opinion from another expert
	
	Why DeepShell?
	
	Just like you’d get a second opinion from another doctor before a big health decision, DeepShell lets you cross-check your sysadmin moves, scripts, and troubleshooting steps with answers from multiple LLMs.

    Reduce risk by seeing where the AIs agree (or disagree) before you act
    Build confidence in your DevOps and coding work
    Vendor-neutral: Not tied to one AI provider
	
	Installation
	From PyPI (Recommended)

	pip install deepshell	
	
	From Source
	
	git clone https://github.com/deepshell/deepshell.git
	cd deepshell
	pip install -e .
	
	Development Installation
	
	git clone https://github.com/deepshell/deepshell.git
	cd deepshell
	pip install -e ".[dev]"
	
	Development Installation
	
	git clone https://github.com/deepshell/deepshell.git
	cd deepshell
	pip install -e ".[dev]"
	
	Quick Start

	Get your API key(s):

    OpenAI
    Gemini (Google AI Studio)
    DeepSeek (optional)

	Set your API key(s):
	
	# For OpenAI
	export OPENAI_API_KEY="sk-your-openai-key"
	# For Gemini
	export GEMINI_API_KEY="your-gemini-key"
	# For DeepSeek (optional)
	export DEEPSEEK_API_KEY="sk-your-deepseek-key"
	
	Start using DeepShell:
	
	# Use OpenAI (default or via --provider)
	deepshell --provider openai "How do I list all files in a directory?"

	# Use Gemini
	deepshell --provider gemini "Show me a bash script to backup /etc"

	#Use DeepSeek (if you have a paid key)
	deepshell --provider deepseek "Explain Linux file permissions"
	
	Usage Examples
    Shell Command Generation
	
	deepshell --provider openai --shell "compress all .log files"
	deepshell --provider gemini --shell "find large files over 100MB"
	
	Chat Sessions
	
	deepshell --provider openai --chat work "Help me debug this Python script"
	deepshell --provider gemini --chat devops "How do I automate user creation in Linux?"
	
	REPL Mode
	
	deepshell --provider openai --repl coding
	deepshell --provider gemini --repl sysadmin
	
	Personas (Specialized AI Behaviors)
	
	deepshell --provider openai --persona shell "optimize this command: find . -name '*.py'"
	deepshell --provider gemini --persona coder "write a REST API in FastAPI"
	
	Configuration

	DeepShell uses a configuration file at ~/.config/deepshell/.deepshellrc:
	
	# Provider Configuration
PROVIDER=openai  # or gemini, deepseek

	# API Keys
	OPENAI_API_KEY=sk-your-openai-key
	GEMINI_API_KEY=your-gemini-key
	DEEPSEEK_API_KEY=sk-your-deepseek-key

	# Model Configuration
	DEFAULT_MODEL=gpt-3.5-turbo  # or gemini-1.5-pro, deepseek-chat

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
	
	Environment Variables

	All configuration options can be overridden with environment variables:
	
	export PROVIDER="openai"
	export OPENAI_API_KEY="sk-your-key"
	export GEMINI_API_KEY="your-gemini-key"
	export DEEPSEEK_API_KEY="sk-your-key"
	export DEFAULT_MODEL="gpt-3.5-turbo"
	
	Supported Providers & Models
	
	Provider	Free?	Recommended For	Example Model	Notes
	OpenAI	Yes	General, code, Linux, DevOps	gpt-3.5-turbo, gpt-4o	Most users, reliable
	Gemini	Yes	General, code, Linux, DevOps	gemini-1.5-pro	Free API, strong
	DeepSeek	No	Optional, for users with paid API key	deepseek-chat, deepseek-coder	Paid only
	
	Command Reference
	Basic Commands
	
	deepshell [OPTIONS] [PROMPT]
	
	Options
	
	Option	Description
	--provider	LLM provider to use (openai, gemini, deepseek)
	--model, -m	Model to use (see above)
	--temperature, -t	Randomness (0.0-2.0)
	--top-p	Nucleus sampling (0.0-1.0)
	--max-tokens	Maximum response tokens
	--shell, -s	Generate shell commands
	--describe-shell, -d	Describe shell commands
	--code, -c	Generate code only
	--interactive	Interactive shell execution
	--chat	Chat session ID
	--repl	Start REPL mode
	--persona, -p	AI persona to use
	--functions	Enable function calling
	--stream/--no-stream	Enable/disable streaming
	--cache/--no-cache	Enable/disable caching
	--md/--no-md	Enable/disable markdown
	--editor	Use $EDITOR for input
	
	Input Methods

	DeepShell supports multiple input methods:
	
	deepshell "your prompt here"
	echo "analyze this" | deepshell
	deepshell "explain this code" < script.py
	deepshell --editor
	deepshell <<< "your prompt"
	
	Error Handling

	DeepShell provides helpful error messages and suggestions:

    API Key Issues: Clear instructions for setting up authentication
    Rate Limits: Automatic retry with exponential backoff
    Network Issues: Connection troubleshooting tips
    Model Errors: Model availability and parameter validation
	
	
	Performance Tips

    Use Caching: Keep caching enabled for repeated queries
    Choose Right Model: Use gpt-3.5-turbo or gemini-1.5-pro for most tasks
    Optimize Prompts: Be specific and clear in your requests
    Batch Operations: Use chat sessions for related queries
    Stream Responses: Enable streaming for better perceived performance
	
	Troubleshooting
	Common Issues

	API Key Not Found
	
	export OPENAI_API_KEY="sk-your-key-here"
	export GEMINI_API_KEY="your-gemini-key"
	# or add to ~/.config/deepshell/.deepshellrc
	
	Connection Issues
	
	# Check your internet connection
	# Verify API endpoint accessibility
	deepshell --version  # Test basic functionality
	
	Cache Issues
	
	rm -rf ~/.cache/deepshell/
	
	Permission Issues
	
	chmod 755 ~/.config/deepshell/
	
	Contributing

	We welcome contributions! Please see our Contributing Guide for details.
	
	git clone https://github.com/deepshell/deepshell.git
	cd deepshell
	python -m venv venv
	source venv/bin/activate  # On Windows: venv\Scripts\activate
	pip install -e ".[dev]"
	
	Running Tests

	pytest
	pytest --cov=deepshell  # With coverage	
	
	black deepshell/
	isort deepshell/
	flake8 deepshell/

License

MIT License - see LICENSE file for details.

Changelog

See CHANGELOG.md for version history and updates.


Support

    📖 Documentation: https://deepshell.readthedocs.io
    🐛 Bug Reports: GitHub Issues
    💬 Discussions: GitHub Discussions
    📧 Email: team@deepshell.ai

Acknowledgments

    Inspired by Shell GPT
    Powered by OpenAI, Gemini, and DeepSeek
    Built with LiteLLM
    CLI framework: Typer
    Rich formatting: Rich	
	
	DeepShell – Bringing the power of the world’s best LLMs to your command line! 🚀
Don’t just ask one AI—get a consensus.
	