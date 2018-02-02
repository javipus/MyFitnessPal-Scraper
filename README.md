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
`$ scrapy crawl Myfitnesspal`
