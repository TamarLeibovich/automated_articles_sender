import bs4
import requests
from bs4 import BeautifulSoup

url = 'https://news.ycombinator.com/?p='  # hackernews url. page number is missing, adding at runtime.
title_and_link = {}  # a dictionary containing title & link to article. [title:link]
end_of_pages = False
page_number = 1


def check_valid_parameter_a_tag(a_tag: bs4.element.Tag) -> None:
    """
    this function raises an error if parameter's type is not bs4.element.Tag.
    :param a_tag: supposed to be type of bs4.element.Tag.
    :return: None.
    """
    if not isinstance(a_tag, bs4.element.Tag):
        raise ValueError('Parameter a_tag must be an instance of bs4.element.Tag')


def check_valid_parameter_html_parsed(html_parsed: bs4.BeautifulSoup) -> None:
    """
    this function raises an error if parameter's type is not bs4.BeautifulSoup.
    :param html_parsed: supposed to be type of bs4.BeautifulSoup.
    :return: None.
    """
    if not isinstance(html_parsed, bs4.BeautifulSoup):
        raise ValueError('Parameter html_parsed must be an instance of bs4.BeautifulSoup')


def check_valid_parameter_request_response(request_response: requests.models.Response) -> None:
    """
    this function raises an error if parameter's type is not requests.models.Response.
    :param request_response: supposed to be type of requests.models.Response.
    :return: None.
    """
    if not isinstance(request_response, requests.models.Response):
        raise ValueError('Parameter request_response must be an instance of requests.models.Response')


def send_request() -> requests.models.Response:
    """
    this function sends a http request to the URL.
    :return: the http response.
    """
    global page_number

    request_response = requests.get(f'{url}{page_number}')
    assert (request_response.status_code == 200), 'Error while requesting the url'  # check whether error has occurred

    return request_response


def attach_to_dict(a_tag: bs4.element.Tag) -> None:
    """
    this function appends a new title:link object to the title_and_link dict.
    :param a_tag: an 'a' tag containing the text and link.
    :return: None.
    """
    global title_and_link

    check_valid_parameter_a_tag(a_tag)

    title_and_link[a_tag.text] = a_tag['href']


def is_last_page(html_parsed: bs4.BeautifulSoup) -> None:
    """
    this function checks whether there is a next page or not. If not, modifies the end_of_file variable to True.
    :param html_parsed: the html code from which we'd retrieve the data.
    :return: None.
    """
    global end_of_pages

    check_valid_parameter_html_parsed(html_parsed)

    more_link = html_parsed.find('a', string='More')

    if not more_link:  # if there isn't a More link, it's the end of the file.
        end_of_pages = True


def get_articles(html_parsed: bs4.BeautifulSoup) -> None:
    """
    this function retrieves all articles' titles and links, and appends them to a dict.
    :param html_parsed: the html code from which we'd retrieve the data.
    :return: None.
    """
    check_valid_parameter_html_parsed(html_parsed)

    """
    in hackernews website, all articles are bounded in a span tag whom class is titleline. The title is linked to a 
    link which leads to the article itself. Thus, we find all items regarded these conditions: get all span tags 
    classed as titleline -> for all spans extract its bounded `a` tag -> attach `a` tag href (link) and 
    text to the dict.
    """
    span_tags = html_parsed.find_all('span', class_='titleline')

    for span_tag in span_tags:
        a_tag = span_tag.find('a')

        if a_tag:
            attach_to_dict(a_tag)

    is_last_page(html_parsed)


def parse_html(request_response: requests.models.Response) -> bs4.BeautifulSoup:
    """
    this function parses http response to html.
    :param request_response: the response to the retrieve request.
    :return: the http response parsed as html code.
    """
    check_valid_parameter_request_response(request_response)

    html_parsed = BeautifulSoup(request_response.content, 'html.parser')

    return html_parsed


def convert_dict_to_str() -> str:
    """
    this function converts the title_and_link dictionary to a string.
    :return: title_and_link dict as a string.
    """
    global title_and_link

    result = ''

    for title, link in title_and_link.items():
        result += f'{title}: {link}\n'

    return result


def run_execution() -> None:
    """
    this function is responsible to run the execution flow and connect all methods to a working script.
    Execution Flow: send a http request to the url -> parse the response as html -> retrieve articles -> increment
    the page number by 1.
    :return: None.
    """
    global page_number

    request_response = send_request()
    html_parsed = parse_html(request_response)
    get_articles(html_parsed)
    page_number += 1
    

def main() -> str:
    """
    this main function resets all relevant global variables, and then calls the web scraper's 
    execution flow function run_execution until end of pages. Returns the title:link dictionary content as a string.
    :return: the title_and_link contents as a string.
    """
    global end_of_pages, page_number, title_and_link

    # resetting global variables
    title_and_link = {}
    end_of_pages = False
    page_number = 1
    
    while not end_of_pages:
        run_execution()

    return convert_dict_to_str()


if __name__ == '__main__':
    main()
