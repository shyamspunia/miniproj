from django.shortcuts import render
import requests
from datetime import datetime,timedelta,timezone,UTC,time
from django.utils import timezone
from .models import City
from django.db.models import Count
from django.db.models import Min



# Create your views here.

def hello(request):
    return render(request,'subtemps/hello.html')


def index(request):
    error = None
    Weather = []
    cityz = ""
    if request.method == 'POST':
        cityz = request.POST.get('city_name') # get value from HTML form    
        url = f"http://api.openweathermap.org/data/2.5/weather?q={cityz}&APPID=edea39996fcc478fdd3bcbf058060ace"
        response = requests.get(url).json()
        data = response
        if data.get('cod') == 200:
          City.objects.get_or_create(name=cityz)
        else:
          error = f"City \"{cityz}\" not found"


    cities = City.objects.distinct() 
    

    for city in cities:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&APPID=edea39996fcc478fdd3bcbf058060ace"
            response = requests.get(url).json()
            data = response
            if data.get('cod') == 200:
              
              timezone_offset = data.get('timezone',0)

              utc_now= timezone.now()
              local_time = utc_now + timedelta(seconds=timezone_offset)
              Timenow = local_time.hour


              if 5 <= Timenow < 12: 
                day_part = "Morning" 
              elif 12 <= Timenow < 17: 
                day_part = "Afternoon" 
              elif 17 <= Timenow < 21: 
                day_part = "Evening"
              else: 
                 day_part = "Night"

              icon = data['weather'][0]['icon']
              icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
 
              deg = data['wind']['deg']

              if deg == 0 or deg in range(0,12) or deg in range(326,360):
                  direction = "North"
              if deg in range(11,56):
                  direction = "Northeast"
              if deg in range(56,101):
                  direction = "East"
              if deg in range(101,146):
                 direction = "Southeast"
              if deg in range(146,191):
                 direction = "South"
              if deg in range(191,236):
                 direction = "SouthWest"
              if deg in range(236,281):
                 direction = "West"
              if deg in range(281,326):
                 direction = "NorthWest"

              # weather_images= {
              #    "Thunderstorm": "static/weatherstatic/Thunderstorm.jpg",
              #    "Fog": "static/weatherstatic/Fog.jpg",
              #    "overcast clouds": "static/weatherstatic/overcast clouds.jpg",
              #    "snow": "static/weatherstatic/snow.jpg",
              #    "clear sky": "static/weatherstatic/clear sky .jpg",
              #    "broken clouds": "static/weatherstatic/broken clouds.jpg",
              #    "few clouds": "static/weatherstatic/few clouds.jpg"}
                 

              # desc = data['weather'][0]['description'] 
                
              # image = weather_images.get(desc)

              # print(image)
               




              datax = {
              'city' : data['name'],
              'weather' : data['weather'][0]['description'],
              'Temp': round(data['main']['temp']-273.15),
              'Feels_like' : round(data['main']['feels_like']-273.15),
              # 'min_temp' : round(data['main']['temp_min']-273.15),
              # 'max_temp' : round(data['main']['temp_max']-273.15),
              'humidity': data['main']['humidity'],
              'day_part' : day_part,
              'wind_speed' : data['wind']['speed'],
              'Time': Timenow,
              'Direction': direction,
              'icon_url' : icon_url
              }

              if datax['city'].strip().lower() == cityz.strip().lower():
                  Weather.insert(0, datax)
                  print(True)
              else:
                  Weather.append(datax)
 
                
    return render(request,'subtemps/index.html',{'Weather':Weather,'error':error})

# def trial(request):
#    if request.method == 'POST':
#         city = request.POST.get('city_name') # get value from HTML form    

#         City.objects.get_or_create(name=city)

#    cities = City.objects.distinct()

#    weather = []
#    for c in cities:
#        url = f"http://api.openweathermap.org/data/2.5/weather?q={c}&APPID=edea39996fcc478fdd3bcbf058060ace"
#        response = requests.get(url).json()
#        data = response
#        if data.get('cod') == 200:
#               timezone_offset = data.get('timezone',0)
 
#               utc_now= timezone.now()
#               local_time = utc_now + timedelta(seconds=timezone_offset)
#               Timenow = local_time.hour

#               if 5 <= Timenow < 12: 
#                 day_part = "Morning" 
#               elif 12 <= Timenow < 17: 
#                 day_part = "Afternoon" 
#               elif 17 <= Timenow < 21: 
#                 day_part = "Evening"
#               else: 
#                  day_part = "Night"

#               icon = data['weather'][0]['icon']
#               icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
 
#               deg = data['wind']['deg']

#               if deg == 0 or deg in range(0,12) or deg in range(326,360):
#                   direction = "North"
#               if deg in range(11,56):
#                   direction = "Northeast"
#               if deg in range(56,101):
#                   direction = "East"
#               if deg in range(101,146):
#                  direction = "Southeast"
#               if deg in range(146,191):
#                  direction = "South"
#               if deg in range(191,236):
#                  direction = "SouthWest"
#               if deg in range(236,281):
#                  direction = "West"
#               if deg in range(281,326):
#                  direction = "NorthWest"

#               datax = {
#               'city' : data['name'],
#               'weather' : data['weather'][0]['description'],
#               'Temp': round(data['main']['temp']-273.15),
#               'Feels_like' : round(data['main']['feels_like']-273.15),
#               'humidity': data['main']['humidity'],
#               'day_part' : day_part,
#               'wind_speed' : data['wind']['speed'],
#               'Time': Timenow,
#               'Direction': direction,
#               'icon_url' : icon_url
#               }
        
        
#        weather.append(datax)

#    return render(request,'subtemps/trial.html',{'weather':weather,'cities' : cities})

# def deletedup(request):
#    # Keep only one record per city name

#    duplicates = City.objects.values('name').annotate(min_id=Min('id')).values_list('name', 'min_id')

#    for name, min_id in duplicates:
#     City.objects.filter(name=name).exclude(id=min_id).delete()

#    cities = City.objects.distinct()


#    weather = []
#    for c in cities:
#        url = f"http://api.openweathermap.org/data/2.5/weather?q={c}&APPID=edea39996fcc478fdd3bcbf058060ace"
#        response = requests.get(url).json()
#        data = response
#        if data.get('cod') == 200:
#         datax = {
#            'city' : data['name'],
#            'weather' : data['weather'][0]['description'],
#            'Temp': round(data['main']['temp']-273.15)
           
#         }
        
#        weather.append(datax)

#    return render(request,'subtemps/trial.html',{'weather':weather,'cities' : cities})

   




       
   
















