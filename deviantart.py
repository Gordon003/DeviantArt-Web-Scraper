#!/usr/bin/env python
from selenium import webdriver

from bs4 import BeautifulSoup as soup

from urllib.request import urlopen as uReq

import time

import codecs

from selenium.webdriver.common.keys import Keys

import urllib.request

# Chrome Driver
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.maximize_window()

# Specific user
user = "gaby-sunflower"
#user = "astral-btlm"
#user = "mother-of-trolls"
#user = "sagraphics1997"

# Access its main folder
driver.get("https://www.deviantart.com/" + user + "/gallery/all")

# All artworks link
all_artwork_link_list = []

# Wait for it to load
time.sleep(1)

# Scroll through each row
while True:

	# Parse HTML
	page_soup = soup(driver.page_source, "html.parser")

	# Get all container
	containers = page_soup.findAll("div", {"class": "bPSGi"})

	# If no row, terminate loop
	if len(containers) == 0: break

	# Go thru all rows
	# NEW - If any new artworks in all row if found
	NEW = False
	for container in containers:

		# Get all image in each row
		curr_artworks_container = container.findAll("span", {"class": "_1TFfi"})

		# If no image, then move to next row
		if len(curr_artworks_container) == 0:
			continue

		# Add new art links to list
		# NEW2 - If any artwork in a row is found
		NEW2 = False
		for art_container in curr_artworks_container:
			art_link = art_container.a["href"]
			if art_link not in all_artwork_link_list:
				all_artwork_link_list.append(art_link)
				NEW2 = True

		# If no new links, move on to next row
		if NEW2 == False:
			continue

		# If has new links, move page to that element
		NEW = True
		last_artwork_link = "//a[@href='" + curr_artworks_container[-1].a["href"] + "']"
		curr_last_artwork_element = driver.find_element_by_xpath(last_artwork_link)
		driver.execute_script("arguments[0].scrollIntoView();", curr_last_artwork_element)
		break

	# If all artworks are accessed and added, terminate loop
	if NEW == False:
		break

	# Wait for page to load
	time.sleep(1)

# Close driver
driver.quit()

# Write to csv
print("Start Writing")

# Open new files
filename = user + ".csv"
f = open(filename, "w")
headers = "Title,Date,Favourites,Comments,Views\n"
f.write(headers)

# Go thru each links
for link in all_artwork_link_list:

	# Grab HTML page
	#uClient = uReq(link)
	#page_html = uClient.read()
	#uClient.close()

	try:
		page=urllib.request.Request(link,headers={'User-Agent': 'Mozilla/5.0'}) 
		infile=urllib.request.urlopen(page).read()
		page_html = infile.decode('ISO-8859-1') # Read the content as string decoded with ISO-8859-1
	except:
		print("Fail request")
		continue


	# HTML parsing
	page_soup = soup(page_html, "html.parser")

	# Get title
	title = page_soup.h1.text

	print(title)

	# Get amount of favs and comments
	containers = page_soup.findAll("span", {"class": "_3USIK _1nd-h"})
	if len(containers) >= 2:
		favourite = containers[0].text.split()[0]
		comment = containers[1].text.split()[0]
	else:
		print("Fail")
		favourite = 'NULL'
		comment = 'NULL'

	# Get amount of views
	try:
		containers = page_soup.findAll("span", {"class": "_1qE63"})
		view = containers[0].text.split()[0]
		if (view[-1] == 'K'):
			view = str(int(view[:-1]) * 1000)
	except:
		view = 'NULL'

	# Get date
	try:
		containers = page_soup.findAll("div", {"class": "_1TgrW _330_U"})
		container = containers[0]
		art_date = container.time["aria-label"].replace(",", "").split()[:3]
		art_date = str(' '.join(art_date))
	except:
		view = 'NULL'

	# Write to file
	f.write(title.replace(",", "|") + "," + art_date + "," + favourite + "," + comment + "," + view + "\n")

# Close file
f.close()