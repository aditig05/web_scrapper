import requests
from bs4 import BeautifulSoup
import csv

# Open the CSV file outside the function
with open('output/out_book.csv', 'w', newline='') as myFile:
    writer = csv.writer(myFile, delimiter=";")
    header = ["Name", "URL", "Author", "Price", "Number of Ratings", "Average Rating"]
    writer.writerow(header)

def dv_spider(max_pages):
    for i in range(1, max_pages + 1):
        url = f'https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref=zg_bs_pg_1?_encoding=UTF8&pg={i}&ajax=1'
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        lower = 'https://www.amazon.com'

        with open('output/out_book.csv', 'a', newline='') as myFile:
            writer = csv.writer(myFile, delimiter=";")
            for containers in soup.findAll('div', 'zg_itemWrapper'):
                link = containers.find('a', 'a-link-normal')
                linkk = "".join([lower, link.get('href')]) if link else "Not available"

                text = containers.find('div', 'p13n-sc-truncate p13n-sc-line-clamp-1')
                title = " ".join(text.get_text().strip().split()) if text else "Not available"

                contain = containers.find('div', 'a-section a-spacing-none p13n-asin')
                name = contain.find('a', 'a-size-small a-link-child')
                name1 = contain.find('span', 'a-size-small a-color-base')
                author = name.string if name else (name1.string if name1 else "Not available")

                contain = containers.find('span', 'p13n-sc-price')
                price = contain.text.strip('\xa0').strip() if contain else "Not available"

                link = containers.find('a', 'a-size-small a-link-normal')
                nrating = link.string if link else "Not available"

                links = containers.find('div', 'a-icon-row a-spacing-none')
                link = links.find('span', 'a-icon-alt') if links else None
                avgrating = link.string if link else "Not available"

                row = [title, linkk, author, price, nrating, avgrating]
                writer.writerow(row)

dv_spider(5)
