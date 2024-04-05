import scrapy
from scrapy.selector import Selector
from selenium import webdriver
import pandas as pd
import time


class AudiblelibSpider(scrapy.Spider):
	name = 'audiblelib2'
	allowed_domains = ['toscrape.com']
	start_urls = ['http://audible.com/']
	"""
	import csv
	csvfile = open('library.csv', 'w', newline="")
	writer = csv.writer(csvfile)
	writer.writerow(['title', 'authors', 'narrators'])
	"""
	web = 'https://www.audible.com/library/titles'
	path = 'D:/webScrappingAndrade/chromedriver/chromedriver.exe'
	print("Starting from class AudublelibSpider")

	def start_requests(self):
		print("in start_request")
		url = "http://quotes.toscrape.com"
		# yield scrapy.Request(url='https://www.audible.com/search/', callback=self.parse,
		yield scrapy.Request(url=url, callback=self.parse_books)
		# headers={'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'})

		print("End start_request")

	def parse_books(self, response):
		print(f"In parse with responce: {response}")
		booksDic = []
		authorsDic = []
		narratorsDic = []

		driver = webdriver.Chrome(self.path)
		print(f'driver is ***+ {driver} ****+ \n')
		driver.get(self.web)
		driver.maximize_window()
		print("****Sleeping***")
		time.sleep(5 * 60)
		print("Awake")

		import csv
		csvfile = open('audible23.csv', 'w', newline='')
		writer = csv.writer(csvfile)
		writer.writerow(['title', 'authors', 'narrators'])

		# Hand-off between Selenium and Scrapy happens here
		# sel = Selector(text=driver.page_source)
		# Pagination
		pagination = driver.find_element_by_xpath(
			'//ul[contains(@class, "pagingElements")]')  # locating pagination bar
		pages = pagination.find_elements_by_tag_name('li')  # locating each page displayed in the pagination bar
		last_page = int(
			pages[-2].text)  # getting the last page with negative indexing (starts from where the array ends)
		print(f'last page:{last_page}')

		current_page = 1  # this is the page the bot starts scraping
		while current_page <=  last_page:

			time.sleep(3)  # let the page render correctly
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

				print(f'authors: {authors}')
				#authors.append(authorsDic)
				narrators = product.xpath('.//li/span[contains(@class, "narratorLabel")]/a/text()').getall()

				print(f'narrators: {narrators}')
				#narrators.append(narratorsDic)

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
				time.sleep(2)
			# End for loop

			current_page = current_page + 1  # increment the current_page by 1 after the data is extracted
			# Locating the next_page button and clicking on it. If the element isn't on the website, pass to the next iteration
			try:
				next_page = driver.find_element_by_xpath('.//span[contains(@class , "nextButton")]')
				print(f'** next_page:(** {next_page} ')
				if next_page:
					print(f'***************** nextpage to be clicked: {next_page}')
					next_page.click()
			except:
				print("** an exception has been raised about next page **")
		# End while loop
		# print("close cvsfile")
		csvfile.close()
