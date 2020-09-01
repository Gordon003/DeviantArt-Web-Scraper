# DeviantArt-Web-Scraper
This little web scraper allow you to go through all possible artworks from your favourite artist and get its stats and links without core membership.

There are 2 different version:
* _deviantart_1.py_
  * A quick version of web scraper
  * Gives you each artwork amount of favs, comments and its link
  * Allows you iterate over specific username
  * Saves data in csv. format
  
* _deviantart_2.py_
  * A slower but better version of deviantart_1.py
  * Achieve everything deviantart_1.py outlined
  * Can also access its view
  * Also enables to select artwork that has specific tags

To go through specific artists, just add their username into the variable user_list and must be undercase.
You can find their username their URL "https://www.deviantart.com/USERNAME"
```python
# Users you want to check
user_list = ["gordon003"]
user_list = ["gordon003", "gordon003-others"]
```

For deviantart_2.py, you can add hashtags you want into the list which also must be undercase.
```python
# Hashtags you want
tags_list = ["totaldrama"]
```

## Requirement
* Python
  * Latest Version
* Selenium
  * https://selenium-python.readthedocs.io/installation.html
  * https://www.youtube.com/watch?v=Xjv1sY630Uc
* BeautifulSoup
  * https://www.crummy.com/software/BeautifulSoup/bs4/doc/
  * https://www.youtube.com/watch?v=ng2o98k983k
* Chrome Driver (for Selenium web driver)
  * https://chromedriver.chromium.org/getting-started
* Google Chrome
  * Can also use Firefox but you need to change the code
