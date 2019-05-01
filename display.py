
import os
import csv
import math
import requests
import pendulum
from PIL import Image, ImageDraw, ImageFont


class Display():

    def __init__(self, image):
        self.d = ImageDraw.Draw(image)
        self.outline = 'black'
        self.fill = 'white'
        self.symbols = {}
        self.now = pendulum.now(tz='Europe/Helsinki')

        # mapping from weathericon font symbols to code-points
        with open('symbols.csv') as symbols:
            for row in csv.reader(symbols):
                self.symbols[row[0]] = chr(int(row[1], 16))

        # openweathermap
        self.ow_location = os.environ['OW_LOCATION']
        self.ow_apikey = os.environ['OW_APIKEY']


    def draw(self):
        self.date((220, 150))
        self.time((250, 40))
        self.weather((20, 10))


    def date(self, coords):
        font = ImageFont.truetype('OpenSans-Regular.ttf', 50)
        weekdays = ['ma', 'ti', 'ke', 'to', 'pe', 'la', 'su']
        self.d.text(coords, '{} {}.{}.'.format(weekdays[self.now.weekday()],
                                              self.now.day, self.now.month),
                    font=font,
                    fill=self.outline)


    def time(self, coords):
        time_decimal = (self.now.hour % 12) + (self.now.minute / 60)
        angle = (math.pi * 2 * time_decimal / 12) + math.pi * 1.5
        radius = 50
        x = coords[0] + radius
        y = coords[1] + radius

        self.d.line([x,
                     y,
                     x + radius * math.cos(angle),
                     y + radius * math.sin(angle)],
                    width=10,
                    fill=self.outline)

        # clock frame
        self.d.rectangle([x - radius - 15,
                          y - radius - 15,
                          x + radius + 15,
                          y + radius + 15],
                         outline=self.outline,
                         width=4)

        # dot in the center of clock
        self.d.rectangle([x-10,y-10,x+10,y+10], outline=self.outline, fill=self.outline, width=4)


    def weather(self, coords):
        # mapping from https://openweathermap.org/weather-conditions to weathericons symbols
        icons = {'01d': self.symbols['day-sunny'],
                 '02d': self.symbols['day-cloudy'],
                 '03d': self.symbols['cloud'],
                 '04d': self.symbols['cloudy'],
                 '09d': self.symbols['showers'],
                 '10d': self.symbols['raindrops'],
                 '11d': self.symbols['thunderstorm'],
                 '13d': self.symbols['snow'],
                 '50d': self.symbols['dust'],
                 '01n': self.symbols['night-clear'],
                 '02n': self.symbols['night-alt-cloudy'],
                 '03n': self.symbols['cloud'],
                 '04n': self.symbols['cloudy'],
                 '09n': self.symbols['showers'],
                 '10n': self.symbols['raindrops'],
                 '11n': self.symbols['thunderstorm'],
                 '13n': self.symbols['snow'],
                 '50n': self.symbols['dust']}

        res = requests.get('https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID={}'.format(self.ow_location, self.ow_apikey))
        data = res.json()

        x, y = coords

        font = ImageFont.truetype('OpenSans-Regular.ttf', 40)
        font_head = ImageFont.truetype('OpenSans-Regular.ttf', 20)
        sym =  ImageFont.truetype('weathericons-regular-webfont.ttf', 45)

        # weather now
        self.d.text((x, y), 'sää nyt', font=font_head, fill=self.outline)
        self.d.text((x + 90, y), icons[data['weather'][0]['icon']], font=sym, fill=self.outline)
        y = y + 30
        self.d.line([x, y, x + 65, y], fill=self.outline)

        # temperature
        y = y + 20
        self.d.text((x, y), self.symbols['celsius'], font=sym, fill=self.outline)
        self.d.text((x + 60, y + 5), '{:.1f}'.format(data['main']['temp']), font=font, fill=self.outline)

        # humidity
        y = y + 50
        self.d.text((x, y), self.symbols['humidity'], font=sym, fill=self.outline)
        self.d.text((x + 60, y + 5), str(data['main']['humidity']), font=font, fill=self.outline)

        # weather forecast
        y = y + 70
        self.d.text((x, y), 'ennuste', font=font_head, fill=self.outline)
        y = y + 30
        self.d.line([x, y, x + 75, y], fill=self.outline)

        res = requests.get('https://api.openweathermap.org/data/2.5/forecast/hourly?q={}&units=metric&APPID={}'.format(self.ow_location, self.ow_apikey))
        data = res.json()

        for f in data['list'][0:6]:
            time = pendulum.from_timestamp(f['dt'], tz='Europe/Helsinki')
            time_str = '{}:{:02d}'.format(time.hour, time.minute)
            symbol_str = icons[f['weather'][0]['icon']]
            self.d.text((x, y), symbol_str, font=sym, fill=self.outline)
            self.d.text((x, y + 50), time_str, font=font_head, fill=self.outline)
            x = x + 60
