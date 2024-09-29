import schedule
import time
import telegram_bot


def activate_bot() -> None:
    """
    this function activates the bot -> runs the main function of it.
    :return: None.
    """
    telegram_bot.bot.send_scraping()


def run_automation() -> None:
    """
    this function runs the activate_bot function every day at 10:00[AM] automatically.
    :return: None.
    """
    schedule.every().day.at('10:00').do(activate_bot)
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # wait for 1 minute before checking again


def main():
    run_automation()


if __name__ == '__main__':
    main()
