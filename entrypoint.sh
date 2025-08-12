#!/bin/sh
<<<<<<< HEAD

# List of known commands
KNOWN_COMMANDS="main repl chat show-chat list-chats create-persona show-persona list-personas install-integration"

# If no argument, insert 'main'
if [ -z "$1" ]; then
  set -- main
else
  FOUND=0
  for cmd in $KNOWN_COMMANDS; do
    if [ "$1" = "$cmd" ]; then
      FOUND=1
      break
    fi
  done
  # If first arg is not a known command, prepend 'main'
  if [ $FOUND -eq 0 ]; then
    set -- main "$@"
  fi
fi

=======
if [ "$1" = "" ]; then
  set -- main
fi
>>>>>>> 399a905 (Dcokerfile fixed)
exec deepshell "$@"
