import datetime
import ctypes
from pexels_api import API
import requests
from bs4 import BeautifulSoup as html
import random
import os
#### MUST HAVE A PEXEL API KEY AND PIP INSTALL PEXEL API
#### pip install pexels-api



# This script performs the function of changing your wallpaper based on current conditions in calgary
# required is a pexel API key. Optional is a directory that you want the image saved to, and how many
# results per page

# you have to enter a pexelkey
PEXELKEY = ''

# Enter your desired directory as a str here. This is optional. If left with None it will download where this .py is running from
DIRECTORY = None


# subclass of pexels API. Performs the function of finding a wallpaper that meets the current conditions
# then it downloads it. API key for pexel is required. You can also enter in the directory that you want 
# the images saved to.
class findWallpaper(API):
    def __init__(self, PEXELS_API_KEY,direct=None,resultPage=10):
        super().__init__(PEXELS_API_KEY)
        self.direct = direct + '\\' if direct is not None else os.getcwd() + '\\'
        
        # resultPage is how many images load up in the search
        if isinstance(resultPage,int):
            self.resultPage = resultPage
        else:
            raise ValueError('it has to be an int')
    
    # searches the pexel api with the search term being the most current conditions formatted like
    # season, time of day, weather condition, wallpaper
    # EX. Fall day partly cloudy wallpaper
    def find_photo(self):
        # self.search returns however many resultPage equals to
        self.search(str(condition()), page=1, results_per_page=10)
        photos = self.get_entries()
        # uses random to choose a photo out of the images that are found to choose one
        return self.download(photos[random.randint(0,len(photos)-1)])

# downloads the image and saves it to the directory indicated.
# returns the path to the image
    def download(self,url: str):
        url = url.large2x
        fileName = self.direct + 'currWallpaper.jpg'
        img_data = requests.get(url).content
        with open(fileName,'wb') as handler:
            handler.write(img_data)
        return fileName

# object finds the current conditions outside.
class condition:
    def __init__(self,time=datetime.datetime.now()) -> None:
        self.time = time
        self.month = time.month
        self.hour = time.hour
        self.seasonDic = {
            'Winter': [12,1,2],
            'Spring': [3,4,5],
            'Summer': [6,7,8],
            'Fall': [9,10,11]
        }
        self.dayDic = {
            'morning': [6,7,8,9,10],
            'day': [11,12,13,14,15,16,17,18,19],
            'night':[20,21,22,23,24,0,1,2,3,4,5]
        }
# returns a string of the current conditions outside. adds wallpaper for search purposes.
    def __str__(self) -> str:
        #return 'Fall day Rainy wallpaper'
        return "%s %s %s wallpaper" %(self.season(),self.timeDay(), self.weatherParse())

# iterates through the season dictionary. When it finds the current month in the dictionary it returns the season
    def season(self):
        for dicMonth, dicValue in self.seasonDic.items():
            for m in dicValue:
                if m == self.month:
                    return dicMonth
# uses the same logic as the season function except it's for the time of day
    def timeDay(self):
        for timeOfDay, endStart in self.dayDic.items():
            if self.hour in endStart:
                return timeOfDay

# Parses through the present weather conditions and returns what the current condition is
    def weatherParse(self):
        text = self.weatherGet()
        a = text.find_all('dd', {'class':'mrgn-bttm-0'})
        return a[2].text

# Looks at weather.gc.ca to find the current weather out and returns the soup
    def weatherGet(self):
        ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        with requests.session() as sess:
            r = sess.get('https://weather.gc.ca/city/pages/ab-52_metric_e.html',headers=ua)
        return html(r.text,'lxml')

# gets the downloaded image and sets it as the wallpaper. It's also a subclass of
# findWallpaper. 
class osPaper(findWallpaper):
    def __init__(self, PEXELS_API_KEY, direct=None,resultPage=10):
        super().__init__(PEXELS_API_KEY, direct=direct,resultPage=resultPage)

    def pastePaper(self):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, self.find_photo() , 0)


if __name__ == '__main__':
    
    f = osPaper(PEXELKEY,direct=DIRECTORY)
    f.pastePaper()
