from flask import Flask, render_template, g, request
from flask_babel import Babel, get_locale, get_timezone, format_date, format_datetime, gettext
from datetime import date, datetime

app = Flask(__name__)
babel = Babel(app)

app.config['SECRET_KEY'] = 'kagebunshinnojutsu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'

def get_locale():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    return request.accept_languages.best_match(['de', 'fr', 'en'])

def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone


@app.route('/')
def index():
    d = date(2011, 1, 8)
    dt = datetime(2010, 4, 9, 21, 13)
    local_date = format_date(d)
    local_datetime = format_datetime(dt)

    florian = gettext('Florian')
    python = gettext('Python')


    return render_template('index.html', locale=get_locale(), local_date=local_date, local_datetime=local_datetime, timezone=get_timezone(), florian=florian, python=python)


if __name__ == '__main__':
    app.run(debug=True)