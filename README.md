# VPN Telegram Bot

I started working on this project after needing to change my n-th VPN provider due to their blocking in my country. At some point, I decided to create my own. So far it has been working flawlessly.

When friends learned about my solution, they started asking for access. What began as occasional requests soon became frequent enough that manually creating and distributing configurations was becoming time-consuming. Additionally, since maintaining servers comes with costs, I needed a way to manage subscriptions and handle payments.

The Telegram bot emerged as a practical solution - it automates user registration, subscription management, and configuration distribution. Users can now purchase access directly through Telegram, receive their VPN configurations immediately, and manage their own accounts without needing my constant involvement.

## Technical Stack

Bot: aiogram 3.x
Backend: FastAPI with SQLAlchemy ORM and PostgreSQL database

## Bot commands
- `/start` – Start 
- `/help` – Show help
- `/buy {n}` – Purchase subscription for `n` days

## Setup
1. Get your Telegram bot token from [@BotFather](https://t.me/BotFather)

2. Edit `config/config.example.env` and run command below:
    ```bash
    mv config/config.example.env config/config.env
    ```

3.  And now **run**:
    ```bash
    docker-compose --env-file config/config.env up --build
    ```
