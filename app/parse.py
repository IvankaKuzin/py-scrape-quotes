from dataclasses import dataclass
from bs4 import BeautifulSoup, ResultSet
import requests

HOME_URL = "https://quotes.toscrape.com/"
PAGE_URL = "page/{page_number}/"


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


def main(output_csv_path: str) -> None:
    request = requests.get(HOME_URL)
    soup = BeautifulSoup(request.content, "html.parser")
    quotes = soup.find_all("div", attrs={"class": "quote"})
    print(f"Found {len(quotes)} quotes")

    print(get_quotes_data(quotes))


if __name__ == "__main__":
    main("quotes.csv")
