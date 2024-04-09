from flask import request, jsonify
from config import app, db
from models import User
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
