from flask import Flask, render_template
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, IntegerField, BooleanField, Form, FormField, FieldList, ValidationError#, DateField
from wtforms.validators import InputRequired, Length, AnyOf, Email
from collections import namedtuple
from wtforms.fields import DateField

class TelephoneForm(Form):
    country_code = IntegerField('country_code')
    area_code = IntegerField('area_code')
    number = StringField('number')

class YearForm(Form):
    year = IntegerField('year')
    total = IntegerField('total')
    
class LoginForm(FlaskForm):
    username = StringField('username', validators=[
        InputRequired('Input Required!'),
        Length(min=3, max=8, message='Your message is not the required length!')
    ])
    password = PasswordField('password', validators=[
        InputRequired('Input Required!'),
        AnyOf(values=['secret', 'password'])
    ])
    age = IntegerField('age', default=24)
    yesno = BooleanField('yesno')
    email = StringField('email', validators=[Email()])

class NameForm(LoginForm):
    first_name = StringField('first name')
    last_name = StringField('last name')
    home_phone = FormField(TelephoneForm)
    mobile_phone = FormField(TelephoneForm)
    years = FieldList(FormField(YearForm), min_entries=5)
    recaptcha = RecaptchaField('recaptcha')

    def validate_first_name(form, field):
        if field.data != 'Anthony':
            raise ValidationError('You do not have the right name.')

class DynamicForm(FlaskForm):
    entrydate = DateField('entrydate')#, format='%m/%d/&Y')

class User:
    def __init__(self, username, age, email):
        self.username = username
        self.age = age
        self.email = email


app = Flask(__name__)
app.config['SECRET_KEY'] = ''
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = ''
app.config['WTF_CSRF_TIME_LIMIT'] = 30
app.config['RECAPTCHA_PUBLIC_KEY'] = ''
app.config['RECAPTCHA_PRIVATE_KEY'] = ''
app.config['TESTING'] = True

@app.route('/', methods=['GET', 'POST'])
def index():
    user = User(username='John', age=50, email='John@yahoo.com')
    print('Before')
    print(user.username)
    print(user.age)
    print(user.email)

    group = namedtuple('Group', ['year', 'total'])
    g1 = group(2015, 10000)
    g2 = group(2016, 15000)
    g3 = group(2017, 25000)

    data = {'years' : [g1, g2, g3]}

    form = NameForm(obj=user, data=data)

    del form.mobile_phone

    if form.validate_on_submit():
        #form.populate_obj(user)
        #print('After')
        #print(user.username)
        #print(user.age)
        #print(user.email)
        #return f'Country Code {form.mobile_phone.country_code.data} Area Code {form.home_phone.area_code.data} Number{form.home_phone.number.data}'
        #return f'<h1>Username: {form.username.data} Password: {form.password.data} Age: {form.age.data} Yes/No: {form.yesno.data} Email: {form.email.data}</h1>'

        output = '<h1>'

        for field in form.years:
            output += f'Year: {field.year.data}'
            output += f'Total: {field.total.data} <br />'

        output += '</h1>'

        return output
    
    return render_template('index.html', form=form)

@app.route('/dynamic', methods=['GET', 'POST'])
def dynamic():
    DynamicForm.name = StringField('name')

    names = ['middle_name', 'last_name', 'nickname']

    for name in names:
        setattr(DynamicForm, name, StringField(name))

    form = DynamicForm()

    if form.validate_on_submit():
        print(type(form.entrydate.data))
        return f'<h1>Date: {form.entrydate.data} Name: {form.name.data} Last Name: {form.last_name.data}</h1>'


    return render_template('dynamic.html', form=form, names=names)

if __name__ == '__main__':
    app.run(debug=True)
