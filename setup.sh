#!/bin/bash

echo "Starting setup..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please create a .env file with the following variables:"
    echo "TELEGRAM_BOT_TOKEN=your_bot_token"
    echo "TELEGRAM_CHAT_ID=your_chat_id"
    echo "CHECK_INTERVAL=300"
    echo "VENUE_ID=334"
    exit 1
fi

# Update system
sudo apt-get update
sudo apt-get install -y python3-full python3-venv tmux

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies in virtual environment
pip install -r requirements.txt

# Kill existing tmux session if it exists
tmux kill-session -t event_checker 2>/dev/null || true

#Wait for 10 seconds to make sure the session is killed
sleep 10

# Create a new tmux session and run the script
tmux new-session -d -s event_checker
tmux send-keys -t event_checker "cd $(pwd)" Enter
tmux send-keys -t event_checker "source venv/bin/activate" Enter
tmux send-keys -t event_checker "python check_events.py" Enter

# Setup auto-start on reboot
CURRENT_PATH=$(pwd)
CRON_CMD="@reboot sleep 30 && cd ${CURRENT_PATH} && ./setup.sh"
(crontab -l 2>/dev/null | grep -v "${CURRENT_PATH}/setup.sh"; echo "$CRON_CMD") | crontab -

echo "Setup completed! Your script is running in tmux session 'event_checker'"
echo "The script will check for new events every 5 minutes"
echo ""
echo "Useful commands:"
echo "- View the running script: tmux attach -t event_checker"
echo "- Detach from session: Press Ctrl+B, then D"
echo "- List sessions: tmux ls"
echo "- Kill session: tmux kill-session -t event_checker"
echo ""
echo "Script will automatically start on system reboot (after 30s delay)" 