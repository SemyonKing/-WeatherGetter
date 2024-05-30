import requests
import json
import socket
from bs4 import BeautifulSoup
from datetime import time, datetime
from flask import Flask




class Weather:
    url = "https://meteobaza.ru/ryazanskaya-oblast/ryazan.php"
    response = requests.get(url)
    bs = BeautifulSoup(response.text, "html.parser")

    temp = int(bs.find('font', class_="nedtemp1").getText().split('°')[0])
 
    cloudiness = bs.find('td', class_="borseg").find('img')['title'].split(',')[0]
 
    wind_speed = bs.find_all('font', class_="progseg")[1].parent.getText().split()[2]
   
    sun_up_time = bs.find_all('font', class_="progseg2")[0].getText().split(':')
    sun_down_time = bs.find_all('font', class_="progseg2")[1].getText().split(':')

    def unixReform(times):    
        time_now = time(int(times[0]),int(times[1]))
        date_now = datetime(datetime.now().year, datetime.now().month, datetime.now().day, time_now.hour, time_now.minute)
        return date_now.timestamp()
    
    sun_up = unixReform(sun_up_time)
    sun_down = unixReform(sun_down_time)
    
    rain = bs.find('td', class_="borseg").find('img')['title'].split(',')[1].strip()
    
   
    if "(" in rain:
        rain = rain.split("(")[1].split("/")[0].split("м")[0]
    else: rain = 0
        
    weather = {
        "temp": temp,
        "cloudiness": cloudiness,
        "wind_speed": wind_speed,
        "sun_up": sun_up,
        "sun_down": sun_down,
        "rain": rain
    }
    
app = Flask(__name__)
@app.route('/', methods=['GET'])
def login():
        return Weather.weather
    
if __name__ == "__main__":
    app.run(port=8000, debug=True)