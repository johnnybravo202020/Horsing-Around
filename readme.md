# Horsing Around
*Django package that scraps data from the official web site of the horse races run in Turkey, in order to forecast the 
race results.*

![alt text][banner]

Official Web site of Turkish Jokey Organization:[Turkish](http://www.tjk.org/)|[English](http://www.tjk.org/EN/YarisSever/YarisSever/Index)

Abbreviations:
* ML: Machine Learning
* DL: Deep Learning
* BS: BeautifulSoup

## Brief Summary
Each day there are races in at least two cities and in those cities there are at least six races run for each city. 
The way to win the grand prize is to correctly guess the winners of the designated six race, this is called "Pick 6" in horse races. [more info](https://en.wikipedia.org/wiki/Pick_6_(horse_racing)). The goal of Horsing Around is to scrap the fixture and statics of each horse in order to leverage machine learning and deep learning algorithms. 

### Technical Summary
The entire project planned around Python and [Django](https://www.djangoproject.com). 

* django-horsing_around: Source code for the package
* horsingaroundtest: A django project for automated tests
* horsingaroundgui: GUI for presenting the data and forecasting

Suggested interpreter is [Anaconda](https://www.anaconda.com) since it comes with ML and DL frameworks. For scrappers
 [BS](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) will be used. For future [Celery](http://www.celeryproject.org/) is going to be used in order to create workers that will scrap the statics automatically.

## Quick Guide
### Installation through pip
* Download the package file 'horsing_around.tar.gz'
* Add the package to your django project by calling the command:
`pip install PATH\TO\THE\FILE\horsing_around.tar.gz `

### Usage
Import the City enum
```python
    from horsing_around import City
```

The return object will be list containing another list of each race and each race is another list of each horse that 
run that race. Depending on the used scrapper the horse object will be either model Result or model Fixture

##### Result Scrapper
Result Scrapper will contain the time and handicap information along with the other information for each horse run 
during the day.
```python
    # Import the scrapper
    from horsing_around.scrappers import ResultScrapper
    
    # Now scrap
    races = ResultScrapper.scrap(City.Bursa, year=2017, month=7, day=3)
```
You can also supply the date as a datetime object
```python
    import datetime
    
    races = ResultScrapper.scrap_by_date(City.Bursa, datetime.date(2017, 7, 3)) 
```

##### Fixture Scrapper
Fixture Scrapper will contain the information of upcoming races and won't contain any results like time and handicap
```python
    # Import the scrapper
    from horsing_around.scrappers import FixtureScrapper
    
    # Now scrap
    races = FixtureScrapper.scrap(City.Bursa, year=2017, month=7, day=3)
```
You can also supply the date as a datetime object
```python
    import datetime
    
    races = FixtureScrapper.scrap_by_date(City.Bursa, datetime.date(2017, 7, 3)) 
```
##### Collecting the statistics
Past results of the horses that were or going to be in the race can be collected along with the race information. 
However,
 since the scrapper needs to visit every page it takes a while depending on how many horses in total was iin the race.
```python
    races_fixture = FixtureScrapper.scrap(City.Istanbul, year=2017, month=10, day=8, get_past_statistics=True)

    races_results = ResultScrapper.scrap_by_date(City.Ankara, datetime.date(2017, 10, 7), get_past_statistics=True)
```

### Testing
There are two types of tests, first one is local and the other one is web tests. Local tests use the data in the local 
sqlite database, and web tests are done to make sure the web site is not updated and data can still scrapped correctly. Local tests are really fast but web tests are not so much since they download html's from the web.

* Download the package file 'horsing_around.tar.gz' and 'horsingaroundtest' directory inside the same directory.  
    *__Note__: If the package and the test project directory are not the same, pip will be unable to locate the package.
     If 
    so, you can also modify the path in the requirements.txt file to match the current path of the package.*
* Now install the required packages through pip.  
    ##### Mac and Linux
    Open a new terminal from the project directory:  
    * `cd horsingaroundtest`
    * `sudo pip install -r requirements.txt`
    
    ##### Windows
    Open a new command prompt as administrator from the project directory:
    * `cd horsingaroundtest`
    * `pip install -r requirements.txt`
    
    And run:  
    Local: `python manage.py test scrapper.tests.local`  
    Web : `python manage.py test scrapper.tests.web`
    

### GUI
* Download the package file 'horsing_around.tar.gz' and 'horsingaroundgui' directory inside the same directory
* Now install the required packages through pip just like described as above in the 'Testing' section.
* Open a new terminal or command prompt depending on the OS and go to the folder 'horsingaroundgui'
* Run `python manage.py runserver`
* Open a browser and go to the `http://127.0.0.1:8000/`

## Road Map
* Write tests for scrappers(Ongoing)
* ~~Develop the scrappers(Ongoing)~~
* Start forecasting with regression and create HTML pages for display
* Create a worker to scrap races automatically in order to save them to database 

## Eager to help?
Everybody is welcome for contribution. The ultimate reason for open-sourcing is to exceed the potential of this 
project and get the maximum accuracy, this cannot be done alone. Even small advices and suggestions are appreciated.


[banner]: github/banner.jpg "Horsing Around Banner"
