#
# Flask example
# tutorial https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https 
# adhoc requires pip install pyopenssl
# to run just by flask run 
# import FLASK_APP=app 
# for some reason it gets message Ignoring a call to 'app.run()' that would block the current 'flask' CLI command." 
# hence, to use code in main have to run as python app.py
# otherwise, flask run --host=0.0.0.0 --port=5001 --cert=adhoc --debug
#  
# TODO
# refactore and replace urllib with regular request
# https://stackoverflow.com/questions/2018026/what-are-the-differences-between-the-urllib-urllib2-urllib3-and-requests-modul  


from flask import Flask, render_template, jsonify  #, request
import os
import logging

# import json to load JSON data to a python dictionary 
import json 
  
# urllib.request to make a request to api 
import urllib.request 
import urllib  
import requests

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


app = Flask(__name__)  


''' commented, not in use
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('500.html'), 500
'''


@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"


# https://stackoverflow.com/questions/15117416/capture-arbitrary-path-in-flask-route 
@app.route('/', defaults={'city': ''}, methods =['POST', 'GET']) # for empty path
@app.route('/<path:city>', methods =['POST', 'GET'])
def catch_all(city):
    '''
    Arbitary route of <host:port>/*
    Considers whatever text after "/"  as city name
    '''
    
    logging.info(f"URI requested: {city=}")

    if city :
      logging.info(f"URI requested: {city=}")
      # return f"The URI you entered is: {city}"
    else:
      logging.warning("No URI provided in the request.")
      logging.warning( "Provide a URI in the 'city' query parameter.xx ")
      return render_template('404.html', data = {"error":"Empty city: requires city name","cityname":city} )
       
  
    # openweathermap.org  API key. Have to obtain upfront 
    api = os.environ.get("WEATHER_API_TOKEN",None)

    logging.debug(f"API requested: {api=}")

    # source contain json data from api 
    # https://openweathermap.org/api/one-call-3#how 
    # https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key} 
    # api.openweathermap.org/data/2.5/onecall?lat=32.085300&lon=34.781769&exclude=alerts&appid=7da1d1af130566e75827795ef5b30af9 
    # https://api.openweathermap.org/data/2.5/weather?q=london,uk&APPID=7da1d1af130566e75827795ef5b30af9
    
    url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric"

    logging.debug(f"URI requested: {url=}  ")

    try:

      # source = urllib.request.urlopen(url).read()   # Employs urllib to return JSON of  weather data
      response = requests.get(url)  # Employs "requests" to return JSON of  weather data
      
      # converting JSON data to a dictionary 
      # weather_data_json = json.loads(source)  # Abandoned in favor of requests package
      weather_data_json = response.json()
      
 
      logging.debug(f"using request returns: {weather_data_json}")
  
      # data for variable weather_data_json , actual data to display
      data = { 
          "cityname": str(weather_data_json["name"]),
          "country_code": str(weather_data_json['sys']['country']), 
          "coordinate": str(weather_data_json['coord']['lon']) + ' ' 
                    + str(weather_data_json['coord']['lat']), 
          "temp": str(weather_data_json['main']['temp']) + ' C', 
          "pressure": str(weather_data_json['main']['pressure']), 
          "humidity": str(weather_data_json['main']['humidity']), 
      }
 
      logging.debug(data)
 
      return render_template('index.html', data = data)  # renders page with results 

    except urllib.error.HTTPError as e :
      print(f"HTTP error occurred: {e.code} - {e.reason}")
      logging.error(f"HTTP error occurred: {e.code} - {e.reason}")
      return render_template('404.html', data = {"error":e.code,"cityname":city} )

    except Exception as e :
      logging.error(f"Error occurred:  - {e}")
      print(f"Error occurred: - {e}")
      return render_template('500.html', data = {"error":e} )
      
# only if script started with 'python app.py'. 
if __name__ == "__main__" or True: 
  host = os.getenv('FLASK_HOST', '0.0.0.0')
  port = os.getenv('FLASK_PORT', '5001')

  logging.info(f"{host =} {port =}")  

  app.run(debug=True,    # Entry point
          ssl_context='adhoc',
#          host='0.0.0.0', port=443  #requires root/sudo
          host = host, port = port
          )
          

