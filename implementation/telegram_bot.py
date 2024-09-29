import telebot
import os
from dotenv import load_dotenv
import web_scraper
import modify_scraping_results

load_dotenv()


class Singleton(type):
    """
    taken from the following resource: https://refactoring.guru/design-patterns/singleton/python/example.
    Added the Singleton design pattern to make sure no more than 1 Bot instance is created.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]


class Bot(metaclass=Singleton):
    def __init__(self) -> None:
        self.token = os.getenv('TOKEN')  # retrieve the bot`s token from the .env file.
        assert self.token, 'Error: token is None'  # throw an error if self.token = None

        try:
            self.bot = telebot.TeleBot(self.token)

        except Exception as e:
            print('Could not connect to telegram bot via token. Error:', e)
            exit()

    @staticmethod
    def retrieve_chat_id() -> int:
        """
        this function retrieves the chat_id from the .env file.
        :return: the chat's ID
        """
        chat_id = os.getenv('CHAT_ID')
        assert chat_id, 'Error: chat_id is None'  # throw an error if chat_id = None

        try:
            return int(chat_id)

        except Exception as e:
            print('could not convert chat_id to int. Error:', e)
            exit()

    def send_scraping(self) -> None:
        """
        this function sends the final scraping results to the user, while parsing to messages of 4096 characters
        length each (telegram doesn't allow longer messages to be sent).
        :return: None.
        """
        articles_message = modify_scraping_results.main(web_scraper.main())
        max_length = 4096
        chat_id = Bot.retrieve_chat_id()

        for i in range(0, len(articles_message), max_length):
            self.bot.send_message(chat_id, articles_message[i:i+max_length])


bot = Bot()  # creating the bot as a global variable to get recognition inside decorators.


def check_valid_parameter_message(message: telebot.types.Message) -> None:
    """
    this function raises an error if parameter's type is not telebot.types.Message
    :param message: expected type of telebot.types.Message
    :return: None.
    """
    if not isinstance(message, telebot.types.Message):
        raise ValueError('Parameter message must be an instance of telebot.types.Message')


@bot.bot.message_handler(commands=['start'])
def write_chat_id(message: telebot.types.Message) -> None:
    """
    this function receives a message from the user and permanently writes his/her chat id into an .env file, if not
    included already.
    :param message: the message received from the user ('/start').
    :return: None.
    """
    check_valid_parameter_message(message)

    with open('.env', 'a+') as env_file:  # a+ for appending and reading.
        env_file.seek(0)  # append sets the env_file pointer to the end of the file by default, so moving to start.

        if 'CHAT_ID' not in env_file.read():  # write CHAT_ID only if not included already in env_file.
            env_file.write(f'\nCHAT_ID={message.chat.id}\n')


def main():
    bot.bot.infinity_polling()


if __name__ == '__main__':
    main()
