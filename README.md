### Weather API
Welcome to weather API, the app uses [openweathermap one call api](https://openweathermap.org/api/one-call-api) 

It returns min,max,mean and median temperature and humidity for a given period.

To get the above go to `<url>/weatherapi/forcast/<cityname>/<period>`

where period can be:
`daily` which shows averages of the next 7 days or `hourly` - which returns average of next 48 hours

Running the app 
``` 
create a virtual environment
`python3 -m venv env`
`source env/bin/activate`
Install required modules
`pip install -r requirements.txt`
The to run the app
`python3 manage.py runserver` 
```

Note:
The apps assumes memchached is running on `127.0.0.1:11211`
