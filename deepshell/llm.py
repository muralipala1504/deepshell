"""
DeepSeek LLM client integration using LiteLLM.

This module provides a unified interface for interacting with DeepSeek's
language models through LiteLLM, with fallback to direct OpenAI SDK usage.
"""

import json
import os
import time
from typing import Any, Dict, Generator, List, Optional, Union

import litellm
from litellm import completion
from rich.console import Console

from .config import config

console = Console()

# Configure LiteLLM
litellm.suppress_debug_info = True
litellm.drop_params = True  # Drop unsupported parameters


class MockResponse:
    """Mock response object for error handling."""
    def __init__(self, content: str):
        self.choices = [MockChoice(content)]

class MockChoice:
    """Mock choice object for error handling."""
    def __init__(self, content: str):
        self.message = MockMessage(content)

class MockMessage:
    """Mock message object for error handling."""
    def __init__(self, content: str):
        self.content = content


class DeepSeekClient:
    """
    DeepSeek LLM client with streaming support and error handling.

    Uses LiteLLM for unified API access with automatic retries and
    comprehensive error handling.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: str = "deepseek-chat",
        timeout: int = 60,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ) -> None:
        """
        Initialize DeepSeek client.

        Args:
            api_key: DeepSeek API key (defaults to config/env)
            base_url: API base URL (defaults to config)
            model: Default model to use
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
            retry_delay: Base delay between retries
        """
        self.api_key = api_key or config.get("DEEPSEEK_API_KEY")
        self.base_url = base_url or config.get("API_BASE_URL")
        self.model = model
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # Set environment variables for LiteLLM
        if self.api_key:
            os.environ["DEEPSEEK_API_KEY"] = self.api_key

        # Validate configuration
        if not self.api_key:
            raise ValueError(
                "DeepSeek API key is required. Set DEEPSEEK_API_KEY environment "
                "variable or provide api_key parameter."
            )

    def _prepare_model_name(self, model: Optional[str] = None) -> str:
        """Prepare model name for LiteLLM."""
        model_name = model or self.model

        # Try without deepseek/ prefix first (as per our debugging)
        # if not model_name.startswith("deepseek/"):
        #     model_name = f"deepseek/{model_name}"

        return model_name

    def _create_error_response(self, error_message: str) -> Any:
        """Create a mock response object for error cases."""
        return MockResponse(f"❌ Error: {error_message}")

    def _retry_with_backoff(self, func, *args, **kwargs) -> Any:
        """Execute function with exponential backoff retry logic."""
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                result = func(*args, **kwargs)
                
                # Validate that we got a proper response
                if result is None:
                    raise ValueError("API returned None response")
                
                if isinstance(result, bool):
                    raise ValueError(f"API returned boolean: {result}")
                
                # Check if it has the expected structure for non-streaming
                if not kwargs.get('stream', False):
                    if not hasattr(result, 'choices'):
                        raise ValueError("API response missing 'choices' attribute")
                    if not result.choices:
                        raise ValueError("API response has empty choices")
                
                return result
                
            except Exception as e:
                last_exception = e
                console.print(f"DEBUG: Exception in attempt {attempt + 1}: {str(e)}")

                if attempt == self.max_retries:
                    break

                # Calculate delay with exponential backoff
                delay = self.retry_delay * (2 ** attempt)
                console.print(f"[yellow]Retry {attempt + 1}/{self.max_retries} in {delay:.1f}s...[/yellow]")
                time.sleep(delay)

        # Create error response instead of raising exception
        console.print(f"DEBUG: All retries failed, raising: {str(last_exception)}")
        return self._create_error_response(str(last_exception))

    def complete(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.0,
        top_p: float = 1.0,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        functions: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> Union[Any, Generator[str, None, None]]:
        """
        Generate completion from DeepSeek model.

        Args:
            messages: List of message dictionaries
            model: Model to use (defaults to instance default)
            temperature: Sampling temperature (0.0-2.0)
            top_p: Nucleus sampling parameter (0.0-1.0)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            functions: Function definitions for function calling
            **kwargs: Additional parameters

        Returns:
            Completion response or generator for streaming
        """
        model_name = self._prepare_model_name(model)

        # Prepare completion parameters
        completion_kwargs = {
            "model": model_name,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream,
            "timeout": self.timeout,
            "cache": kwargs.get("cache", True),
            **kwargs
        }

        # Add optional parameters
        if max_tokens is not None:
            completion_kwargs["max_tokens"] = max_tokens

        # Add function calling support
        if functions:
            completion_kwargs["tools"] = [
                {"type": "function", "function": func} for func in functions
            ]
            completion_kwargs["tool_choice"] = "auto"

        console.print(f"DEBUG: Using model: {model_name}")
        console.print(f"DEBUG: completion_kwargs: {completion_kwargs}")

        if stream:
            return self._stream_completion(**completion_kwargs)
        else:
            return self._retry_with_backoff(completion, **completion_kwargs)

    def _stream_completion(self, **kwargs) -> Generator[str, None, None]:
        """Handle streaming completion with proper error handling."""
        try:
            stream = self._retry_with_backoff(completion, **kwargs)

            for chunk in stream:
                if hasattr(chunk, 'choices') and chunk.choices:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, 'content') and delta.content:
                        yield delta.content
                    elif hasattr(delta, 'tool_calls') and delta.tool_calls:
                        # Handle function calls in streaming
                        for tool_call in delta.tool_calls:
                            if tool_call.function.name:
                                yield f"\n🔧 Calling function: {tool_call.function.name}\n"

        except Exception as e:
            console.print(f"[red]Streaming error: {str(e)}[/red]")
            yield f"❌ Streaming Error: {str(e)}"

    def chat(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        **kwargs
    ) -> Union[str, Generator[str, None, None]]:
        """
        Simple chat interface.

        Args:
            prompt: User prompt
            system_message: Optional system message
            **kwargs: Additional completion parameters

        Returns:
            Response string or generator for streaming
        """
        messages = []

        if system_message:
            messages.append({"role": "system", "content": system_message})

        messages.append({"role": "user", "content": prompt})

        try:
            response = self.complete(messages, **kwargs)

            if kwargs.get("stream", False):
                return response
            else:
                # Defensive check for response structure
                if not response or not hasattr(response, 'choices'):
                    return self._create_error_response("Invalid API response structure")
                
                if not response.choices:
                    return self._create_error_response("Empty choices in API response")
                
                if not hasattr(response.choices[0], 'message'):
                    return self._create_error_response("Invalid message structure in API response")
                
                if not hasattr(response.choices[0].message, 'content'):
                    return self._create_error_response("No content in API response message")
                
                return response

        except Exception as e:
            console.print(f"[red]Chat error: {str(e)}[/red]")
            return self._create_error_response(f"Chat failed: {str(e)}")

    def get_available_models(self) -> List[str]:
        """Get list of available DeepSeek models."""
        return [
            "deepseek-chat",
            "deepseek-reasoner",
            "deepseek-coder"
        ]

    def validate_model(self, model: str) -> bool:
        """Validate if model is available."""
        available_models = self.get_available_models()
        clean_model = model.replace("deepseek/", "")
        return clean_model in available_models

    def get_model_info(self, model: Optional[str] = None) -> Dict[str, Any]:
        """Get information about a specific model."""
        model_name = model or self.model
        clean_model = model_name.replace("deepseek/", "")

        model_info = {
            "deepseek-chat": {
                "name": "DeepSeek Chat",
                "description": "General conversation and assistance",
                "context_length": 64000,
                "max_output": 8000,
                "supports_functions": True,
                "supports_reasoning": False,
            },
            "deepseek-reasoner": {
                "name": "DeepSeek Reasoner",
                "description": "Chain-of-thought reasoning model",
                "context_length": 64000,
                "max_output": 64000,
                "supports_functions": True,
                "supports_reasoning": True,
            },
            "deepseek-coder": {
                "name": "DeepSeek Coder",
                "description": "Code generation and programming assistance",
                "context_length": 64000,
                "max_output": 8000,
                "supports_functions": True,
                "supports_reasoning": False,
            }
        }

        return model_info.get(clean_model, {
            "name": "Unknown Model",
            "description": "Model information not available",
            "context_length": 0,
            "max_output": 0,
            "supports_functions": False,
            "supports_reasoning": False,
        })

    def test_connection(self) -> bool:
        """Test connection to DeepSeek API."""
        try:
            response = self.complete(
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            
            # Defensive check
            if not response or not hasattr(response, 'choices') or not response.choices:
                return False
            
            if not hasattr(response.choices[0], 'message') or not response.choices[0].message:
                return False
                
            return bool(response.choices[0].message.content)
            
        except Exception as e:
            console.print(f"[red]Connection test failed: {str(e)}[/red]")
            return False


# Global client instance
_client: Optional[DeepSeekClient] = None


def get_client() -> DeepSeekClient:
    """Get or create global DeepSeek client instance."""
    global _client

    if _client is None:
        _client = DeepSeekClient(
            model=config.get("DEFAULT_MODEL"),
            timeout=config.get("REQUEST_TIMEOUT"),
            max_retries=config.get("MAX_RETRIES"),
            retry_delay=config.get("RETRY_DELAY"),
        )

    return _client


def reset_client() -> None:
    """Reset global client instance."""
    global _client
    _client = None
