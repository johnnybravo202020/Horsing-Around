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
The way to win the grand prize is to correctly guess the winners of the designated six race, this is called "Pick 6" 
in horse races. [more info](https://en.wikipedia.org/wiki/Pick_6_(horse_racing)). The goal of Horsing Around is to 
scrap the fixture and statistics of each horse in order to leverage machine learning and deep learning algorithms. 

### Technical Summary
The entire project planned around Python and [Django](https://www.djangoproject.com). 

Suggested interpreter is [Anaconda](https://www.anaconda.com) since it comes with ML and DL frameworks. For scrappers
 [BS](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) will be used. For future [Celery](http://www.celeryproject.org/) is going to be used in order to create workers that will scrap the statics automatically.

## Quick Guide
### Installation through pip
* Add the package to your django project by calling the command:
`-e git://github.com/egeaydin/Horsing-Around.git#egg=horsing_around&subdirectory=django-horsing_around`

### Example
Import the City enum
```python
    from horsing_around import City
```
Import the scrapper that is going to gather the data

```python
    from horsing_around.scrappers import FixtureScrapper
```
Import the data model that will forecast the outcome

```python
    from horsing_around.forecaster import RaceDay
```

Call the scrap method of the ```FixtureScrapper``` to get the race program of a particular date and city. Also by 
setting the ```get_past_statistics``` parameter to ```True```, we collect the past results of the horses that are going to run that day.

```python
fixture = FixtureScrapper.scrap(City.Izmir, 2017, 11, 17, get_past_statistics=True)

```

Since the scrapper needs to visit all the horses' pages, it takes sometime to complete. Upon compilation, we create a
 new RaceDay object and pass the fixture to it. 
```python
race_day = RaceDay(fixture)
```

The `race_day` object contains multiple races and predictions of those races. Currently there are two different 
prediction techniques used:

 * Linear Regression  
    ```python
    linear_forecast = race_day.races[0].forecasts['LinearRegression']
    ```
 * Polynomial Regression
    ```python
    linear_forecast = race_day.races[0].forecasts['PolynomialRegression']
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
