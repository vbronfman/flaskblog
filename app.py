#
# Flask example
# tutorial https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https 
# adhoc requires pip install pyopenssl
# to run just by flask run 
# import FLASK_APP=app 
# for some reason it gets message Ignoring a call to 'app.run()' that would block the current 'flask' CLI command." 
# hence, to use code in main have to run as python app.py
# otherwise, flask run --host=0.0.0.0 --port=5001 --cert=adhoc --debug

from flask import Flask
import os

print(__name__)
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

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
          

