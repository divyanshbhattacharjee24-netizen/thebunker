#!/bin/bash
set -e

# Unzip the discord bot archive.
# Prefer `unzip` (always available in Railpack Python images), fall back to
# python3 (the correct binary name in modern Python environments).
echo "Unzipping discord-bot.zip..."
if command -v unzip >/dev/null 2>&1; then
    unzip -o discord-bot.zip
elif command -v python3 >/dev/null 2>&1; then
    python3 -c "import zipfile; zipfile.ZipFile('discord-bot.zip').extractall('.')"
else
    echo "ERROR: Neither 'unzip' nor 'python3' is available to extract discord-bot.zip." >&2
    exit 1
fi

# If the zip extracted into a subdirectory, move into it
# (look for a directory that isn't a known top-level file)
EXTRACTED_DIR=""
for item in */; do
    if [ -d "$item" ]; then
        EXTRACTED_DIR="${item%/}"
        break
    fi
done

if [ -n "$EXTRACTED_DIR" ]; then
    echo "Entering extracted directory: $EXTRACTED_DIR"
    cd "$EXTRACTED_DIR"
fi

# Install Python dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    python3 -m pip install -r requirements.txt
else
    echo "No requirements.txt found, skipping dependency installation."
fi

# Run the bot using the first entry point that exists
if [ -f "main.py" ]; then
    echo "Starting bot with main.py..."
    exec python3 main.py
elif [ -f "bot.py" ]; then
    echo "Starting bot with bot.py..."
    exec python3 bot.py
elif [ -f "app.py" ]; then
    echo "Starting bot with app.py..."
    exec python3 app.py
else
    echo "ERROR: Could not find a bot entry point (main.py, bot.py, or app.py)." >&2
    echo "Files in current directory:" >&2
    ls -la >&2
    exit 1
fi
