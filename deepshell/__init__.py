
"""
DeepShell - A command-line productivity tool powered by DeepSeek LLM

DeepShell is a Shell GPT-inspired CLI tool that leverages DeepSeek's powerful
language models to provide AI-powered assistance for shell commands, code
generation, and general queries.

Key Features:
- Shell command generation and explanation
- Interactive chat sessions
- REPL mode for continuous interaction
- Role-based AI personas
- Function calling capabilities
- Streaming responses
- Comprehensive caching system
"""

__version__ = "1.0.0"
__author__ = "DeepShell Team"
__email__ = "team@deepshell.ai"
__license__ = "MIT"

from .cli import app
from .config import config
#from .llm import DeepSeekClient

__all__ = ["app", "config", "DeepSeekClient", "__version__"]
