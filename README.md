# faq2bot
A bot to create bots

		This is the README file for Web2Bot Beta

1. About Web2Bot

Web2Bot was developed at Flow.ai, Tilburg, The Netherlands under the direction of Stefan Samba.
Web2Bot is script that allows you to scrape data form existing FAQ web pages and convert them in a format can be handled by the Flow.ai platform.  In this way an existing FAQ page can be translated into a bot with minimal effort. Always comply with local regulations.

To scrape elements of a website, the package BeautifulSoup is used. To learn more visit BeautifulSoup docs:

	https://www.crummy.com/software/BeautifulSoup/bs4/doc/

2. How it works
You will need the following files:

 1 Web Scraper.ipynb or Web Scraper.py
 2 Convert to Flow Format.ipynb or Convert to Flow Format.py
 3 Upload in Flow.ai (We'll create that one in the process)

2.1 Web Scraper.ipynb or Web Scraper.py
This is the main file for scraping elements from a site. You can select the singlepage or multipage folder depending on the set-up of your FAQ page. Make sure to adjust:
- Your page(s) to scrape, see “insert page to scrape” in file
- Elements that represent the questions, see “Create list of questions” in file
- Elements that represent the answers, see “Create list of answers” in file

2.2 Convert to Flow Format.ipynb or Convert to Flow Format.py
This file converts the export of 2.1 into a Flow.ai format called 'uploadthisfiletoflow.json’. You will need ‘export.json’, make sure to have it in the same folder.

2.3 Upload in Flow.ai
Upload your created .json file in Flow.ai. Project settings -> Backup -> Import -> Select 'uploadthisfiletoflow.json’ 


