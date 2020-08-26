#!/usr/bin/env python
from selenium import webdriver

from bs4 import BeautifulSoup as soup

import time

from selenium.webdriver.common.keys import Keys

# Chrome Driver
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.maximize_window()

# Specific user
#user = "gordon003"
#user = "astral-btlm"
#user = "mother-of-trolls"
#user = "sagraphics1997"
#user = "gaby-sunflower"
user = "blueparadicey"

# Access its main folder
driver.get("https://www.deviantart.com/" + user + "/gallery/all")

# All arts list
all_arts_list = []

# Wait for it to load
time.sleep(1)

# Last artworks
last_artwork = None

# Scroll through all row
while True:

	# Parse HTML
	page_soup = soup(driver.page_source, "html.parser")

	# Get all rows
	containers = page_soup.findAll("div", {"class": "bPSGi"})

	# If no row, terminate loop
	if len(containers) == 0: break

	# Get last available row
	last_container = containers[-1]

	# Access script and scrap essential art info
	containers2 = page_soup.findAll("section", {"data-hook": "deviation_std_thumb"})
	for container2 in containers2:

		# Title
		title = container2.h2.text

		# Favourite
		container_2 = container2.find("button", {"aria-label": "Favourite"})
		favourite = container_2.text.replace("Favourites","")

		# Comment
		container_2 = container2.find("a", {"aria-label": "Comment"})
		comment = container_2.text.replace("Comments","")

		# If new, add to art_list
		if [title, favourite, comment] not in all_arts_list:
			all_arts_list.append([title, favourite, comment])


	# Get last available artwork and start from there
	curr_artworks_container = last_container.findAll("span", {"class": "_1TFfi"})
	curr_last_artwork = curr_artworks_container[-1].a["href"]
	curr_last_artwork_link = "//a[@href='" + curr_last_artwork + "']"

	# If same last artwork, we have reach the limit
	if last_artwork is None or last_artwork != curr_last_artwork:
		last_artwork = curr_last_artwork
	else:
		break 

	# If different artwork, scroll to that artwork
	curr_last_artwork_element = driver.find_element_by_xpath(curr_last_artwork_link)
	driver.execute_script("arguments[0].scrollIntoView();", curr_last_artwork_element)


	# Wait for page to load
	time.sleep(1)

# Open File
filename = user + ".csv"
f = open(filename, "w")

# Write Header
headers = "Title,Favourites,Comments\n"
f.write(headers)

# Write all art records
for art in all_arts_list:
	title, favourite, comment = art
	print(title)
	# Write to file
	f.write(title.replace(",", "|") + "," + favourite + "," + comment + "\n")

# Close file
f.close()

# Close driver
driver.quit()