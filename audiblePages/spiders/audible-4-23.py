import scrapy
from scrapy.selector import Selector
import pandas as pd
import time

from selenium import webdriver
# from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
start_url = 'http://audible.com/library/titles/?pageSize=50'


class AudiblelibSpider(scrapy.Spider):
    name = 'audiblelib2'
    allowed_domains = ['toscrape.com']
    """
    import csv
    csvfile = open('library.csv', 'w', newline="")
    writer = csv.writer(csvfile)
    writer.writerow(['title', 'authors', 'narrators'])
    """
    web = 'https://www.audible.com/library/titles'

    print("Starting from class AudublelibSpider")

    def start_requests(self):
        print("in start_request")
        url = "https://quotes.toscrape.com"
        # yield scrapy.Request(url='https://www.audible.com/search/', callback=self.parse,
        yield scrapy.Request(url=url, callback=self.parse_books)

        print("End start_request")

    def parse_books(self, response):
        print(f"In parse_books with response:")  # {response}")
        booksDic = []
        authorsDic = []
        narratorsDic = []
        print("now for the correct driver")

        driver.get(self.web)
        driver.maximize_window()
        print("****Sleeping***")
        time.sleep(5 * 60)
        print("Awake")

        import csv
        csvfile = open('Xaudible24 .csv', 'w', newline='')
        writer = csv.writer(csvfile)
        writer.writerow(['title', 'authors', 'narrators'])

        # Hand-off between Selenium and Scrapy happens here
        # sel = Selector(text=driver.page_source)
        # Pagination
        print("Now to get pagination")
        # pagination = driver.find_element(By.XPATH,
        # # pages = pagination.find_elements_by_tag_name('li')  # locating each page displayed in the pagination bar
        # pages = pagination.find_elements(By.TAG_NAME, 'li')
        #
        # print(f'pages: {pages}')
        # last_page = int(
        #     pages[-2].text)  # getting the last page with negative indexing (starts from where the array ends)

        last_page = 3

        print(f'last page:{last_page}')
        current_page = 1  # this is the page the bot starts scraping

        while current_page <= last_page:
            driver.get(f"{start_url}&page={current_page}")
            time.sleep(2 * 60)  # let the page render correctly
            sel = Selector(text=driver.page_source)
            product_container = sel.xpath(
                '//div[contains(@class, "bc-container")  and @id ="adbl-library-content-main"]//ul')
            # Looping through each product listed in the product_container box
            for product in product_container:
                book_title = product.xpath('.//span[contains(@class, "bc-size-headline3")]/text()').get()
                book_title = book_title.strip()
                print(f'book: {book_title}')

                authorsDic.clear()
                narratorsDic.clear()

                authors = product.xpath('.//li/span[contains(@class, "authorLabel")]/a/text()').getall()

                # print(f'authoers: {authors}')
                # authors.append(authorsDic)
                narrators = product.xpath('.//li/span[contains(@class, "narratorLabel")]/a/text()').getall()

                # print(f'narrators: {narrators}')
                # narrators.append(narratorsDic)

                # Return data extracted and also the user-agent defined before
                # print(f'write book {book_title} to file')
                # self.writer.writerow([book_title, authorsDic, narratorsDic])

                """
                import csv
                with open('abc.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['title', 'authors', 'narrators'])
                    writer.writerow(['abc', [], []])

                print("before yield")
                yield {
                    'title': book_title,
                    'author': authorsDic,
                    'narrator': narratorsDic, }
                """
                field = [book_title, authors, narrators]
                writer.writerow(field)
                time.sleep(3)
            # End of product  for loop

            current_page = current_page + 1  # increment the current_page by 1 after the data is extracted

        print('bottom of while loop')
        # End while loop
        print("close cvsfile")
        csvfile.close()
