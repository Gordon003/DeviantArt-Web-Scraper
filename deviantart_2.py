#!/usr/bin/env python

from bs4 import BeautifulSoup as soup

from urllib.request import urlopen as uReq
import urllib.request

import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome Driver
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.maximize_window()

# All users you want to view
user_list = ["gordon003"]
tags_list = ["totaldrama"]

for user in user_list:

	# Access user art gallery
	driver.get("https://www.deviantart.com/" + user + "/gallery/all")

	# All arts info
	arts_link_list = []

	# Wait page to be loaded
	try:
	    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'bPSGi')))
	    print("Page is ready!\n")
	except:
		print("Loading took too much time!")

	# Scroll through all row
	while True:

		# Parse HTML
		page_soup = soup(driver.page_source, "html.parser")

		new_artwork = None

		# Access script and scrap essential art info
		script_containers = page_soup.findAll("section", {"data-hook": "deviation_std_thumb"})

		# Access each art
		for container in script_containers:

			# Link
			link = container.a["href"]

			# If new, add to art_list
			if link not in arts_link_list:
				arts_link_list.append(link)
				new_artwork = link


		# Check new artworks have been found
		try:
			assert new_artwork is not None
			last_artwork_link = "//a[@href='" + new_artwork + "']"
		except:
			break

		# Go to last artwork
		last_artwork_element = driver.find_element_by_xpath(last_artwork_link)
		driver.execute_script("arguments[0].scrollIntoView();", last_artwork_element)

		# Wait for page to load
		time.sleep(1)

	print("Founded " + str(len(arts_link_list)) + " Artworks")

	# Open new files
	filename = user + "_2.csv"
	f = open(filename, "w")
	headers = "Title,Date,Favourites,Comments,Views,Link\n"
	f.write(headers)

	# Go thru each links
	for link in arts_link_list:

		# Grab HTML page
		while True:
			try:
				uClient = uReq(link)
				time.sleep(1)
				page_html = uClient.read()
				uClient.close()
				break
			except:
				print("Can't access. Wait")
				time.sleep(20)

		# HTML parsing
		page_soup = soup(page_html, "html.parser")

		# Tags
		containers = page_soup.findAll('a', {"class": "j9kGS"})
		art_tags = [container.text for container in containers]

		check1 = True
		for tag in tags_list:
			if tag not in art_tags:
				check1 = False

		if check1 == False:
			continue

		# Get title
		title = page_soup.h1.text
		print(title)

		# Get favourites and comments
		containers = page_soup.findAll("span", {"class": "_3USIK _1nd-h"})
		favourite = containers[0].text.split()[0]
		try:
			comment = containers[1].text.split()[0]
		except:
			comment = '0'

		# Get view
		container = page_soup.find('span', class_='_3jmcd')
		view = container.text.split()[0]
		if (view[-1] == 'K'):
			view = str(int(view[:-1]) * 1000)

		# Get date
		container = page_soup.findAll("div", {"class": "_1TgrW"})[0]
		art_year = container.time["aria-label"].replace(",", "").split()[2]

		# Write to file
		f.write(title.replace(",", "|") + "," + art_year + "," + favourite + "," + comment + "," + view + "," + link + "\n")

	# Close file
	f.close()

# Close driver
driver.quit()