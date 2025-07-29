
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
    """
    Manages a persistent chat session with message history.
    
    Handles message storage, retrieval, and truncation to stay within
    context limits while preserving conversation continuity.
    """
    
    def __init__(self, session_id: str, max_length: int = 100) -> None:
        """
        Initialize chat session.
        
        Args:
            session_id: Unique session identifier
            max_length: Maximum number of messages to keep
        """
        self.session_id = session_id
        self.max_length = max_length
        self.is_temp = session_id == "temp"
        
        # Session file path
        if not self.is_temp:
            cache_dir = Path(config.get("CHAT_CACHE_PATH"))
            cache_dir.mkdir(parents=True, exist_ok=True)
            self.session_file = cache_dir / f"{session_id}.json"
        else:
            self.session_file = None
        
        # Load existing messages
        self.messages: List[Dict[str, Any]] = []
        if not self.is_temp and self.session_file and self.session_file.exists():
            self._load_messages()
    
    def _load_messages(self) -> None:
        """Load messages from session file."""
        try:
            with open(self.session_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.messages = data.get("messages", [])
        except (json.JSONDecodeError, IOError) as e:
            console.print(f"[yellow]Warning: Could not load session {self.session_id}: {e}[/yellow]")
            self.messages = []
    
    def _save_messages(self) -> None:
        """Save messages to session file."""
        if self.is_temp or not self.session_file:
            return
        
        try:
            session_data = {
                "session_id": self.session_id,
                "created_at": time.time(),
                "messages": self.messages
            }
            
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
        
        except IOError as e:
            console.print(f"[yellow]Warning: Could not save session {self.session_id}: {e}[/yellow]")
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add message to session.
        
        Args:
            role: Message role (system, user, assistant)
            content: Message content
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": time.time()
        }
        
        self.messages.append(message)
        self._truncate_messages()
        self._save_messages()
    
    def _truncate_messages(self) -> None:
        """Truncate messages to stay within max_length."""
        if len(self.messages) <= self.max_length:
            return
        
        # Keep the first message (usually system prompt) and recent messages
        if self.messages and self.messages[0]["role"] == "system":
            system_message = self.messages[0]
            recent_messages = self.messages[-(self.max_length - 1):]
            self.messages = [system_message] + recent_messages
        else:
            self.messages = self.messages[-self.max_length:]
    
    def get_messages(self) -> List[Dict[str, str]]:
        """
        Get messages formatted for API calls.
        
        Returns:
            List of message dictionaries without timestamps
        """
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.messages
        ]
    
    def clear(self) -> None:
        """Clear all messages from session."""
        self.messages = []
        if not self.is_temp and self.session_file and self.session_file.exists():
            try:
                self.session_file.unlink()
            except OSError as e:
                console.print(f"[yellow]Warning: Could not delete session file: {e}[/yellow]")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get session summary information."""
        return {
            "session_id": self.session_id,
            "is_temp": self.is_temp,
            "message_count": len(self.messages),
            "max_length": self.max_length,
            "file_path": str(self.session_file) if self.session_file else None,
        }


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
                
                content = response.choices[0].message.content
                self.print_response(content)
                
                # Add assistant response to session
                self.session.add_message("assistant", content)
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled by user[/yellow]")
        
        except Exception as e:
            self.handle_error(e)
    
    @staticmethod
    def list_sessions() -> None:
        """List all available chat sessions."""
        cache_dir = Path(config.get("CHAT_CACHE_PATH"))
        
        if not cache_dir.exists():
            console.print("[yellow]No chat sessions found[/yellow]")
            return
        
        session_files = list(cache_dir.glob("*.json"))
        
        if not session_files:
            console.print("[yellow]No chat sessions found[/yellow]")
            return
        
        table = Table(title="Chat Sessions", show_header=True, header_style="bold cyan")
        table.add_column("Session ID", style="green")
        table.add_column("Messages", style="white")
        table.add_column("Last Modified", style="dim")
        
        for session_file in sorted(session_files, key=lambda f: f.stat().st_mtime, reverse=True):
            session_id = session_file.stem
            
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                message_count = len(data.get("messages", []))
                last_modified = time.strftime(
                    "%Y-%m-%d %H:%M",
                    time.localtime(session_file.stat().st_mtime)
                )
                
                table.add_row(session_id, str(message_count), last_modified)
            
            except (json.JSONDecodeError, IOError):
                table.add_row(session_id, "Error", "Unknown")
        
        console.print(table)
    
    @staticmethod
    def show_session(session_id: str) -> None:
        """
        Display chat session history.
        
        Args:
            session_id: Session to display
        """
        cache_dir = Path(config.get("CHAT_CACHE_PATH"))
        session_file = cache_dir / f"{session_id}.json"
        
        if not session_file.exists():
            console.print(f"[red]Error: Session '{session_id}' not found[/red]")
            return
        
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            messages = data.get("messages", [])
            
            if not messages:
                console.print(f"[yellow]Session '{session_id}' is empty[/yellow]")
                return
            
            console.print(f"\n[bold cyan]Chat Session: {session_id}[/bold cyan]")
            console.print(f"Messages: {len(messages)}\n")
            
            for i, message in enumerate(messages):
                role = message["role"]
                content = message["content"]
                
                # Format role with colors
                if role == "system":
                    role_display = "[dim]System[/dim]"
                elif role == "user":
                    role_display = "[bold green]User[/bold green]"
                elif role == "assistant":
                    role_display = "[bold blue]Assistant[/bold blue]"
                else:
                    role_display = f"[yellow]{role.title()}[/yellow]"
                
                # Create panel for each message
                panel = Panel(
                    content,
                    title=f"{role_display} (Message {i + 1})",
                    border_style="dim",
                    padding=(0, 1)
                )
                
                console.print(panel)
        
        except (json.JSONDecodeError, IOError) as e:
            console.print(f"[red]Error reading session '{session_id}': {e}[/red]")
    
    @staticmethod
    def delete_session(session_id: str) -> None:
        """
        Delete a chat session.
        
        Args:
            session_id: Session to delete
        """
        cache_dir = Path(config.get("CHAT_CACHE_PATH"))
        session_file = cache_dir / f"{session_id}.json"
        
        if not session_file.exists():
            console.print(f"[red]Error: Session '{session_id}' not found[/red]")
            return
        
        try:
            session_file.unlink()
            console.print(f"[green]✓ Session '{session_id}' deleted successfully[/green]")
        except OSError as e:
            console.print(f"[red]Error deleting session '{session_id}': {e}[/red]")
