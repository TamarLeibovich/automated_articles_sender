"""
this file contains all functions which handles the only-one-instance of an article to be sent to the user via the bot.
"""
import web_scraper

articles_message = ''  # the final message to be sent to the user.


def check_valid_str_parameter(parameter: str) -> None:
    """
    this function raises an error if parameter's type is not str.
    :param parameter: supposed to be type of str.
    :return: None.
    """
    if not isinstance(parameter, str):
        raise ValueError('Parameter must be an instance of str')


def is_existing(article: str) -> bool:
    """
    this function checks whether an article is already existing in the database. If so, return True. Otherwise,
    return False.
    :param article: a string containing the article.
    :return: a boolean value which indicates whether the article exists in the database or not.
    """
    check_valid_str_parameter(article)

    with open('database.txt', 'r', encoding='utf-8') as database_file:
        if article in database_file.read():
            return True

    return False


def add_to_database() -> None:
    """
    this function adds the global variable articles_message to the database.
    :return: None.
    """
    global articles_message

    with open('database.txt', 'a', encoding='utf-8') as database_file:
        database_file.write(f'\n{articles_message}')


def run_execution(scraping_results: str) -> None:
    """
    this function is responsible for executing the program's workflow.
    iterate through all scraping results -> if result not in database, add to articles_message.
    :param: scraping_results: the web-scraping results.
    :return: None.
    """
    global articles_message

    for article in scraping_results.split('\n'):
        if not is_existing(article):
            articles_message += f'{article}\n'

    add_to_database()


def main(scraping_results: str) -> str:
    """
    this function resets the global variable articles_message and then runs the run_execution function.
    Returns the articles_message global variable.
    :param scraping_results: the web-scraping results.
    :return: a string containing only the articles which have never been sent to the user.
    """
    global articles_message
    
    #reset global variable
    articles_message = ''
    
    check_valid_str_parameter(scraping_results)

    run_execution(scraping_results)

    return articles_message


if __name__ == '__main__':
    main(web_scraper.main())
