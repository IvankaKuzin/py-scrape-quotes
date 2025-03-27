from dataclasses import dataclass
from bs4 import BeautifulSoup, ResultSet
import requests


HOME_URL = "https://quotes.toscrape.com/page/{page_number}/"


@dataclass
class Quote:
    text: str
    author: str
    tags: list[str]


def get_quotes_data(quotes: ResultSet) -> list[Quote]:
    quotes_inform = [
        Quote(
            text=quote.select_one(".text").text,
            author=quote.select_one("small.author").text,
            tags=[
                tag.get_text()
                for tag in quote.find_all("a", attrs={"class": "tag"})
            ],
        )
        for quote in quotes
    ]
    return quotes_inform


def get_quotes_from_pages() -> list[Quote]:
    counter = 1
    all_quotes_from_page = []

    while True:
        page = requests.get(HOME_URL.format(page_number=counter))
        if page.status_code != 200 or counter > 10:
            return all_quotes_from_page

        print("Scraping page", counter)
        soup = BeautifulSoup(page.content, "html.parser")
        quotes = soup.find_all("div", attrs={"class": "quote"})
        all_quotes_from_page.extend(get_quotes_data(quotes))
        counter += 1


def main(output_csv_path: str) -> list | None:
    pass


if __name__ == "__main__":
    print(main("quotes.csv"))
    print(len(main("quotes.csv")))
