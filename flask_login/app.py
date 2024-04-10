from flask import request, jsonify, render_template, session, redirect, url_for
from config import app, db
from models import User
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user, fresh_login_required
from urllib.parse import urlparse, urljoin

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'You need to login to access this page.'
login_manager.refresh_view = 'login'
login_manager.needs_refresh_message = 'You need to login again.'

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))

    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@app.route('/')
def index():
    return '<h1>Home Page</h1>'

@app.route('/register', methods=['Post'])
def register():
    email = request.json.get('email')
    username = request.json.get('username')

    if not email or not username:
        return (
            jsonify({"message" : "Must include Username and Email."}), 400
        )
    
    new_user = User(email=email, username=username)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return jsonify({"message" : str(e)}), 400
    
    return jsonify({"message" : "User created!"}), 201

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        remember_me = request.form.get('remember_me')

        user = User.query.filter_by(username=username).first()

        if not user:
            return '<h1>Unauthorized Access</h1>'
        
        login_user(user, remember=remember_me)

        if 'next' in session and session['next']:
            if is_safe_url(session['next']):
                return redirect(session['next'])
        
        return redirect(url_for('index'))
    session['next'] = request.args.get('next')
    return render_template('login.html')

@app.route('/profile')
@login_required
def profile():
    return f'<h1>You are in the Profile, {current_user.username}.</h1>'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return '<h1>Logout successfully</h1>'

@app.route('/change')
@fresh_login_required
def change():
    return '<h1>Only for fresh logins</h1>'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
