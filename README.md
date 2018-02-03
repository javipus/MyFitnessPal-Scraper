## MyFitnessPal.com Scraper and Parser
======================================

* Scraps food diary on [MyFitnessPal](myfitnesspal.com)
* Gets pages of the form /food/diary/[USERNAME]?date=.\*
* Parses the page to get whatever information is available - e.g. macros,
  serving size
* The crawler only downloads the raw HTMLs to data/
* `getDiary(htmlfile)` parses the file and returns a pandas.DataFrame with all
  the info

#### Dependencies
-----------------

* scrapy
* BeautifulSoup
* HTMLParser
* NumPy
* Pandas

#### Run
-----------------
Replace `USERNAME` in `myfitnesspal/spiders/spider1.py` and run `$ scrapy crawl Myfitnesspal`

### TODO
-----------------
* Proper login
* Parse meal times e.g. Lunch, Dinner
* Parse micronutrients in main table regardless of column order
* Parse goal, total and excercise calories and macros
* Scrape database to get micronutrients for all foods
