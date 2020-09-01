#!/usr/bin/env python

from selenium import webdriver

from bs4 import BeautifulSoup as soup

import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

# Chrome Driver
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.maximize_window()

# All users you want to view
user_list = ["gordon003"]

for user in user_list:

	# Access user art gallery
	driver.get("https://www.deviantart.com/" + user + "/gallery/all")

	# All arts info
	arts_list = []

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

			# Title
			title = container.h2.text

			# Favourite
			favourite = container.find("button", {"aria-label": "Favourite"}).text.replace("Favourites","")

			# Comment
			comment = container.find("a", {"aria-label": "Comment"}).text.replace("Comments","")

			# Link
			link = container.a["href"]

			# If new, add to art_list
			if [title, favourite, comment, link] not in arts_list:
				arts_list.append([title, favourite, comment, link])
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

	print("Founded " + str(len(arts_list)) + " Artworks")

	# Open File
	filename = user + "_1.csv"
	f = open(filename, "w")

	# Write Header
	headers = "Title,Favourites,Comments, Link\n"
	f.write(headers)

	# Write all art records
	for art in arts_list:
		title, favourite, comment, link = art
		f.write(title.replace(",", "|") + "," + favourite + "," + comment + "," + link + "\n")

	# Close file
	f.close()

# Close driver
driver.quit()