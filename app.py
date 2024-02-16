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
# add debugging import logging 


from flask import Flask, render_template, request
import os
import logging

# import json to load JSON data to a python dictionary 
import json 
  
# urllib.request to make a request to api 
import urllib.request 
  

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# stop-gap. Fetch geospital by city name
# for brevity from predefined value in file. There are tel-aviv and london
def get_location(city: str ="tel-aviv"):
  return ("32.085300","34.781769") #FOR DEBUG ONLY!!!



app = Flask(__name__)

@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/', defaults={'path': ''}, methods =['POST', 'GET'])
@app.route('/<path:city>')
def catch_all(city):
#    return f"You entered: {city}"
    logging.info(f"URI requested: {city}")


#@app.route('/tel-aviv', methods =['POST', 'GET']) 
#def weather(): 
    #if request.method == 'POST': 
    #    city = request.form['city']
    if city:
      logging.info(f"URI requested: {city=}")
        #return f"The URI you entered is: {city}"
    else:
      logging.warning("No URI provided in the request.")
      logging.warning( "Provide a URI in the 'city' query parameter. Set default tel-aviv")
# for default name tel-aviv
      city = 'tel-aviv'
       
  
    # openweathermap.org  API key. Have to obtain upfront 
    api = os.environ.get("WEATHER_API_TOKEN",None)

    logging.debug(f"API requested: {api=}")
    lat,lon=get_location()
    part="alerts" #optional
    logging.debug(f"latitude requested: {lat=}")

    # source contain json data from api 
    # https://openweathermap.org/api/one-call-3#how 
    # https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key} 
    # api.openweathermap.org/data/2.5/onecall?lat=32.085300&lon=34.781769&exclude=alerts&appid=7da1d1af130566e75827795ef5b30af9 
    # https://api.openweathermap.org/data/2.5/weather?q=london,uk&APPID=7da1d1af130566e75827795ef5b30af9
    url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}"

    logging.debug(f"URI requested: {url=}")

    try:

      source = urllib.request.urlopen(url).read() 
 
      # converting JSON data to a dictionary 
      list_of_data = json.loads(source) 
  
      # data for variable list_of_data 
      data = { 
          "country_code": str(list_of_data['sys']['country']), 
          "coordinate": str(list_of_data['coord']['lon']) + ' ' 
                    + str(list_of_data['coord']['lat']), 
          "temp": str(list_of_data['main']['temp']) + 'k', 
          "pressure": str(list_of_data['main']['pressure']), 
          "humidity": str(list_of_data['main']['humidity']), 
      } 
      print(data) 
      return render_template('index.html', data = data) 

    except urllib.error.HTTPError as e :
      print(f"HTTP error occurred: {e.code} - {e.reason}")
      logging.error(f"HTTP error occurred: {e.code} - {e.reason}")
      return render_template('404.html', data = {})

# only if script started with 'python app.py'. 
if __name__ == "__main__" or True: #
  host = os.getenv('FLASK_HOST', '0.0.0.0')
  port = os.getenv('FLASK_PORT', '5001')

  print (f"{host =} {port =}")  

  app.run(debug=False,
          ssl_context='adhoc',
#          host='0.0.0.0', port=443  #requires root/sudo
           host = host, port = port
          )
          

