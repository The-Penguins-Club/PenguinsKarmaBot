
# Penguins Karma Bot

A Telegram bot for tracking karma in group chats, built with Python and the python-telegram-bot library. Created for [Penguins Network](https://t.me/The_penguinsClub).

## Features

- **Karma System**: Give or take karma from users with `+1` or `-1` replies
- **Karma Statistics**: View karma leaderboards with `/stats`
- **Sudo Management**: Add or remove administrators with `/addsudo` and `/rmsudo`
- **Backup & Restart**: Admin commands for bot management
- **SQLite Database**: Persistent storage of user karma and history

## Prerequisites

- Python 3.8 or higher
- A Telegram Bot Token (get one from [@BotFather](https://t.me/BotFather))
- Your Telegram User ID
- Your group/network chat ID

## Installation & Deployment

### 1. Configuration

First, create your configuration file:

```bash
cp sample_config.env .env
```

Edit `.env` and add your credentials:

```env
BOT_TOKEN=your_bot_token_here
SUDOERS=your_user_id,other_user_id  # Comma-separated list
NETWORK=your_group_chat_id
```

### 2. Choose Your Deployment Method

#### Option A: Standard Python (Development)

```bash
pip3 install -r requirements.txt
python3 -m bot
```

#### Option B: UV (Fast Python Package Manager)

```bash
uv sync
uv run -m bot
```

#### Option C: Docker (Recommended for Production)

```bash
docker compose up -d
```

To view logs:
```bash
docker compose logs -f
```

To stop the bot:
```bash
docker compose down
```

## Usage

### User Commands

- `/start` - Start the bot and get a welcome message
- `/help` - Show available commands
- `/stats` - Display karma leaderboard (groups only)

### Karma Actions

Reply to a message with:
- `+1` or `+` - Give karma
- `-1` or `-` - Take karma

### Admin Commands (Sudoers Only)

- `/addsudo` - Reply to a user to grant them sudo privileges
- `/rmsudo` - Reply to a user to revoke sudo privileges
- `/backup` - Get a backup of the database (private chat)
- `/restart` - Restart the bot (private chat)

## Project Structure

```
PenguinsKarmaBot/
├── bot/
│   ├── __init__.py          # Main application setup
│   ├── __main__.py          # Entry point
│   ├── database.py          # Database configuration
│   ├── models.py            # Database models
│   └── plugins/
│       ├── karma.py         # Karma functionality
│       ├── misc.py          # Helper commands
│       └── sudoers.py       # Admin management
├── compose.yml              # Docker Compose configuration
├── Dockerfile               # Docker build instructions
├── requirements.txt         # Python dependencies
└── sample_config.env        # Example configuration
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

See [LICENSE](LICENSE) file for details.