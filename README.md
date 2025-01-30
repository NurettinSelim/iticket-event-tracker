# iTicket Event Tracker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://core.telegram.org/bots)

A Python script that monitors iTicket events and sends notifications via Telegram when new events are posted.

## Features

- 🔄 Automatically checks for new events every 5 minutes
- 📱 Sends notifications via Telegram
- 🔒 Secure configuration using environment variables
- 🚀 Runs in tmux for persistent operation
- 🔄 Auto-restarts on system reboot

## Prerequisites

- Python 3.x
- tmux
- A Telegram bot token and chat ID

## Installation

1. Clone the repository:
```bash
git clone https://github.com/NurettinSelim/iticket-event-tracker.git
cd iticket-event-tracker
```

2. Create a `.env` file with your configuration:
```bash
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
CHECK_INTERVAL=300  # Check interval in seconds (default: 5 minutes)
VENUE_ID=334       # iTicket venue ID
```

3. Make the setup script executable:
```bash
chmod +x setup.sh
```

4. Run the setup script:
```bash
./setup.sh
```

## Usage

The script runs automatically in a tmux session after setup. Here are some useful commands:

- View the running script:
```bash
tmux attach -t event_checker
```

- Detach from the tmux session (leave it running):
  - Press `Ctrl+B`
  - Then press `D`

- List active tmux sessions:
```bash
tmux ls
```

- Kill the script session:
```bash
tmux kill-session -t event_checker
```

## Configuration

You can modify the following settings in the `.env` file:

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token (get it from @BotFather)
- `TELEGRAM_CHAT_ID`: Your Telegram chat ID
- `CHECK_INTERVAL`: How often to check for new events (in seconds)
- `VENUE_ID`: The iTicket venue ID to monitor

## Auto-start on Reboot

The script is automatically configured to start on system reboot with a 30-second delay. This is handled by a crontab entry created during setup.

## Logs

The script outputs its status to the tmux session, which you can view by attaching to the session. It shows:
- When checks are performed
- Any new events found
- Error messages if something goes wrong

## Troubleshooting

1. If the script isn't running:
   - Check if tmux session exists: `tmux ls`
   - View the script output: `tmux attach -t event_checker`
   - Ensure the .env file exists and has correct values

2. If Telegram messages aren't being sent:
   - Verify your bot token is correct
   - Make sure you've started a conversation with your bot
   - Check if your chat ID is correct

3. If the script doesn't start after reboot:
   - Check your crontab entries: `crontab -l`
   - Verify the script path in crontab is correct
   - Ensure setup.sh has execute permissions

## License

This project is open source and available under the MIT License. 