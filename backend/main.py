from app.settings.settings import get_settings


def main():
    print("Hello from backend!")


if __name__ == "__main__":
    settings = get_settings()
    print(f"Database URL: {settings.DATABASE_URL}")
    print(f"Redis URL: {settings.REDIS_URL}")
    print(f"Telegram Bot Token: {settings.TELEGRAM_BOT_TOKEN}")
    print(f"Telegram API URL: {settings.TELEGRAM_API_URL}")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"Storage Chat ID: {settings.STORAGE_CHAT_ID}")
    main()
