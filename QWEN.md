# Telegram Bot — Birthday & Notes

## Project Overview

This is a **Telegram bot** built with **aiogram 3.x** that provides birthday tracking, notes management, and various utility features. The bot uses **SQLite** for data persistence and **APScheduler** for scheduled tasks.

### Main Features

- **Birthday Management**: Add, view, edit, and delete birthday records with automatic reminders
- **Notes System**: Create text/photo/audio/video/document notes with edit/delete functionality
- **Admin Panel**: Send announcements to all users, manage user data
- **Utility Functions**:
  - Weather forecast (5 days)
  - Currency exchange rates (USD, EUR, AMD, BTC, ETH)
  - Random jokes/toasts/wishes
  - Random greeting cards
  - Ideal weight calculator (multiple formulas)

### Architecture

```
Beget/
├── main.py              # Entry point, bot initialization, scheduler setup
├── config.py            # Configuration (TOKEN, MY_ID, API_KEY) - NOT in repo
├── requirements.txt     # Python dependencies
├── app/
│   ├── handlers.py      # Main user handlers (birthday CRUD, weight calculator)
│   ├── handlers_notes.py # Notes management handlers
│   ├── handlers_admin.py # Admin panel handlers
│   ├── database.py      # SQLite operations with aiosqlite
│   ├── func.py          # External API calls (weather, currency, jokes)
│   └── keyboards.py     # Reply and inline keyboard definitions
├── DATA/
│   └── user.db          # SQLite database (gitignored)
├── files/
│   ├── toasts.txt       # Toast messages
│   └── wishes.txt       # Greeting wishes
└── images/              # Random greeting cards
```

### Technologies

| Component | Technology |
|-----------|------------|
| Framework | aiogram 3.26.0 |
| Database | SQLite (aiosqlite 0.22.1) |
| Scheduling | APScheduler 3.11.2 |
| HTTP Client | aiohttp, requests |
| Parsing | BeautifulSoup4 |

## Building and Running

### Prerequisites

- Python 3.8+
- Telegram Bot Token (from @BotFather)
- OpenWeatherMap API key (for weather feature)

### Setup

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create config.py with required variables
echo "TOKEN = 'your_bot_token'" > config.py
echo "MY_ID = your_telegram_id" >> config.py
echo "API_KEY = 'your_openweathermap_key'" >> config.py

# Run the bot
python main.py
```

### Scheduled Jobs

| Job | Time (MSK) | Description |
|-----|------------|-------------|
| `delta_db` | 03:07 | Update birthday countdown timers |
| `open_birthday` | 12:00 | Send birthday notifications |
| `open_birthday_reminder` | 12:00 | Send 3-day birthday reminders |

## Development Conventions

### Code Style

- **FSM States**: Named groups (`Form`, `Notes`, `UserData`, `PhotoForm`) for different workflows
- **Database**: All paths use `pathlib.Path` for cross-platform compatibility
- **Error Handling**: Admin receives error notifications for failed user messages
- **Naming**: Russian function/variable names in handlers, English in utilities

### Database Structure

**Tables:**
- `users` — Telegram users (tg_id, full_name, id_data)
- `birthday` — Birthday records (tg_id, surname, name, data, delta_time, age)
- `notes` — User notes (tg_id, note_name, note_text, note_data, note_type, file_id)

### Key Patterns

- **State Management**: aiogram FSM for multi-step forms
- **Callback Data**: Prefix-based routing (`notes_`, `edit_`, etc.)
- **Inline Keyboards**: Dynamic generation from database results

## Configuration Variables

| Variable | Description |
|----------|-------------|
| `TOKEN` | Telegram bot API token |
| `MY_ID` | Admin Telegram ID |
| `API_KEY` | OpenWeatherMap API key |

## API Endpoints Used

- `https://www.cbr-xml-daily.ru/daily_json.js` — Currency rates
- `http://api.openweathermap.org/data/2.5/forecast` — Weather forecast
- `https://anekdotov.net/anekdot/day/` — Random jokes
- `https://api.coinbase.com/v2/exchange-rates` — Crypto rates
