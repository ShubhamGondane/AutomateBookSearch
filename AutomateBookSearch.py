from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
from tqdm import tqdm 
from selenium.common.exceptions import NoSuchElementException
import traceback
from SendEmail import sendEmail
from GoodreadsDriver import getToRead

input_list_path = '/Users/shubhamgondane/Automation/books.txt'
abebooks_url = 'https://www.abebooks.com/'
thriftbooks_url = 'https://www.thriftbooks.com/'

def writeLogs(error_message, stack_trace):
	# print the error message and stack and see if that's what you want to log
	# print (error_message + '\n' + stack_trace)
	# if it is, add it to your outfile how you want to record it
	with open('/Users/shubhamgondane/Automation/selenium_browser.log', 'a') as outfile:
		outfile.write(error_message + '\n' + stack_trace)

opts = Options()
opts.set_headless()
assert opts.headless  # Operating in headless mode
browser = Firefox(options=opts)

def getBookPriceThriftBooks(book_title):
	try:
		browser.get(thriftbooks_url)
		time.sleep(2)

		search_element = browser.find_element_by_xpath('//*[@id="GlobalSearch"]/div/input')
		search_element.send_keys(book_title)

		search_button = browser.find_element_by_xpath('//*[@id="GlobalSearch"]/div/div/button')
		search_button.click()

		filter_button = browser.find_element_by_class_name("AllEditions-refine-button AllEditions-grow is-link")
		filter_button.click()

		hide_out_of_stock = browser.find_element_by_name("Hide Out of Stock")
		hide_out_of_stock.click()

		apply_filters = browser.find_element_by_class_name("NewButton AllEditions-apply-button")
		apply_filters.click()

		time.sleep(1)

		sort_button = browser.find_element_by_class_name("AllEditions-Sort-OptionsContainer")
		sort_button.click()

		sort_items = browser.find_element_by_class_name("AllEditions-Sort-Options")
		sort_items[3].click()

	except NoSuchElementException as e:
		# browser.close()
		print("NoSuchElementException")

def getBookPriceAbeBooks(book_title, book_author):
	total_price = float("inf")
	link = ""
	try:
		browser.get(abebooks_url)
		time.sleep(2)
		author_inputElement = browser.find_element_by_id("hp-search-author")
		author_inputElement.send_keys(book_author)

		title_inputElement = browser.find_element_by_id("hp-search-title")
		title_inputElement.send_keys(book_title)

		# Submit button
		submit_button = browser.find_element_by_id("hp-search-find-book")
		submit_button.click()

		first_item = browser.find_element_by_id("book-1")
		book_link = first_item.find_element_by_css_selector('a')
		
		book_link.click()
		time.sleep(2)
		link = browser.current_url
		# print(link)
		price_text = browser.find_element_by_class_name("basket-price").text
		price_text = price_text.split("\n")
		book_price = price_text[0].split(" ")[1]
		# print(book_price)
		shipping_text = browser.find_element_by_class_name("basket-shipping").text
		shipping_text = shipping_text.split("\n")
		shipping_price = shipping_text[0].split(" ")[-1]
		# print(shipping_price)

		total_price = float(book_price) + float(shipping_price)
	except NoSuchElementException as e:
		print("NoSuchElementException")
		error_message = str(e)
		stack_trace = str(traceback.format_exc())
		write_logs(error_message, stack_trace)
		print("Error found for: " + book_title)
	finally:
		return total_price, link

def getTopThree(books):
	prices = []
	for title, author in tqdm(books):
		price,link = getBookPriceAbeBooks(title, author)
		time.sleep(10)
		prices.append([title, author, price, link])

	browser.close()
	prices.sort(key = lambda x: x[2])
	return prices[:3]

def getInputBooks(inputFile):
	file = open(inputFile)
	books = []
	for line in file.readlines():
		title, author = line.strip().split("\t")
		books.append([title, author])
	return books

def displayTopThree(top_three):
	for book in top_three:
		print(book[0] + ": %.2f" % book[2])


books = getToRead()

top_three = getTopThree(books)

displayTopThree(top_three)
sendEmail(top_three)












