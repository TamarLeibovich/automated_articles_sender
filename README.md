# Automated Articles Sender

## Project's Background
This project was done in order to optimize the time spent on searching things up on the internet.
Many people visit the hackernews.com website in order to learn new things, and to stay updated of what's going on
in today's tech world. Instead of wasting time scrolling up and down, while seeing articles you've already read,
this automated articles sender sends you all new articles right to your pocket every morning.

## About The Project
> Web Scraping | Telegram Bot | Automation Scripting

- __Web Scraping__: Wrote a web-scraper using the `requests` & `BeautifulSoup` libraries.
- __Telegram Bot__: Wrote a telegram bot using the `telebot` telegram's api.
- __Automation Scripting__: Wrote an automation for activating the bot using the `schedule` library.

__This project sends you all new hackernews articles via telegram every morning at 10:00 AM.__
## How To Use?

> ___Prerequisite___: python needs to be installed. This project was written in python 3.12, which can 
be installed from [the official Python's website](https://www.python.org/downloads/) 

Clone the repository to your desired folder and perform the following steps:

### Step #1
Create a bot token via BotFather inside Telegram. Here's a simple guide:
- search for `@BotFather` inside your Telegram app. Then, enter the command `/newbot`.
- choose a name of your choosing for your bot (any name is acceptable).
- choose a username for your bot (you can only use usernames which have not been already taken).
- start the chat with your new bot by clicking the provided link BotFather gives you, and __copy the token
to the `.env` file, in between quotation marks. e.g. `TOKEN = 'your token here'`__

### Step #2
Run the following command (change the `path_to` to your own path in which you cloned the repository to):
```commandline
pip install -r path_to\automated_articles_sender\requirements.txt
```

### Step #3
Run the `telegram_bot.py` file.

### Step #4
Through the Telegram App, send the message `/start`. This command will save your chat identifier
in a `.env` file.

### Step #5
terminate the `telegram_bot.py` script and run the following command:
```commandline
pythonw.exe path_to\automated_articles_sender\implementation\automation.pyw
```
This will start the automation in a hidden manner for convenience. i.e., no console window.

> ___Note___: re-run `pythonw.exe path_to\automated_articles_sender\implementation\automation.pyw` whenever 
re-booting your machine.
*** 
### Thanks For Reading!
