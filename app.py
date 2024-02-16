#
# Flask example
# tutorial https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https 
# adhoc requires pip install pyopenssl
# to run just by flask run 
# import FLASK_APP=app 
# for some reason it gets message Ignoring a call to 'app.run()' that would block the current 'flask' CLI command." 
# hence, to use code in main have to run as python app.py
# otherwise, flask run --host=0.0.0.0 --port=5001 --cert=adhoc --debug

from flask import Flask, render_template, request
import os
# import json to load JSON data to a python dictionary 
import json 
  
# urllib.request to make a request to api 
import urllib.request 
  


print(__name__)
app = Flask(__name__)

@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/', methods =['POST', 'GET']) 
def weather(): 
    if request.method == 'POST': 
        city = request.form['city'] 
    else: 
        # for default name mathura 
        city = 'mathura'
  
    # your API key will come here 
    api = api_key_here 
  
    # source contain json data from api 
    source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q =' + city + '&appid =' + api).read() 
  
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
          

