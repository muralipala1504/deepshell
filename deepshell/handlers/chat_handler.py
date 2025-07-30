"""
Chat handler for persistent conversation sessions.

Manages conversation history, session persistence, and multi-turn interactions.
"""

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .base_handler import BaseHandler
from ..config import config
from ..persona import Persona

console = Console()


class ChatSession:
    # ... (no changes needed in ChatSession, so keep as is)
    # Paste your existing ChatSession class here


class ChatHandler(BaseHandler):
    """
    Handler for persistent chat conversations.

    Manages conversation sessions with history persistence and
    multi-turn interactions.
    """

    def __init__(self, session_id: str, persona: Persona, markdown: bool = True) -> None:
        """
        Initialize chat handler.

        Args:
            session_id: Chat session identifier
            persona: AI persona to use
            markdown: Whether to enable markdown formatting
        """
        super().__init__(persona, markdown)

        self.session = ChatSession(
            session_id=session_id,
            max_length=config.get("CHAT_CACHE_LENGTH")
        )

        # Add system message if this is a new session
        if not self.session.messages:
            self.session.add_message("system", self.persona.system_prompt)

    def make_messages(self, prompt: str) -> List[Dict[str, str]]:
        """
        Create message list including conversation history.

        Args:
            prompt: User prompt

        Returns:
            List of messages including history and new prompt
        """
        # Add user message to session
        self.session.add_message("user", prompt)

        # Return all messages for API call
        return self.session.get_messages()

    def handle(self, prompt: str, **options) -> None:
        """
        Handle chat interaction with history.

        Args:
            prompt: User prompt to process
            **options: Handler options (model, temperature, etc.)
        """
        if not prompt.strip():
            console.print("[red]Error: Empty prompt provided[/red]")
            return

        try:
            # Validate options
            validated_options = self.validate_options(**options)

            # Create messages with history
            messages = self.make_messages(prompt)

            # Get response
            if validated_options["stream"]:
                # Streaming response
                response_generator = self.get_completion(
                    messages=messages,
                    **validated_options
                )

                full_response = self.stream_response(response_generator)

                # Add assistant response to session
                self.session.add_message("assistant", full_response)

            else:
                # Non-streaming response
                response = self.get_completion(
                    messages=messages,
                    **validated_options
                )

                # Defensive: check for response structure
                if not response or not hasattr(response, 'choices') or not response.choices:
                    console.print("[red]Error: Invalid response from LLM[/red]")
                    return
                if not hasattr(response.choices[0], 'message') or not response.choices[0].message:
                    console.print("[red]Error: Invalid message in response[/red]")
                    return
                if not hasattr(response.choices[0].message, 'content'):
                    console.print("[red]Error: No content in response message[/red]")
                    return

                content = response.choices[0].message.content
                self.print_response(content)

                # Add assistant response to session
                self.session.add_message("assistant", content)

        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled by user[/yellow]")

        except Exception as e:
            self.handle_error(e)

    # ... (rest of ChatHandler unchanged)
    # Paste your existing static methods (list_sessions, show_session, delete_session) here
