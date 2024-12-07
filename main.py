from flask import Flask

app = Flask('App')

@app.route('/', methods=['GET'])
def welcome():
  return "<h1>asdfasdf</h1>"

if __name__ == 'main':
  app.run()
