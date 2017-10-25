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

Suggested interpreter is [Anaconda](https://www.anaconda.com) since it comes with ML and DL frameworks. For scrappers
 [BS](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) will be used. For future [Celery](http://www.celeryproject.org/) is going to be used in order to create workers that will scrap the statics automatically.

## Quick Guide
### Installation through pip
* Add the package to your django project by calling the command:
`-e git://github.com/egeaydin/Horsing-Around.git#egg=horsing_around&subdirectory=django-horsing_around`

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

## Road Map
* Write tests for scrappers(Ongoing)
* ~~Develop the scrappers(Ongoing)~~
* Start forecasting with regression and create HTML pages for display
* Create a worker to scrap races automatically in order to save them to database 

## Eager to help?
Everybody is welcome for contribution. The ultimate reason for open-sourcing is to exceed the potential of this 
project and get the maximum accuracy, this cannot be done alone. Even small advices and suggestions are appreciated.


[banner]: github/banner.jpg "Horsing Around Banner"
