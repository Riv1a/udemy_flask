from views import demo
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = ''

app.register_blueprint(demo)

if __name__ == '__main__':
    app.run(debug=True)   
