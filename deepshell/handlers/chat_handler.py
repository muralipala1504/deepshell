class ChatSession:
    """
    Manages a persistent chat session with message history.

    Handles message storage, retrieval, and truncation to stay within
    context limits while preserving conversation continuity.
    """

    def __init__(self, session_id: str, max_length: int = 100) -> None:
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
        try:
            with open(self.session_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.messages = data.get("messages", [])
        except (json.JSONDecodeError, IOError) as e:
            console.print(f"[yellow]Warning: Could not load session {self.session_id}: {e}[/yellow]")
            self.messages = []

    def _save_messages(self) -> None:
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
        message = {
            "role": role,
            "content": content,
            "timestamp": time.time()
        }

        self.messages.append(message)
        self._truncate_messages()
        self._save_messages()

    def _truncate_messages(self) -> None:
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
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.messages
        ]

    def clear(self) -> None:
        self.messages = []
        if not self.is_temp and self.session_file and self.session_file.exists():
            try:
                self.session_file.unlink()
            except OSError as e:
                console.print(f"[yellow]Warning: Could not delete session file: {e}[/yellow]")

    def get_summary(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "is_temp": self.is_temp,
            "message_count": len(self.messages),
            "max_length": self.max_length,
            "file_path": str(self.session_file) if self.session_file else None,
        }
