import json
from random import randint

import selenium.webdriver.remote.webelement
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


def create_driver() -> webdriver.Chrome:
    """
    Create web driver object
    :return: object web driver
    """
    return webdriver.Chrome()


def parse_book_data(book: webdriver.remote.webelement.WebElement) -> dict:
    """
    Parsing web element from book
    :param book:
    :return: dict book data
    """
    mark_dict = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
    full_title = book.find_element(By.CSS_SELECTOR, "h3 > a").get_attribute("title")
    book_url = book.find_element(By.CSS_SELECTOR, "h3 > a").get_attribute("href")
    book_cover = book.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
    book_price = float(book.find_element(By.CSS_SELECTOR, "p.price_color").text.lstrip('£'))
    book_availability_classes = book.find_element(By.CSS_SELECTOR, "p.instock").get_attribute(
        "class")
    book_availability = True if "availability" in book_availability_classes.lower() else False
    str_mark = (
        book.find_element(By.CSS_SELECTOR, "p.star-rating")  # star-rating One
        .get_attribute("class")
        .split(" ")[1]
    )
    mark = mark_dict[str_mark]
    return {
        "full_title": full_title,
        "book_url": book_url,
        "book_cover": book_cover,
        "book_price": book_price,
        "book_availability": book_availability,
        "book_rating": mark,
    }


def parse_page(driver: webdriver.Chrome, url: str) -> list[dict]:
    """
    Get page from url
    :param driver: browser driver
    :param url: url
    :return: list dict data from page
    """
    result: list[dict] = list()
    # get page
    driver.get(url)
    # search by class name
    books = driver.find_elements(By.CLASS_NAME, "product_pod")
    for book in books:
        result.append(parse_book_data(book))
    return result


def save_data(data: list[dict], filename: str) -> None:
    """
    Function save json data to file
    :param data: list dict data
    :param filename: filename
    :return: None
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as error_info:
        print('error', error_info)


def main():
    driver = create_driver()
    full_list = list()
    for i in range(1, 51):
        url = f'https://books.toscrape.com/catalogue/page-{i}.html'
        data_page = parse_page(driver, url)
        full_list.extend(data_page)
        sleep(randint(0, 2))
    save_data(full_list, 'books_data.json')
    driver.quit()


if __name__ == '__main__':
    main()
