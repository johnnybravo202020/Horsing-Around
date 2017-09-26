# Horsing Around
*Scraps data from the official web site of the horse races run in Turkey, in order to forecast the race results.*

**Current Functionalty:**
* Can scrap the results of a given date and city

Official Web site of Turkish Jokey Organization:[Turkish](http://www.tjk.org/)|[English](http://www.tjk.org/EN/YarisSever/YarisSever/Index)

Abbreviations:
* ML: Machine Learning
* DL: Deep Learning
* BS: BeautifulSoup

## Brief Summary
Each day there are races in at least two cities and in those cities there are at least six races run for each city. 
The way to win the grand prize is to correctly guess the winners of the designated six race, this is called "Pick 6" in horse races. [more info](https://en.wikipedia.org/wiki/Pick_6_(horse_racing)). The goal of Horsing Around is to scrap the fixture and statics of each horse in order to leverage machine learning and deep learning algorithms. 

### Technical Summary
The entire project planned around Python and [Django](https://www.djangoproject.com). Suggested interpreter is [Anaconda](https://www.anaconda.com) since it comes with ML and DL frameworks. For scrappers [BS](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) will be used. For future [Celery](http://www.celeryproject.org/) is going to be used in order to create workers that will scrap the statics automatically.

## Quick Guide

### Installation
[Download](https://www.anaconda.com/download/#download) and install the latest anaconda for your operating system. Now install the required packages through pip.
##### Mac and Linux
Open a new terminal from the project directory.  
`sudo pip install -r requirements.txt`

##### Windows
Open a new command prompt as administrator from the project directory.  
`pip install -r requirements.txt`

### Running
Make sure you run the tests for to make sure scrappers are working. Run `python manage.py test --exe` and if you see "OK" 
then run `python manage.py shell` in order to activate the django shell. 

From now on we can write python code.

Import the RaceResult model and City enum
```python
    from scrapper.models import RaceResult
    from scrapper.scrappers import City
```
Now we can call the scrap method from the model. 
```python
    races = RaceResult.objects.scrap(City.Bursa, year=2017, month=7, day=3)
```
This will return a list of races which contains the results of the respected race. 

You can also supply the date as a datetime object
```python
    import datetime
    
    races = RaceResult.objects.scrap(City.Bursa, datetime.date(2017, 7, 3)) 
```

Now, in order to see the results, we can do `print(races)`

## Road Map
* Write tests for scrappers(Ongoing)
* Develop the scrappers(Ongoing)
* Start forecasting with regression and create HTML pages for display
* Create a worker to scrap races automatically in order to save them to database 


## Eager to help?
Everybody is welcome for contribution. The ultimate reason for open-sourcing is to exceed the potential of this 
project and get the maximum accuracy, this cannot be done alone. Even small advices and suggestions are appreciated.
