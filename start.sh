#!/bin/bash
set -e

# Unzip the discord bot archive
echo "Unzipping discord-bot.zip..."
python -c "import zipfile; zipfile.ZipFile('discord-bot.zip').extractall('.')"

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
    pip install -r requirements.txt
else
    echo "No requirements.txt found, skipping dependency installation."
fi

# Run the bot using the first entry point that exists
if [ -f "main.py" ]; then
    echo "Starting bot with main.py..."
    exec python main.py
elif [ -f "bot.py" ]; then
    echo "Starting bot with bot.py..."
    exec python bot.py
elif [ -f "app.py" ]; then
    echo "Starting bot with app.py..."
    exec python app.py
else
    echo "ERROR: Could not find a bot entry point (main.py, bot.py, or app.py)." >&2
    echo "Files in current directory:" >&2
    ls -la >&2
    exit 1
fi
