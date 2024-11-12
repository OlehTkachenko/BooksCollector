import logging
import os
from typing import List

import pandas as pd
import requests
from lxml.html import HtmlElement, fromstring
from sqlalchemy import create_engine

logging.basicConfig(
    format="{asctime} - [{levelname}] - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,
)

SOURCE_TEMPLATE = "https://www.yakaboo.ua/ua/knigi/dobirki-yakaboo.html?p={number}"
PREFIX = "https://www.yakaboo.ua"
PAGE_NR = (
    9  # Code just for simulation scrapping proces, this value i decided to hardcode.
)


def connector(url: str) -> requests.Response:
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.ConnectTimeout:
        logging.critical(
            f"Sth went wrong Connection Timeout. Check if you can reach link: {url}"
        )
        raise

    response.encoding = "utf-8"

    return response


def get_book_links(url: str) -> List[str]:
    response = connector(url)

    if response.status_code != 200:
        logging.warning(f"Bad request {response.status_code} from page: {url}.")
        return []

    soup = fromstring(response.text)

    elements = soup.xpath(
        '//div[@class="product-listing view-category"]/div//a[@class="category-card__image"]'
    )

    links = []
    for element in elements:
        link = f"{PREFIX}{element.get('href')}"
        links.append(link)

    return links


def get_book_name(soup: HtmlElement) -> str:
    try:
        name = soup.xpath('//h1[@id="product-title"]')[0].text
    except IndexError:
        return "Not Found"
    name = name.strip()
    name = name.removeprefix("Книга ")
    return name


def get_book_author(soup: HtmlElement) -> str:
    try:
        author = soup.xpath('//a[@id="product-author"]')[0].text
    except IndexError:
        return "Author Unknown"

    author = author.strip()
    return author


def get_book_price(soup: HtmlElement) -> int:
    try:
        price = soup.xpath('//span[@id="product-price"]')[0].text
    except IndexError:
        return 0

    price = price.removesuffix(" грн")
    price = int(price)

    return price


def collector(all_links: List[str]) -> pd.DataFrame:

    records_num = len(all_links)

    df = pd.DataFrame(
        columns=["Urls", "Names", "Authors", "Prices"], index=range(records_num)
    )

    for i, url in enumerate(all_links):
        response = connector(url)

        if response.status_code != 200:
            logging.warning(
                f"Bad request {response.status_code} from page: {url}. Data cant be collected."
            )
            df.iloc[i] = [None, None, None, None]
            continue

        soup = fromstring(response.text)

        name = get_book_name(soup)
        author = get_book_author(soup)
        price = get_book_price(soup)

        df.iloc[i] = [url, name, author, price]
        logging.info(f"Succesfully added record nr: {i+1}")

    return df


def save_to_db(df: pd.DataFrame):
    password = os.environ.get("POSTGRES_PASSWORD")
    user = os.environ.get("POSTGRES_USER")
    db_name = os.environ.get("POSTGRES_DB")
    port = os.environ.get("POSTGRES_PORT")
    ip = os.environ.get("POSTGRES_IP")

    url = f"postgresql://{user}:{password}@{ip}:{port}/{db_name}"
    engine = create_engine(url)

    df.to_sql("books", engine)

    logging.info(f"Collector save {len(df.index)} rows in db.{url}")


def main():
    logging.info("Collector start working.")
    all_links = []

    for i in range(2, PAGE_NR):
        books_page = SOURCE_TEMPLATE.format(number=i)
        links = get_book_links(books_page)
        all_links.extend(links)

    df = collector(all_links)

    save_to_db(df)


if __name__ == "__main__":
    main()
